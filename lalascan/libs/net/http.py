#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
HTTP protocol API for GoLismero.
"""

__all__ = ["HTTP"]

from lalascan.api.exception import LalascanNetworkException, LalascanNetworkOutOfScope
from .web_utils import detect_auth_method, get_auth_obj
from ...data.http import HTTP_Request, HTTP_Response, HTTP_Raw_Request
from ...data.resource.url import URL
from ..core.common import Singleton
from ...libs.core.globaldata import conf

from hashlib import md5
from os import environ
from os.path import join
from requests import Session
from requests.cookies import cookiejar_from_dict
from requests.exceptions import RequestException
from socket import socket, error, getaddrinfo, SOCK_STREAM
from ssl import wrap_socket
from StringIO import StringIO
from time import time


#------------------------------------------------------------------------------
class _HTTP(Singleton):
    """
    HTTP protocol API for GoLismero.
    """


    #--------------------------------------------------------------------------
    def __init__(self):
        self.__session = None


    #--------------------------------------------------------------------------
    def _initialize(self):
        """
        .. http request init
        """

        # Start a new session.
        self.__session = Session()

        # Load the proxy settings.
        if conf is not None and conf.has_key('proxy_addr') and conf.has_key('proxy_port'):
            proxy_addr = conf.proxy_addr
            if proxy_addr:
                proxy_port = conf.proxy_port
                if proxy_port:
                    proxy_addr = "%s:%s" % (proxy_addr, proxy_port)

                '''
                auth_user = Config.audit_config.proxy_user
                auth_pass = Config.audit_config.proxy_pass
                auth, _ = detect_auth_method(proxy_addr)
                self.__session.auth = get_auth_obj(auth, auth_user, auth_pass)
                '''
                self.__session.proxies = {
                    "http":  proxy_addr,
                    "https": proxy_addr,
                    "ftp":   proxy_addr,
                }

        # Load the cookies.
        if conf is not None and conf.has_key('cookie'):
            cookie = conf.cookie
            if cookie:
                self.__session.cookies = cookiejar_from_dict(cookie)

        # Set User Agent
        if conf is not None and conf.has_key('user_agent'):
            self.__user_agent = conf.user_agent


    #--------------------------------------------------------------------------
    def _finalize(self):
        '''
        clean session headers
        :return:
        '''

        self.__session = None


    #--------------------------------------------------------------------------
    def get_url(self, url, method = "GET", callback = None, timeout = 10.0, allow_redirects = True):
        """
        Send a simple HTTP request to the server and get the response back.

        :param url: URL to request.
        :type url: str

        :param method: HTTP method.
        :type method: str

        :param callback: Callback function.
        :type callback: callable

        :param timeout: Timeout in seconds.
            The minimum value is 0.5 and the maximum is 100.0. Any other values
            will be silently converted to either one of them.
        :type timeout: int | float

        :param allow_redirects: True to follow redirections, False otherwise.
        :type allow_redirects: bool

        :returns: HTTP response, or None if the request was cancelled.
        :rtype: HTTP_Response | None

        :raises NetworkOutOfScope: The resource is out of the audit scope.
            Note that this can happen even if the URL has been checked against
            Config.audit_scope -- if the server responds with a
            redirection against another URL that's out of scope.
        :raises NetworkException: A network error occurred.
        """
        request = HTTP_Request(url, method = method, user_agent=self.__user_agent)
        return self.make_request(request, callback = callback, timeout = timeout, allow_redirects = allow_redirects)


    #--------------------------------------------------------------------------
    def make_request(self, request, callback = None, timeout = 10.0, allow_redirects = True):
        """
        Send an HTTP request to the server and get the response back.

        :param request: HTTP request to send.
        :type request: HTTP_Request

        :param callback: Callback function.
        :type callback: callable

        :param timeout: Timeout in seconds.
            The minimum value is 0.5 and the maximum is 100.0. Any other values
            will be silently converted to either one of them.
        :type timeout: int | float

        :param allow_redirects: True to follow redirections, False otherwise.
        :type allow_redirects: bool

        :returns: HTTP response, or None if the request was cancelled.
        :rtype: HTTP_Response | None

        :raises NetworkOutOfScope: The resource is out of the audit scope.
        :raises NetworkException: A network error occurred.
        """

        # Check initialization.
        if self.__session is None:
            self._initialize()

        # Check the arguments.
        if not isinstance(request, HTTP_Request):
            raise TypeError("Expected HTTP_Request, got %r instead" % type(request))
        if callback is not None and not callable(callback):
            raise TypeError(
                "Expected callable (function, class, instance with __call__),"
                " got %r instead" % type(callback)
            )

        # Sanitize the timeout value.
        if timeout:
            timeout = float(timeout)
            if timeout > 100.0:
                timeout = 100.0
            elif timeout < 0.5:
                timeout = 0.5
        else:
            timeout = 0.5


        # Filter the Host header to work around a Requests quirk.
        headers = request.headers.to_dict()
        try:
            del headers['host']
        except KeyError:
            pass

        # Send the request.
        try:
            t1 = time()
            resp = self.__session.request(
                method  = request.method,
                url     = request.url,
                headers = headers,
                data    = request.post_data,
                ##files   = request.files,   # not supported yet!
                verify  = False,
                stream  = True,
                timeout = timeout,
                allow_redirects = allow_redirects,
            )
            t2 = time()
        except RequestException, e:
            #print str(e)
            raise LalascanNetworkException(str(e))

        try:
            # Get the response properties.
            url = resp.url
            status_code  = str(resp.status_code)
            content_type = resp.headers.get("Content-Type")
            try:
                content_length = int(resp.headers["Content-Length"])
            except Exception:
                content_length = None

            # If the final URL is different from the request URL,
            # abort if the new URL is out of scope.
            if url != request.url:
                raise LalascanNetworkOutOfScope("URL out of scope: %s" % url)

            # Call the user-defined callback, and cancel if requested.
            if callback is not None:
                cont = callback(request, url, status_code, content_length, content_type)
                if not cont:
                    return

            # Autogenerate an URL object.
            # XXX FIXME: the depth level is broken!!!
            url_obj = None
            if url != request.url:
                url_obj = URL(
                    url         = url,
                    method      = request.method,
                    post_params = request.post_data,
                    referer     = request.referer,
                )

            # Download the contents.
            try:
                t3 = time()
                data = resp.content
                t4 = time()
            except RequestException, e:
                raise LalascanNetworkException(str(e))

            # Calculate the elapsed time.
            elapsed = (t2 - t1) + (t4 - t3)

            # Build an HTTP_Response object.
            # Since the requests library won't let us access the raw
            # response bytes, we have to "reconstruct" them.
            response = HTTP_Response(
                request = request,
                status  = status_code,
                headers = resp.headers,
                data    = data,
                elapsed = elapsed,
            )

            # Link it to the originating URL.
            #if url_obj is not None:
            #    response.add_resource(url_obj)


            # Return the HTTP_Response object.
            return response

        finally:

            # Close the connection.
            resp.close()


    #--------------------------------------------------------------------------
    def make_raw_request(self, raw_request, host, port = 80, proto = "http",
                 callback = None, timeout = 10.0):
        """
        Send a raw HTTP request to the server and get the response back.

        .. note: This method does not support the use of the cache or a proxy.

        .. warning::
           This method only returns the HTTP response headers, **NOT THE CONTENT**.

        :param raw_request: Raw HTTP request to send.
        :type raw_request: HTTP_Raw_Request

        :param host: Hostname or IP address to connect to.
        :type host: str

        :param port: TCP port to connect to.
        :type port: int

        :param proto: Network protocol (that is, the URL scheme).
        :type proto: str

        :param callback: Callback function.
        :type callback: callable

        :param timeout: Timeout in seconds.
            The minimum value is 0.5 and the maximum is 100.0. Any other values
            will be silently converted to either one of them.
        :type timeout: int | float

        :param use_cache: Control the use of the cache.
                          Use True to force the use of the cache,
                          False to force not to use it,
                          or None for automatic.
        :type use_cache: bool | None

        :returns: HTTP response, or None if the request was cancelled.
        :rtype: HTTP_Response | None

        :raises NetworkOutOfScope: The resource is out of the audit scope.
        :raises NetworkException: A network error occurred.
        """

        # Abort if a proxy is configured, because we don't support this yet.
        if conf.audit_config.proxy_addr:
            raise NotImplementedError("Proxy not yet supported")

        # Check the arguments.
        if type(raw_request) is str:
            raw_request = HTTP_Raw_Request(raw_request)
        elif not isinstance(raw_request, HTTP_Raw_Request):
            raise TypeError("Expected HTTP_Raw_Request, got %r instead" % type(raw_request))
        if type(host) == unicode:
            raise NotImplementedError("Unicode hostnames not yet supported")
        if type(host) != str:
            raise TypeError("Expected str, got %r instead" % type(host))
        if proto not in ("http", "https"):
            raise ValueError("Protocol must be 'http' or 'https', not %r" % proto)
        if port is None:
            if proto == "http":
                port = 80
            elif proto == "https":
                port = 443
            else:
                assert False, "internal error!"
        elif type(port) not in (int, long):
            raise TypeError("Expected int, got %r instead" % type(port))
        if port < 1 or port > 32767:
            raise ValueError("Invalid port number: %d" % port)
        if callback is not None and not callable(callback):
            raise TypeError(
                "Expected callable (function, class, instance with __call__),"
                " got %r instead" % type(callback)
            )


        # Sanitize the timeout value.
        if timeout:
            timeout = float(timeout)
            if timeout > 100.0:
                timeout = 100.0
            elif timeout < 0.5:
                timeout = 0.5
        else:
            timeout = 0.5

        # Resolve the hostname.
        # FIXME: we're only using the first item, but we could use more
        #        than one, for example iterate through them if they fail.
        family, socktype, proto, canonname, sockaddr = \
            getaddrinfo(host, port, 0, SOCK_STREAM)[0]

        # Start the timer.
        t1 = time()

        try:
            s = socket(family, socktype, proto)
            try:
                s.settimeout(timeout)
                s.connect(sockaddr)
                try:
                    if proto == "https":
                        s = wrap_socket(s)

                    # Send the HTTP request.
                    s.sendall(raw_request.raw_request)

                    # Get the HTTP response headers.
                    raw_response = StringIO()
                    while True:
                        data = s.recv(1)
                        if not data:
                            raise LalascanNetworkException(
                                "Server has closed the connection")
                        raw_response.write(data)
                        if raw_response.getvalue().endswith("\r\n\r\n"):
                            break   # full HTTP headers received
                        if len(raw_response.getvalue()) > 65536:
                            raise LalascanNetworkException(
                                "Response headers too long")

                    # Stop the timer.
                    t2 = time()

                    # Call the user-defined callback,
                    # and cancel if requested.
                    if callback is not None:
                        temp_request  = HTTP_Raw_Request(
                            raw_request.raw_request)
                        temp_response = HTTP_Response(
                            temp_request,
                            raw_response = raw_response.getvalue()
                        )
                        cont = callback(temp_request, temp_response)
                        if not cont:
                            return
                        del temp_request
                        del temp_response

                    # Start the timer.
                    t3 = time()

                    # Download the contents.
                    #
                    #
                    #
                    # XXX TODO
                    #
                    #
                    #

                    # Stop the timer.
                    t4 = time()

                    # Return the HTTP_Response object.
                    return HTTP_Response(
                        request      = raw_request,
                        raw_response = raw_response.getvalue(),
                        elapsed      = (t2 - t1) + (t4 - t3),
                    )

                # Close the connection and clean up the socket.
                finally:
                    try:
                        s.shutdown(2)
                    except Exception:
                        pass
            finally:
                try:
                    s.close()
                except Exception:
                    pass

        # On socket errors, send an exception.
        except error, e:
            raise LalascanNetworkException(str(e))


#------------------------------------------------------------------------------

# Singleton pattern.
HTTP = _HTTP()
