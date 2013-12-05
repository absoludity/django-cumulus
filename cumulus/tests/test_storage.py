import unittest
import pyrax

from mock import patch

from cumulus.storage import SwiftclientStorage
from cumulus.tests.helpers import PyraxTestCase


class SwiftclientStorageTestCase(PyraxTestCase):

    def setUp(self):
        super(SwiftclientStorageTestCase, self).setUp()

        patcher = patch('cumulus.storage.pyrax')
        self.addCleanup(patcher.stop)
        pyrax = patcher.start()

        self.pyrax_connection = pyrax.connect_to_cloudfiles.return_value
        self.container = self.pyrax_connection.create_container.return_value

    def test__get_object_does_not_iterate_names(self):
        storage = SwiftclientStorage()

        result = storage._get_object('foo.txt')

        self.assertEqual(self.container.get_object.return_value, result)
        self.assertEqual(0, self.container.get_object_names.call_count)
        self.assertEqual(1, self.container.get_object.call_count)

    def test__get_object_returns_none(self):
        storage = SwiftclientStorage()
        self.container.get_object.side_effect = pyrax.exceptions.NoSuchObject

        result = storage._get_object('foo.txt')

        self.assertIsNone(result)
