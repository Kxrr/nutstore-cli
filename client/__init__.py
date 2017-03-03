# coding: utf-8
import re
import sys
import tempfile
import logging
from os import path
from contextlib import contextmanager

from dateutil.parser import parse as dt_parse

try:
    from itertools import ifilter
except ImportError:
    ifilter = filter

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
log = logging.getLogger('webdav')

try:
    import easywebdav
except ImportError:
    sys.exit('Easywebdav required, try: pip install easywebdav')


def join(*names):
    return path.sep.join(names)


class NutStoreClient(object):
    """坚果云"""

    server = 'dav.jianguoyun.com'
    working_dir = ''

    def __init__(self, username, password, working_dir, check_conn=True):
        self.cd(working_dir)
        self._client = easywebdav.connect(self.server, username=username, password=password)

        if check_conn:
            self.check_conn()

    @property
    def cwd(self):
        return self.working_dir

    def upload(self, local, target_dir=None):
        """
        上传文件

        :param local: 本地文件名
        """
        assert path.exists(local)
        remote = self.to_remote_path(path.basename(local))
        log.info('[Upload] {0} => {1}'.format(local, remote))
        self._client.upload(local, remote)

    def download(self, remote_file, store_path=None):
        """
        下载文件

        :param remote_file: 远程文件名, 例如`file_on_cloud.txt`
        :param store_path: 存储的文件名的绝对路径, 例如`/tmp/file_on_disk.txt`
        """
        remote_file = self.to_remote_path(remote_file)
        local_path = store_path or tempfile.mktemp(path.splitext(remote_file)[-1])
        log.info('[Download] {0} => {1}'.format(remote_file, local_path))
        self._client.download(remote_file, local_path)
        return local_path

    def formatted_ls(self):
        def flat(max_width):
            def _flat(f):
                return '{name: <{width}} {time: <{width}}'\
                    .format(name=path.basename(f.name), time=f.mtime, width=max_width)
            return _flat

        files = self.ls()
        col_width = max(len(f.name) for f in files) + 2
        return map(flat(col_width), files)

    def ls(self):
        return self._client.ls(self.working_dir)

    def cd(self, directory):
        self.working_dir = join('dav', directory)

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

    def to_remote_path(self, path):
        if self.working_dir not in path:
            return join(self.working_dir, path)
        return path

    def check_conn(self):
        assert bool(self._client.ls(self.working_dir))

    def search_latest(self, pattern):
        """
        根据pattern获取最新的文件
        """
        sorted_files = sorted(self.search(pattern), key=lambda f: dt_parse(f.mtime))
        return sorted_files[-1].name if sorted_files else None

    def download_latest_file(self):
        filename = self.search_latest('')
        return self.download(filename)

