# coding: utf-8

import pickle
import unittest
from os.path import join

from nutstore_cli.client.file import FileTable


class FileTestCase(unittest.TestCase):
    with open(join('raw', 'two_files.pickle'), 'rb') as f:
        files = pickle.loads(f.read())

    def test_table_display(self):
        table = FileTable(self.files)
        print(table.get_listing_columns())


if __name__ == '__main__':
    unittest.main()
