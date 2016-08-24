#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

__all__ = ["AuditScope"]

from lalascan.libs.net.web_utils import ParsedURL
from lalascan.data.resource.ip import IP
from lalascan.data.resource.domain import Domain
from lalascan.data.resource.url import URL, SpiderURL
from lalascan.api.exception import LalascanNotImplementedError

import re
from netaddr import IPNetwork, IPAddress

class AbstractScope(object):
    '''
    abstract scope base class
    '''
    def __init__(self):
        raise LalascanNotImplementedError()

    @property
    def addresses(self):
        raise LalascanNotImplementedError()

    @property
    def domains(self):
        raise LalascanNotImplementedError()

    @property
    def target_url(self):
        raise LalascanNotImplementedError()

    def add_target(self):

        raise LalascanNotImplementedError()

    def get_target(self):

        raise LalascanNotImplementedError()

    def __str__(self):
        return "<%s>" % self

    def __contains__(self, target):
        raise LalascanNotImplementedError()

    def get_targets(self):
        """
        Get the audit targets as Data objects.

        :returns: Data objects.
        :rtype: list(Data)
        """
        result = []
        result.extend( IP(address) for address in self.addresses )
        result.extend( Domain(domain) for domain in self.domains )
        result.extend( Domain(root) for root in self.roots )
        result.extend( URL(url) for url in self.web_pages )
        #----------ADD By BlackYe
        result.extend( SpiderURL(url) for url in self.target_url)
        return result

class AuditScope(AbstractScope):

    _re_is_domain = re.compile(r"^[A-Za-z0-9][A-Za-z0-9\_\-\.]*[A-Za-z0-9]$")

    def __init__(self):
        self.__domains   = set()   # Domain names.
        self.__roots     = set()   # Domain names for subdomain matching.
        self.__addresses = set()   # IP addresses.
        self.__web_pages = set()   # URLs.
        self.__target_url = set()

    #--------------------------------------------------------------------------
    @property
    def addresses(self):
        return sorted(self.__addresses)


    #--------------------------------------------------------------------------
    @property
    def domains(self):
        return sorted(self.__domains)


    #--------------------------------------------------------------------------
    @property
    def roots(self):
        return sorted(self.__roots)


    #--------------------------------------------------------------------------
    @property
    def web_pages(self):
        return sorted(self.__web_pages)


    # Add By BlackYe.
    #--------------------------------------------------------------------------
    @property
    def target_url(self):
        return sorted(self.__target_url)


    def add_target(self, target):

        try:
            IP(target)
            address = target
        except Exception:
            address = None
        if address is not None:
            # Keep the IP address.
            self.__addresses.add(address)
            # If it's an IP network...
        else:
            try:
                network = IPNetwork(target)
            except Exception:
                ##raise  # XXX DEBUG
                network = None
            if network is not None:
                # For each host IP address in range...
                for address in network.iter_hosts():
                    address = str(address)
                    # Keep the IP address.
                    self.__addresses.add(address)

            #domain
            elif self._re_is_domain.match(target):
                target = target.lower()
                if target not in self.__domains:
                    # Keep the domain name.
                    self.__domains.add(target)
            else:
                try:
                    parsed_url = ParsedURL(target)
                    url = parsed_url.url
                except Exception:
                    url = None
                if url is not None:
                    self.__web_pages.add(url)
                    self.__target_url.add(url)
                    host = parsed_url.host
                    try:
                        if host.startswith("[") and host.endswith("]"):
                            IPAddress(host[1:-1], version=6)
                            host = host[1:-1]
                        else:
                            IPAddress(host)
                        self.__addresses.add(host)
                    except Exception:
                        ##raise  # XXX DEBUG
                        host = host.lower()
                        if host not in self.__domains:
                            self.__domains.add(host)
                else:
                    raise ValueError("I don't know what to do with this: %s" % target)


     #--------------------------------------------------------------------------
    def __str__(self):
        result = ["Audit scope:\n"]
        addresses = self.addresses
        if addresses:
            result.append("\nIP addresses:\n")
            for address in addresses:
                result.append("    %s\n" % address)
        domains = ["*." + domain for domain in self.roots]
        domains.extend(self.domains)
        if domains:
            result.append("\nDomains:\n")
            for domain in domains:
                result.append("    %s\n" % domain)
        web_pages = self.web_pages
        if web_pages:
            result.append("\nWeb pages:\n")
            for url in web_pages:
                result.append("    %s\n" % url)
        return "".join(result)



class DummyScope (AbstractScope):
    """
    Dummy scope tells you everything is in scope, all the time.
    """

    def __init__(self):
        pass

    @property
    def has_scope(self):
        return False

    @property
    def addresses(self):
        return []

    @property
    def domains(self):
        return []

    @property
    def roots(self):
        return []

    @property
    def web_pages(self):
        return []

    def get_targets(self):
        return []

    def __contains__(self, target):
        return True

    def __str__(self):
        return (
            "Audit scope:\n"
            "\n"
            "IP addresses:\n"
            "    *\n"
            "\n"
            "Domains:\n"
            "    *\n"
            "\n"
            "Web pages:\n"
            "    *\n"
        )
