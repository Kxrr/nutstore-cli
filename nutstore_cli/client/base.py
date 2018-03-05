# coding: utf-8
import re
import tempfile
from contextlib import contextmanager

from nutstore_cli.utils import output
from nutstore_cli.client.utils import check_local_path
from nutstore_cli.client.path_helper import *

import easywebdav


class BaseNutStoreClient(object):
    """坚果云"""

    api = 'dav.jianguoyun.com'

    def __init__(self, username, password, working_dir, check_conn=True):
        if not working_dir.startswith('/'):
            working_dir = '/' + working_dir
        self.username = username
        self.np = PathHelper(start=working_dir)
        self._client = easywebdav.connect(self.api, username=username, password=password)
        if check_conn:
            self.check_conn()

    @property
    def cwd(self):
        """Current working directory for display"""
        return self.np.pretty

    @check_local_path
    def upload(self, local_path, remote_dir=None):
        """Upload a local file to the remote(with the same filename)"""
        name = basename(local_path)
        directory = remote_dir or self.cwd
        remote_path = join(directory, name)
        output.debug('[UPLOAD] {0} => {1}'.format(local_path, remote_path))
        self._client.upload(local_path, self._to_real_path(remote_path))
        return remote_path

    def download(self, remote_path, local_path=None):
        """Download a remote file to your machine."""
        local_path = local_path or tempfile.mktemp(suffix=splitext(remote_path)[-1])
        output.debug('[DOWNLOAD] {0} => {1}'.format(remote_path, local_path))
        self._client.download(self._to_real_path(remote_path), local_path)
        return local_path

    def ls(self):
        """
        :rtype: list[easywebdav.client.File]
        """
        def file_in_dir(filename, directory):
            return (directory in filename) and (filename != directory)

        real_path = self.np.real
        output.debug('List "{}"'.format(real_path))
        return filter(lambda f: file_in_dir(f.name, real_path), self._client.ls(real_path))

    def cd(self, directory):
        self.np.cd(directory)
        output.debug('Change directory to "{}"'.format(self.np.real))

    def rm(self, remote_path):
        """Remove a file on the remote."""
        output.debug('[DELETE] {0}'.format(remote_path))
        self._client.delete(self._to_real_path(remote_path))
        return remote_path

    def mkdir(self, directory):
        return self._client.mkdir(self._to_real_path(directory))

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

    def _to_real_path(self, path):
        """Turn remote path(like /photos) into a real path on server"""
        return self.np.to_real(path)

    def check_conn(self):
        self.ls()
        return True
