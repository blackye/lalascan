#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'


from . import Fingerprint
from ...utils.text_utils import to_utf8

#------------------------------------------------------------------------------
class WebServiceFingerprint(Fingerprint):
    """
    Fingerprint information for a particular host and web server.
    """

    data_subtype = "webservice"


    #--------------------------------------------------------------------------
    def __init__(self, name, version, banner, canonical_name, related = None, others = None):
        """
        :param name: Web server name. Example: "Apache".
        :type name: str

        :param version: Web server version. Example: "2.2.23".
        :type version: str

        :param banner: Web server banner. Example:
            "Apache 2.2.23 ((Unix) mod_ssl/2.2.23 OpenSSL/1.0.1e-fips)".
        :type banner: str

        :param canonical_name: Web server name, in lowercase.
            The name will be one of the file:
            'wordlist/fingerprint/webservers_keywords.txt'.
            Example: "apache".
        :type canonical_name: str

        :param related: Alternative brands for this web server.
        :type related: set(str)

        :param others: Map of other possible web servers by name and their probabilities of being correct [0.0 ~ 1.0].
        :type others: dict( str -> float )
        """

        # Sanitize the strings.
        name           = to_utf8(name)
        version        = to_utf8(version)
        banner         = to_utf8(banner)
        canonical_name = to_utf8(canonical_name)

        # Check the data types.
        if not isinstance(name, str):
            raise TypeError("Expected str, got %r instead" % type(name))
        if not isinstance(version, str):
            raise TypeError("Expected str, got %r instead" % type(version))
        if not isinstance(banner, str):
            raise TypeError("Expected str, got %r instead" % type(banner))
        if not isinstance(canonical_name, str):
            raise TypeError("Expected str, got %r instead" % type(canonical_name))

        # Save the identity properties.
        self.__name           = name
        self.__version        = version
        self.__banner         = banner
        self.__canonical_name = canonical_name

        # Save the mergeable properties.
        self.related          = related
        self.others           = others

        # Parent constructor.
        super(WebServiceFingerprint, self).__init__()


    #--------------------------------------------------------------------------
    def __repr__(self):
        return "<WebServerFingerprint server='%s-%s' banner='%s'>" % (
            self.__name,
            self.__version,
            self.__banner,
        )


    #--------------------------------------------------------------------------
    def __str__(self):
        return self.__banner


    #--------------------------------------------------------------------------
    def to_dict(self):
        d = super(WebServiceFingerprint, self).to_dict()
        d["others"] = { k: list(v) for (k,v) in self.others.iteritems() }
        return d


    #--------------------------------------------------------------------------
    @property
    def display_properties(self):
        others = []
        for k in sorted(self.others.iterkeys()):
            others.append("%s:" % k)
            for v in sorted(self.others[k]):
                others.append("  %s" % v)
        props = super(WebServiceFingerprint, self).display_properties
        props["[DEFAULT]"]["Others"] = "\n".join(others)
        return props


    #--------------------------------------------------------------------------
    @identity
    def name(self):
        """
        :return: Web server name. Example: "Apache".
        :rtype: str
        """
        return self.__name


    #--------------------------------------------------------------------------
    @identity
    def version(self):
        """
        :return: Web server version. Example: "2.2.3".
        :rtype: str
        """
        return self.__version


    #--------------------------------------------------------------------------
    @identity
    def banner(self):
        """
        :return: Web server banner. Example:
            "Apache 2.2.23 ((Unix) mod_ssl/2.2.23 OpenSSL/1.0.1e-fips)".
        :rtype: str
        """
        return self.__banner


    #--------------------------------------------------------------------------
    @identity
    def canonical_name(self):
        """
        :return: Web server name, in lowercase.
            The full list of names is taken from the file:
            'wordlist/fingerprint/webservers_keywords.txt'.
            Example: "apache".
        :rtype: str
        """
        return self.__canonical_name


    #--------------------------------------------------------------------------
    @merge
    def others(self):
        """
        :return: Map of other possible web servers by name and their
            probabilities of being correct [0.0 ~ 1.0].
        :rtype: dict( str -> float )
        """
        return self.__others


    #--------------------------------------------------------------------------
    @others.setter
    def others(self, others):
        """
        :param others: Map of other possible web servers by name and their
            probabilities of being correct [0.0 ~ 1.0].
        :type others: dict( str -> float )
        """
        if others:
            if not isinstance(others, dict):
                raise TypeError("Expected dict, got %r instead" % type(others))
            others = {
                to_utf8(k): float(v)
                for k,v in others.iteritems()
            }
            for k in others.iterkeys():
                if not isinstance(k, str):
                    raise TypeError("Expected str, got %r instead" % type(k))
        else:
            others = {}
        self.__others = others


    #--------------------------------------------------------------------------
    @merge
    def related(self):
        """
        :return: Alternative brands for this web server.
        :rtype: set(str)
        """
        return self.__related


    #--------------------------------------------------------------------------
    @related.setter
    def related(self, related):
        """
        :param related: Alternative brands for this web server.
        :type related: set(str)
        """
        if related:
            if not isinstance(related, set):
                raise TypeError("Expected set, got %r instead" % type(related))
            related = { to_utf8(v) for v in related }
            for v in related:
                if not isinstance(v, str):
                    raise TypeError("Expected str, got %r instead" % type(v))
        else:
            related = {}
        self.__related = related
