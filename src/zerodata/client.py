# No Copyright (-) 2010 The Ampify Authors. This file is under the
# Public Domain license that can be found in the root LICENSE file.

"""Ampify Zerodata Client."""

from os.path import dirname, join as join_path, realpath

from urllib2 import (
    HTTPHandler, HTTPSHandler, ProxyHandler, UnknownHandler,
    HTTPDefaultErrorHandler, HTTPRedirectHandler, HTTPErrorProcessor,
    URLError, build_opener, install_opener, urlopen
    )

from simplejson import dumps as json_encode, loads as json_decode

# ------------------------------------------------------------------------------
# extend sys.path
# ------------------------------------------------------------------------------

ZERODATA_ROOT = dirname(realpath(__file__))
AMPIFY_ROOT = dirname(dirname(ZERODATA_ROOT))

sys.path.insert(0, join_path(AMPIFY_ROOT, 'environ'))

import rconsole

# ------------------------------------------------------------------------------
# some konstants
# ------------------------------------------------------------------------------

API_OPERATIONS = ['get', 'delete', 'invalidate', 'put', 'query']
PRODUCTION_ENDPOINT = "http://ampifyit.appspot.com/"
TEST_ENDPOINT = "http://localhost:8080/"
ENDPOINT_MESSAGE = "This is the API endpoint of the Ampify ZeroDataStore."

class ZeroDataClient(object)
    """Provides a client for ZeroDataStore"""

    def __init__(self):
        self._endpoint = TEST_ENDPOINT
        # Create an OpenerDirector with support for SSL and other stuff...
        opener = self.build_opener(debug=True) 
        # ...and install it globally so it can be used with urlopen. 
        install_opener(opener) 
        try:
            response = urlopen(self._endpoint)
        except URLError:
            raise RuntimeError("API endpoint not available")
        content = response.read()

    def build_opener(self, debug=False):
        """Create handlers with the appropriate debug level.  
        We intentionally create new ones because the OpenerDirector 
        class in urllib2 is smart enough to replace its internal 
        versions with ours if we pass them into the 
        urllib2.build_opener method.  This is much easier than 
        trying to introspect into the OpenerDirector to find the 
        existing handlers.
        Based on http://code.activestate.com/recipes/440574/#c1

        TODO: Implement workaround for http://bugs.python.org/issue7152
        """
        http_handler = HTTPHandler(debuglevel=debug)
        https_handler = HTTPSHandler(debuglevel=debug)
        proxy_handler = ProxyHandler(debuglevel=debug)
        unknown_handler = UnknownHandler(debuglevel=debug)
        http_default_error_handler = HTTPDefaultErrorHandler(debuglevel=debug)
        http_redirect_handler = HTTPRedirectHandler(debuglevel=debug)
        http_error_processor = HTTPErrorProcessor(debuglevel=debug)

        handlers = [http_handler, https_handler, proxy_handler, \
                    unknown_handler, http_default_error_handler, \
                    http_redirect_handler, http_error_processor]
        opener = build_opener(handlers)

        return opener

    def call(self, api_operation, api_request):
        try:
            API_OPERATIONS.index(api_operation)
        except ValueError:
            raise RuntimeError("Invalid API operation.")
        url = "%s/%s" % (self._endpoint, api_operation)
        req = http_request(url)
        json_request = json_encode(api_request)
        try:
            response = urlopen(req, json_request)
        except URLError:
            raise RuntimeError("API request failed.")
        return json_decode(response.read())

