#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
IP address.
"""

__all__ = ["IP"]

from . import Resource
from ...utils.text_utils import to_utf8

from ...api.exception import LalascanValueError

from netaddr import IPAddress



#------------------------------------------------------------------------------
class IP(Resource):
    """
    IP address.
    """


    #--------------------------------------------------------------------------
    def __init__(self, address):
        """
        :param address: IP address.
        :type address: str
        """

        address = to_utf8(address)
        if not isinstance(address, str):
            raise TypeError("Expected str, got %r instead" % type(address))

        try:
            if address.startswith("[") and address.endswith("]"):
                parsed  = IPAddress(address[1:-1], version=6)
                address = address[1:-1]
            else:
                parsed  = IPAddress(address)
            version = int( parsed.version )
        except Exception:
            raise LalascanValueError("Invalid IP address: %s" % address)

        # IP address and protocol version.
        self.__address = address
        self.__version = version

        # Parent constructor.
        super(IP, self).__init__()


    #--------------------------------------------------------------------------
    def __str__(self):
        return self.address


    #--------------------------------------------------------------------------
    def __repr__(self):
        return "<IPv%s address=%r>" % (self.version, self.address)


    #--------------------------------------------------------------------------
    @property
    def display_name(self):
        return "IP info"


    #--------------------------------------------------------------------------
    @property
    def address(self):
        """
        :return: IP address.
        :rtype: str
        """
        return self.__address


    #--------------------------------------------------------------------------
    @property
    def version(self):
        """
        :return: version of IP protocol: 4 or 6.
        :rtype: int(4|6)
        """
        return self.__version
