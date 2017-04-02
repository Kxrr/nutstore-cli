# coding: utf-8
import unittest

from nutstore_cli.execution import grammar


class GrammarTestCase(unittest.TestCase):
    def test_parse_cd(self):
        for c in ['a', 'a_', 'a.b']:
            root = grammar.parse('cd {}'.format(c))
            cd = root.children[0]
            self.assertEqual(cd.expr_name, 'cd')

    def test_parse_download(self):
        text = 'download a.txt /tmp/a.txt'
        root = grammar.parse(text)
        download = root.children[0]
        self.assertEqual(download.expr_name, 'download')
        self.assertEqual(len(download.children), 5)

    def test_parse_upload(self):
        text = 'upload /tmp/a.txt'
        root = grammar.parse(text)
        upload = root.children[0]
        self.assertEqual(upload.expr_name, 'upload')

    def test_parse_ls(self):
        for text in (
                'ls',
                'ls  | grep something',
        ):
            root = grammar.parse(text)

    def test_parse_help(self):
        text = 'help'
        grammar.parse(text)


if __name__ == '__main__':
    unittest.main()
