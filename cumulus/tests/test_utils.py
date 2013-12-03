import unittest
import pyrax

from mock import (
    call,
    patch,
)

from cumulus.utils import ensure_pyrax_settings


class EnsurePyraxSettingsTestCase(unittest.TestCase):

    def setUp(self):
        """The pyrax module keeps state - we don't want to affect state."""
        super(EnsurePyraxSettingsTestCase, self).setUp()
        patcher = patch('cumulus.utils.pyrax')
        self.addCleanup(patcher.stop)
        self.mock_pyrax = patcher.start()

    def patch_cumulus_settings(self, **kwargs):
        patcher = patch.dict('cumulus.utils.CUMULUS', **kwargs)
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_noop_for_no_values(self):
        self.patch_cumulus_settings(PYRAX_IDENTITY_TYPE=None,
                                    AUTH_URL=None,
                                    AUTH_TENANT_ID=None)

        ensure_pyrax_settings()

        self.assertEqual(0, self.mock_pyrax.set_setting.call_count)

    def test_sets_pyrax_settings(self):
        self.patch_cumulus_settings(PYRAX_IDENTITY_TYPE='keystone',
                                    AUTH_URL='http://example.com',
                                    AUTH_TENANT_ID='abc123')

        ensure_pyrax_settings()

        expected_calls = [
            call('identity_type', 'keystone'),
            call('auth_endpoint', 'http://example.com'),
            call('tenant_id', 'abc123'),
        ]
        self.mock_pyrax.set_setting.assert_has_calls(
            expected_calls, any_order=True)
