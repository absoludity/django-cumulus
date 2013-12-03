import unittest
import pyrax

from mock import patch


class PyraxTestCase(unittest.TestCase):
    """Restore pyrax settings after each test.

    The pyrax module keeps state in the class attribute
    pyrax.Settings._settings. We don't want our tests leaving
    modifications to the pyrax settings.
    """
    def setUp(self):
        """Patch the class attribute that keeps the pyrax settings."""
        super(PyraxTestCase, self).setUp()
        blank_settings = pyrax.Settings()
        blank_settings = {
            "default": dict.fromkeys(pyrax.Settings.env_dct.keys()),
        }
        patcher = patch.object(pyrax.Settings, '_settings', blank_settings)
        self.addCleanup(patcher.stop)
        patcher.start()



