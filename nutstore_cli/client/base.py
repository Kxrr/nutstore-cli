# coding: utf-8
import re
import tempfile
import logging
from contextlib import contextmanager

from nutstore_cli.client.utils import check_local_path
from nutstore_cli.client.road import *

import easywebdav

log = logging.getLogger('webdav')


class BaseNutStoreClient(object):
    """坚果云"""

    api = 'dav.jianguoyun.com'

    def __init__(self, username, password, working_dir, check_conn=True):
        self.np = NutPath()
        self.cd('/' + working_dir.split('/', 1)[-1])
        self._client = easywebdav.connect(self.api, username=username, password=password)

        if check_conn:
            self.check_conn()

    @property
    def cwd(self):
        """Current working directory for display"""
        return self.np.dummy_path

    @check_local_path
    def upload(self, local_path, remote_dir=None):
        """Upload a local file to the remote(with the same filename)"""
        name = basename(local_path)
        directory = remote_dir or self.cwd
        remote_path = join(directory, name)
        log.info('[UPLOAD] {0} => {1}'.format(local_path, remote_path))
        self._client.upload(local_path, self.to_server_path(remote_path))
        return remote_path

    @check_local_path
    def download(self, remote_path, local_path=None):
        """Download a remote file to your machine."""
        local_path = local_path or tempfile.mktemp(suffix=splitext(remote_path)[-1])
        log.info('[DOWNLOAD] {0} => {1}'.format(remote_path, local_path))
        self._client.download(self.to_server_path(remote_path), local_path)
        return local_path

    def ls(self):
        return self._client.ls(self.np.real_path)

    def cd(self, directory):
        self.np.set_dummy_path(directory)

    def rm(self, remote_path):
        """Remove a file on the remote."""
        log.info('[DELETE] {0}'.format(remote_path))
        self._client.delete(self.to_server_path(remote_path))
        return remote_path

    def mkdir(self, directory):
        return self._client.mkdir(self.to_server_path(directory))

    @contextmanager
    def cd_context(self, directory):
        saved = self.cwd
        self.cd(directory)
        yield
        self.cd(saved)

    def search(self, pattern):
        files = self.ls()
        return filter(
            lambda f: (re.search(pattern=pattern, string=f.name, flags=re.IGNORECASE) and f.size != 0), files
        )

    def to_server_path(self, path):
        """Turn remote path(like /photos) into a real path on server"""
        return self.np.to_real_path(path)

    def check_conn(self):
        self.ls()
        return True
