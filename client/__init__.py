# coding: utf-8
import re
import sys
import tempfile
import logging
from os import path as p
from contextlib import contextmanager

from urlparse import urljoin
from dateutil.parser import parse as dt_parse

try:
    from itertools import ifilter
except ImportError:
    ifilter = filter

from client.file import FileTable

try:
    import easywebdav
except ImportError:
    sys.exit('Easywebdav required, try: pip install easywebdav')

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
log = logging.getLogger('webdav')


def join(base, path, **kwargs):
    """Copied from http-prompt/http_prompt/execution.py"""
    if not base.endswith('/'):
        base += '/'
    url = urljoin(base, path, **kwargs)
    if url.endswith('/') and not path.endswith('/'):
        url = url[:-1]
    return url


class NutStoreClient(object):
    """坚果云"""

    server = 'dav.jianguoyun.com'
    working_dir = ''

    def __init__(self, username, password, working_dir, check_conn=True):
        if not working_dir.startswith('/'):
            working_dir = '/' + working_dir
        self.cd(working_dir)
        self._client = easywebdav.connect(self.server, username=username, password=password)

        if check_conn:
            self.check_conn()

    @property
    def _working_dir(self):
        """Fixed path for NutStoreDAV operation"""
        return 'dav' + self.working_dir

    @property
    def cwd(self):
        """Current working directory for display"""
        return self.working_dir

    def upload(self, local_path, cloud_dir=None):
        assert p.exists(local_path)
        cloud_path = self.to_cloud_path(p.basename(local_path))
        log.info('[Upload] {0} => {1}'.format(local_path, cloud_path))
        self._client.upload(local_path, cloud_path)

    def download(self, cloud_file, store_path=None):
        cloud_file = self.to_cloud_path(cloud_file)
        local_path = store_path or tempfile.mktemp(p.splitext(cloud_file)[-1])
        log.info('[Download] {0} => {1}'.format(cloud_file, local_path))
        self._client.download(cloud_file, local_path)
        return local_path

    def formatted_ls(self):
        table = FileTable(self.ls())
        table.sort(key=lambda f: f.mtime)
        return table.get_display()

    def ls(self):
        return self._client.ls(self._working_dir)

    def cd(self, directory):
        self.working_dir = join(self.working_dir, directory)

    def rm(self, cloud_path):
        self._client.delete(self.to_cloud_path(cloud_path))

    def mkdir(self, directory):
        return self._client.mkdir(directory)

    @contextmanager
    def cd_context(self, directory):
        saved = self.working_dir
        yield self.cd(directory)
        self.working_dir = saved

    def search(self, pattern):
        files = self.ls()
        return ifilter(
            lambda f: (re.search(pattern=pattern, string=f.name, flags=re.IGNORECASE) and f.size != 0), files
        )

    def to_cloud_path(self, path):
        if not path.startswith('dav'):
            return 'dav' + join(self.working_dir, path)
        return path

    def check_conn(self):
        self.ls()
        return True

    def search_latest(self, pattern):
        """
        根据pattern获取最新的文件
        """
        sorted_files = sorted(self.search(pattern), key=lambda f: dt_parse(f.mtime))
        return sorted_files[-1].name if sorted_files else None

    def download_latest_file(self):
        filename = self.search_latest('')
        return self.download(filename)
