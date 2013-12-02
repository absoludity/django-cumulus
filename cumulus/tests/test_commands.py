import unittest
import pyrax

from django.core.management import call_command

from mock import patch


class ContainerCreateTestCase(unittest.TestCase):

    def setUp(self):
        super(ContainerCreateTestCase, self).setUp()
        patcher = patch('cumulus.management.commands.container_create.'
                        'swiftclient')
        self.addCleanup(patcher.stop)
        self.swiftclient = patcher.start()
        self.connection = self.swiftclient.Connection.return_value

        patcher = patch('cumulus.management.commands.container_create.'
                        'pyrax.set_credentials')
        self.addCleanup(patcher.stop)
        self.pyrax_set_credentials = patcher.start()

        patcher = patch('cumulus.management.commands.container_create.'
                        'pyrax.connect_to_cloudfiles')
        self.addCleanup(patcher.stop)
        connect_to_cloudfiles = patcher.start()
        self.pyrax_connection = connect_to_cloudfiles.return_value

    def patch_cumulus_settings(self, **kwargs):
        patcher = patch.dict('cumulus.utils.CUMULUS', **kwargs)
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_creates_swiftclient_connection(self):
        self.patch_cumulus_settings(
            AUTH_URL='http://example.com/v1/auth', USERNAME='fredrick',
            API_KEY='sekrit', SERVICENET=False, AUTH_VERSION='2.0',
            AUTH_TENANT_NAME='users', USE_PYRAX=False)

        call_command('container_create', 'test-container')

        self.swiftclient.Connection.assert_called_once_with(
            tenant_name='users', snet=False,
            authurl='http://example.com/v1/auth', auth_version='2.0',
            user='fredrick', key='sekrit')

    def test_puts_container(self):
        self.patch_cumulus_settings(USE_PYRAX=False)

        call_command('container_create', 'test-container')

        self.connection.put_container.assert_called_once_with('test-container')

    def test_container_public_by_default(self):
        self.patch_cumulus_settings(USE_PYRAX=False)

        call_command('container_create', 'test-container')

        self.connection.post_container.assert_called_once_with(
            'test-container', headers={"X-Container-Read": ".r:*"})

    def test_container_not_public_when_private_specified(self):
        self.patch_cumulus_settings(USE_PYRAX=False)

        call_command('container_create', 'test-container', private=True)

        self.assertEqual(0, self.connection.post_container.call_count)

    def test_pyrax_settings(self):
        self.patch_cumulus_settings(AUTH_URL='http://example.com/v1/auth',
                                    USE_PYRAX=True,
                                    PYRAX_IDENTITY_TYPE='keystone')

        call_command('container_create', 'test-container')

        self.assertEqual(pyrax.get_setting('auth_endpoint'),
                         'http://example.com/v1/auth')

    def test_cdn_enabled(self):
        self.patch_cumulus_settings(USE_PYRAX=True, TTL=999,
                                    PYRAX_IDENTITY_TYPE='keystone')

        call_command('container_create', 'test-container')

        self.pyrax_connection.get_container.assert_called_once_with(
            'test-container')
        container = self.pyrax_connection.get_container.return_value
        container.make_public.assert_called_once_with(ttl=999)
