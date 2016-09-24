#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Universal Resource Locator (URL).
"""

__all__ = ["BaseURL", "FolderURL", "URL", "SpiderURL"]

from . import Resource
from .domain import Domain
from .ip import IP
from ...libs.net.web_utils import parse_url
from ...utils.text_utils import to_utf8

from urllib import quote


#------------------------------------------------------------------------------
class _AbstractURL(Resource):
    """
    Abstract class for all URL based resources.
    """

    # Not true, but this bypasses an integrity check in the metaclass.
    data_subtype = "resource/abstract"


    #--------------------------------------------------------------------------
    def __init__(self, url):
        """
        :param url: Absolute URL.
        :type url: str

        :raises ValueError: Relative URLs are not allowed.
        """

        # Parse, verify and canonicalize the URL.
        # TODO: if relative, make it absolute using the referer when available.
        parsed = parse_url(url)
        if not parsed.host or not parsed.scheme:
            raise ValueError("Only absolute URLs must be used! Got: %r" % url)
        if parsed.scheme == "mailto":
            raise ValueError("For emails use the Email type instead! Got: %r" % url)
        if parsed.scheme not in ("http", "https", "ftp"):
            raise ValueError("URL scheme not supported: %r" % parsed.scheme)
        url = parsed.url

        # URL.
        self.__url = url

        # Parsed URL.
        self.__parsed_url = parsed

        # Parent constructor.
        super(_AbstractURL, self).__init__()


    #--------------------------------------------------------------------------

    @property
    def url(self):
        """
        :return: URL in canonical form.
        :rtype: str
        """
        return self.__url


    #--------------------------------------------------------------------------

    @property
    def parsed_url(self):
        """
        :return: URL in parsed form.
        :rtype: ParsedURL
        """
        return self.__parsed_url

    @property
    def hostname(self):
        """
        :return: Hostname this URL points to.
        :rtype: str
        """
        return self.parsed_url.hostname

    @property
    def path(self):
        """
        :return: Path component of the URL.
        :rtype: str
        """
        return self.parsed_url.path

    @property
    def is_https(self):
        """
        :return: True if it's HTTPS, False otherwise.
        :rtype: bool
        """
        return self.parsed_url.scheme == "https"


    #--------------------------------------------------------------------------
    def __str__(self):
        return self.url


    #--------------------------------------------------------------------------
    def __repr__(self):
        cls = self.__class__.__name__
        if "." in cls:
            cls = cls[ cls.rfind(".") + 1 : ]
        return "<%s url=%r>" % (cls, self.url)


#------------------------------------------------------------------------------
class URL(_AbstractURL):
    """
    Universal Resource Locator (URL).

    You can get the URL in canonical form:

    - url

    In deconstructed form:

    - parsed_url

    The current crawling depth level:

    - depth

    And some extra information needed to build an HTTP request:

    - method
    - url_params
    - post_params
    - referer
    """

    data_subtype = "url"


    #--------------------------------------------------------------------------
    def __init__(self, url, method = "GET", post_params = None, referer = None, urlencode = True, **kwargs):
        """
        :param url: Absolute URL.
        :type url: str

        :param method: HTTP method.
        :type method: str

        :param post_params: POST parameters or raw data.
        :type post_params: dict(str -> str) | str

        :param referer: Referrer URL.
        :type referer: str

        :param urlencode: POST|GET Data urlencode
        :type urlencode: bool

        :raises ValueError: Currently, relative URLs are not allowed.
        """

        # Validate the arguments.
        if method:
            method = to_utf8(method)
        else:
            method = "GET"
        if referer:
            referer = to_utf8(referer)
        else:
            referer = None
        if not isinstance(method, str):
            raise TypeError("Expected string, got %r instead" % type(method))
        if post_params is not None and not isinstance(post_params, dict):
            raise TypeError("Expected dict, got %r instead" % type(post_params))
        if referer is not None and not isinstance(referer, str):
            raise TypeError("Expected string, got %r instead" % type(referer))
        if post_params:
            if hasattr(post_params, "iteritems"):
                post_params = {
                    to_utf8(k): to_utf8(v) for k,v in post_params.iteritems()
                }
                if urlencode:
                    post_data = '&'.join(
                        '%s=%s' % ( quote(k, safe=''), quote(v, safe='') )
                        for (k, v) in sorted(post_params.iteritems())
                    )
                else:
                    post_data = '&'.join(
                        '%s=%s' % ( k, v ) for (k, v) in sorted(post_params.iteritems())
                    )
            else:
                post_data   = to_utf8(post_params)
                post_params = None
        else:
            post_data   = None
            post_params = None

            '''
            # Checks for get param
            url_params = kwargs.get('url_params', None)

            if url_params is not None:
                if hasattr(url_params, "iteritems"):
                    url_params = {
                        to_utf8(k): to_utf8(v) for k, v in url_params.iteritems()
                    }
                    query_param = '&'.join(
                        '%s=%s' % ( quote(k, safe=''), quote(v, safe='') )
                        for (k, v) in sorted(url_params.iteritems())
                    )
                    url = url + '?' + query_param
            '''

        #bug solved by blackye
        #solve get_param bug
        #http://www.baidu.com/index.php?id=1 POST: a=1
        # Checks for get param
        url_params = kwargs.get('url_params', None)

        if url_params is not None:
            if hasattr(url_params, "iteritems"):
                url_params = {
                    to_utf8(k): to_utf8(v) for k, v in url_params.iteritems()
                }
                if urlencode:
                     query_param = '&'.join(
                    '%s=%s' % ( quote(k, safe=''), quote(v, safe='') )
                    for (k, v) in sorted(url_params.iteritems()))
                else:
                    query_param = '&'.join(
                        '%s=%s' % ( k, v)
                        for (k, v) in sorted(url_params.iteritems())
                    )
                url = url + '?' + query_param
                if "sysdate" in query_param and "limit" in query_param:
                    print url, 'fuck!!'


        # Save the properties.
        self.__method      = method
        self.__post_data   = post_data
        self.__post_params = post_params
        self.__referer     = parse_url(referer).url if referer else None

        # Call the parent constructor.
        super(URL, self).__init__(url)


    #--------------------------------------------------------------------------
    def __repr__(self):
        s = "<URL url=%r, method=%r, params=%r, referer=%r>"
        s %= (self.url, self.method, self.post_params, self.referer)
        return s


    #--------------------------------------------------------------------------
    @property
    def display_name(self):
        return "URL"


    #--------------------------------------------------------------------------

    @property
    def method(self):
        """
        :return: HTTP method.
        :rtype: str
        """
        return self.__method

    @property
    def post_data(self):
        """
        :return: POST data.
        :rtype: str
        """
        return self.__post_data


    #--------------------------------------------------------------------------

    @property
    def url_params(self):
        """
        :return: GET parameters.
        :rtype: dict(str -> str)
        """
        query_params = self.parsed_url.query_params
        if query_params:
            return query_params
        return {}

    @property
    def has_url_params(self):
        """
        :return: True if there are GET parameters, False otherwise.
        :rtype: bool
        """
        return bool(self.url_params)

    @property
    def post_params(self):
        """
        :return: POST parameters.
        :rtype: dict(str -> str)
        """
        if self.__post_params:
            return self.__post_params.copy()
        return {}

    @property
    def has_post_params(self):
        """
        :return: True if there are POST parameters, False otherwise.
        :rtype: bool
        """
        return bool(self.post_params)

    @property
    def referer(self):
        """
        :return: Referer for this URL.
        :rtype: str
        """
        return self.__referer


    #--------------------------------------------------------------------------
    @property
    def discovered(self):
        if self.is_in_scope():
            result = FolderURL.from_url(self.url)
            result.append( BaseURL(self.url) )
            try:
                result.append( IP(self.hostname) )
            except ValueError:
                result.append( Domain(self.hostname) )
            return result
        return []


#------------------------------------------------------------------------------
class BaseURL(_AbstractURL):
    """
    Base URL.

    Unlike the URL type, which refers to any URL, this type is strictly for
    root level URLs in a web server. Plugins that only run once per web server
    should probably receive this data type.

    For example, a plugin receiving both BaseURL and URL may get this input:

    - BaseURL("http://www.example.com/")
    - URL("http://www.example.com/")
    - URL("http://www.example.com/index.php")
    - URL("http://www.example.com/admin.php")
    - URL("http://www.example.com/login.php")

    Notice how the root level URL is sent twice,
    once as BaseURL and again the more generic URL.
    """

    data_subtype = "base_url"


    #--------------------------------------------------------------------------
    def __init__(self, url):
        """
        :param url: Any **absolute** URL. The base will be extracted from it.
        :type url: str

        :raises ValueError: Only absolute URLs must be used.
        """

        # Parse, verify and canonicalize the URL.
        parsed = parse_url(url)
        if not parsed.host or not parsed.scheme:
            raise ValueError("Only absolute URLs must be used! Got: %r" % url)

        # Convert it into a base URL.
        parsed.auth = None
        parsed.path = "/"
        parsed.fragment = None
        parsed.query = None
        parsed.query_char = None
        url = parsed.url

        # Call the parent constructor.
        super(BaseURL, self).__init__(url)


    #--------------------------------------------------------------------------
    @property
    def display_name(self):
        return "Base URL"


    #--------------------------------------------------------------------------
    @property
    def discovered(self):
        if self.is_in_scope():
            try:
                return [IP(self.hostname)]
            except ValueError:
                return [Domain(self.hostname)]
        return []


#------------------------------------------------------------------------------
class FolderURL(_AbstractURL):
    """
    Folder URL.

    Unlike the URL type, which refers to an URL that's linked or somehow found
    to be valid, the FolderURL type refers to inferred URLs to folders detected
    within another URL.

    This makes it semantically different, since there's no guarantee that the
    URL actually points to a valid resource, nor that it belongs to the normal
    web access flow.

    For example, a plugin receiving both FolderURL and URL may get this input:

    - URL("http://www.example.com/wp-content/uploads/2013/06/attachment.pdf")
    - FolderURL("http://www.example.com/wp-content/uploads/2013/06/")
    - FolderURL("http://www.example.com/wp-content/uploads/2013/")
    - FolderURL("http://www.example.com/wp-content/uploads/")
    - FolderURL("http://www.example.com/wp-content/")

    Note that the folder URLs may or may not be sent again as an URL object.
    For example, for a site that has a link to the "incoming" directory in its
    index page, we may get something like this:

    - URL("http://www.example.com/index.html")
    - URL("http://www.example.com/incoming/")
    - FolderURL("http://www.example.com/incoming/")

    FolderURL objects are never sent for the root folder of a web site.
    For that, see the BaseURL data type.
    """

    data_subtype = "folder_url"


    #--------------------------------------------------------------------------
    def __init__(self, url):
        """
        :param url: Absolute URL to a folder.
        :type url: str

        :raises ValueError: The URL wasn't absolute or didn't point to a folder.
        """

        # Parse, verify and canonicalize the URL.
        parsed = parse_url(url)
        if not parsed.host or not parsed.scheme:
            raise ValueError("Only absolute URLs must be used! Got: %r" % url)
        if not parsed.path.endswith("/"):
            raise ValueError("URL does not point to a folder! Got: %r" % url)

        # Call the parent constructor.
        super(FolderURL, self).__init__(parsed.url)


    #--------------------------------------------------------------------------
    @staticmethod
    def from_url(url):
        """
        :param url: Any **absolute** URL. The folder will be extracted from it.
        :type url: str

        :returns: Inferred folder URLs.
        :rtype: list(FolderURL)

        :raises ValueError: Only absolute URLs must be used.
        """
        assert isinstance(url, basestring)

        # Parse, verify and canonicalize the URL.
        parsed = parse_url(url)
        if not parsed.host or not parsed.scheme:
            raise ValueError("Only absolute URLs must be used! Got: %r" % url)

        # Extract the folders from the path.
        path = parsed.path
        folders = path.split("/")
        if not path.endswith("/"):
            folders.pop()

        # Convert the URL to a base URL.
        parsed.auth = None
        parsed.path = "/"
        parsed.fragment = None
        parsed.query = None
        parsed.query_char = None

        # Generate a new folder URL for each folder.
        folder_urls = {parsed.url}
        for folder in folders:
            if folder:
                parsed.path += folder + "/"
                folder_urls.add(parsed.url)

        # Return the generated URLs.
        return [FolderURL(x) for x in folder_urls]


    #--------------------------------------------------------------------------
    @property
    def display_name(self):
        return "Folder URL"


    #--------------------------------------------------------------------------
    @property
    def discovered(self):
        if self.is_in_scope():
            result = [ BaseURL(self.url) ]
            try:
                result.append( IP(self.hostname) )
            except ValueError:
                result.append( Domain(self.hostname) )
            return result
        return []


#------------------------------------------------------------------------------
class SpiderURL(_AbstractURL):
    """
    Spider URL.

    Unlike the URL type, which refers to any URL, this type is strictly for
    root level URLs in a web server. Plugins that only run once per web server
    should probably receive this data type.

    For example, a plugin receiving both BaseURL and URL may get this input:

    - BaseURL("http://www.example.com/")
    - URL("http://www.example.com/")
    - URL("http://www.example.com/index.php")
    - URL("http://www.example.com/admin.php")
    - URL("http://www.example.com/login.php")

    Notice how the root level URL is sent twice,
    once as BaseURL and again the more generic URL.
    """

    data_subtype = "spider_url"


    #--------------------------------------------------------------------------
    def __init__(self, url):
        """
        :param url: Any **absolute** URL. The base will be extracted from it.
        :type url: str

        :raises ValueError: Only absolute URLs must be used.
        """
        # Call the parent constructor.
        super(SpiderURL, self).__init__(url)


    #--------------------------------------------------------------------------
    @property
    def display_name(self):
        return "Spider URL"


    #--------------------------------------------------------------------------
    @property
    def discovered(self):
        if self.is_in_scope():
            try:
                return [IP(self.hostname)]
            except ValueError:
                return [Domain(self.hostname)]
        return []