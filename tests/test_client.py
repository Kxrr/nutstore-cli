# coding: utf-8
import unittest

from nutstore_cli.client.client import NutStoreClient
from tests import NutStoreTestCase


class NutStoreClientTestCase(NutStoreTestCase):

    def test_cd(self):
        client = NutStoreClient('', '', 'demo', check_conn=False)
        self.assertEqual(client._working_dir, 'dav/demo')

        client.cd('/mov')
        self.assertEqual(client._working_dir, 'dav/mov')

        client.cd('a')
        self.assertEqual(client._working_dir, 'dav/mov/a')

        client.working_dir = '/mov/a'
        client.cd('..')
        self.assertEqual(client._working_dir, 'dav/mov')


if __name__ == '__main__':
    unittest.main()
