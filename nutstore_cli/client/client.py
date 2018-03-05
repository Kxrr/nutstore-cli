# coding: utf-8
from dateutil.parser import parse as dt_parse

from nutstore_cli.client.base import BaseNutStoreClient
from nutstore_cli.client.utils import get_attr


class NutStoreClient(BaseNutStoreClient):
    def search_latest(self, pattern):
        """
        根据pattern获取最新的文件
        """
        sorted_files = sorted(self.search(pattern), key=lambda f: dt_parse(f.mtime))
        return sorted_files[-1].name if sorted_files else None

    def download_latest_file(self):
        filename = self.search_latest('')
        return self.download(filename)
