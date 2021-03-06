from __future__ import print_function

import os
import socket
import logging

import pytest

from six.moves import http_client
from six.moves.urllib.request import urlopen
from six.moves.urllib.error import URLError

from .base import TestServer

log = logging.getLogger(__name__)


@pytest.yield_fixture
def simple_http_test_server():
    with SimpleHTTPTestServer() as s:
        s.start()
        yield s


class HTTPTestServer(TestServer):

    def __init__(self, uri=None, **kwargs):
        self._uri = uri
        super(HTTPTestServer, self).__init__(**kwargs)

    @property
    def uri(self):
        if self._uri:
            return self._uri
        return "http://%s:%s" % (self.hostname, self.port)

    def check_server_up(self):
        """ Check the server is up by polling self.uri
        """
        try:
            log.debug('accessing URL:', self.uri)
            url = urlopen(self.uri)
            return url.getcode() == 200
        except (URLError, socket.error, http_client.BadStatusLine) as e:
            if getattr(e, 'code', None) == 403:
                # This is OK, the server is probably running in secure mode
                return True

            log.debug("Server not up yet (%s).." % e)
            return False


class SimpleHTTPTestServer(HTTPTestServer):
    """A Simple HTTP test server that serves up a folder of files over the web."""

    def __init__(self, workspace=None, delete=None, **kwargs):
        kwargs.pop("hostname", None)  # User can't set the hostname it is always 0.0.0.0
        # If we don't pass hostname="0.0.0.0" to our superclass's initialiser then the cleanup
        # code in kill won't work correctly. We don't set self.hostname however as we want our
        # uri property to still be correct.
        super(SimpleHTTPTestServer, self).__init__(workspace=workspace, delete=delete, hostname="0.0.0.0", **kwargs)
        self.cwd = self.file_dir

    @property
    def uri(self):
        if self._uri:
            return self._uri
        return "http://%s:%s" % (socket.gethostname(), self.port)

    @property
    def run_cmd(self):
        return ["python", "-m", "SimpleHTTPServer", str(self.port)]

    @property
    def file_dir(self):
        """This is the folder of files served up by this SimpleHTTPServer"""
        file_dir = os.path.join(str(self.workspace), "files")
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        return file_dir
