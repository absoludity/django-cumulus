import unittest
import pyrax

from mock import patch

from cumulus.utils import ensure_pyrax_settings


class EnsurePyraxSettingsTestCase(unittest.TestCase):

    def patch_cumulus_settings(self, **kwargs):
        patcher = patch.dict('cumulus.utils.CUMULUS', **kwargs)
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_noop_for_no_values(self):
        self.patch_cumulus_settings(PYRAX_IDENTITY_TYPE=None,
                                    AUTH_URL=None,
                                    AUTH_TENANT_ID=None)

        ensure_pyrax_settings()

        self.assertIsNone(pyrax.get_setting('identity_type'))
        self.assertIsNone(pyrax.get_setting('auth_endpoint'))
        self.assertIsNone(pyrax.get_setting('tenant_id'))

    def test_sets_pyrax_settings(self):
        self.patch_cumulus_settings(PYRAX_IDENTITY_TYPE='keystone',
                                    AUTH_URL='http://example.com',
                                    AUTH_TENANT_ID='abc123')

        ensure_pyrax_settings()

        self.assertEqual('keystone', pyrax.get_setting('identity_type'))
        self.assertEqual('http://example.com',
                         pyrax.get_setting('auth_endpoint'))
        self.assertEqual('abc123', pyrax.get_setting('tenant_id'))
