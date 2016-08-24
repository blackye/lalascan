#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Portscan results.
"""

__all__ = ["Portscan"]

from . import Fingerprint
from ..resource.ip import IP

from lalascan.api.exception import LalascanTypeError, LalascanValueError

#------------------------------------------------------------------------------
class PortScanFingerprint(Fingerprint):
    """
    Portscan results.
    """

    #--------------------------------------------------------------------------
    def __init__(self, ip, ports):
        """
        :param ip: Scanned host's IP address.
        :type ip: IP

        :param ports: Portscan results.
            A set of tuples, each tuple containing the following data for
            each scanned port: state, protocol, port. The state is a string
            with one of the following values: "OPEN, "CLOSED" or "FILTERED".
            The protocol is a string with one of the following values: "TCP"
            or "UDP". The port is an integer from 0 to 65536, not included.
        :type ports: set( tuple(int, str), ... )

        """

        # Sanitize and store the properties.
        try:
            assert isinstance(ip, IP), type(ip)
            self.__address   = ip.address
            sane    = set()
            visited = set()
            for port, service in ports:
                port     = int(port)
                service  = str(service.upper())

                if port <= 0 or port > 65535:
                    raise LalascanValueError("Invalid port number: %d" % port)
                key = (port, service)
                if key not in visited:
                    visited.add(key)
                    sane.add( (port, service) )
            self.__ports = frozenset(sane)
        except Exception:
            ##raise # XXX DEBUG
            raise LalascanValueError("Malformed portscan results!")

        # Call the superclass constructor.
        super(PortScanFingerprint, self).__init__()


    #--------------------------------------------------------------------------
    @property
    def address(self):
        """
        :returns: Scanned host's IP address.
        :rtype: str
        """
        return self.__address


    #--------------------------------------------------------------------------
    @property
    def ports(self):
        """
        :returns: Portscan results.
            A set of tuples, each tuple containing the following data for
            each scanned port: service.
        :rtype: frozenset( tuple(int, str), ... )
        """
        return self.__ports


    #--------------------------------------------------------------------------
    def __repr__(self):
        return "<%s name=%s port=%d service=%s" % (
            self.__class__.__name__, self.name, self.port, self.protocol
        )


    #--------------------------------------------------------------------------
    def __str__(self):
        return "\n".join("%-8s %-3s %d" % p for p in sorted(self.ports))


    #--------------------------------------------------------------------------
    @property
    def display_name(self):
        return "Port Scan Results"

