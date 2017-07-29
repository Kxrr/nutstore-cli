# coding: utf-8
import re
import tempfile
import logging
from contextlib import contextmanager
from os import path as p

from nutstore_cli.client.utils import dir_join, check_local_path

import easywebdav

log = logging.getLogger('webdav')


class BaseNutStoreClient(object):
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

    @check_local_path
    def upload(self, local_path, cloud_dir=None):
        """Upload a local file to the cloud(with the same filename)"""
        cloud_path = cloud_dir or self.to_cloud_path(p.basename(local_path))
        log.info('[Upload] {0} => {1}'.format(local_path, cloud_path))
        self._client.upload(local_path, cloud_path)

    @check_local_path
    def download(self, cloud_path, local_path=None):
        """Download a cloud file to your machine."""
        cloud_path = self.to_cloud_path(cloud_path)
        local_path = local_path or tempfile.mktemp(p.splitext(cloud_path)[-1])
        log.info('[Download] {0} => {1}'.format(cloud_path, local_path))
        self._client.download(cloud_path, local_path)
        return local_path

    def ls(self):
        return self._client.ls(self._working_dir)

    def cd(self, directory):
        self.working_dir = dir_join(self.working_dir, directory)

    def rm(self, cloud_path):
        """Remove a file on the cloud."""
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
        return filter(
            lambda f: (re.search(pattern=pattern, string=f.name, flags=re.IGNORECASE) and f.size != 0), files
        )

    def to_cloud_path(self, path):
        if not re.search('^/?dav.*', path):
            return '/dav' + dir_join(self.working_dir, path)
        return path

    def check_conn(self):
        self.ls()
        return True
