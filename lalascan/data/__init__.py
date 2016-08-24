#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

__all__ = [

    # Base class for all data objects.
    "Data",
]


#------------------------------------------------------------------------------
class Data(object):
    """
    Base class for all data entities.
    This is the common interface for Information, Resource and Vulnerability.
    """
    #--------------------------------------------------------------------------
    # Data types

    TYPE_UNKNOWN = 0      # not a real type! only used in get_accepted_types()

    TYPE_INFORMATION   = 1
    TYPE_VULNERABILITY = 2
    TYPE_RESOURCE      = 3

    data_type = TYPE_UNKNOWN


    #--------------------------------------------------------------------------
    def __init__(self):
       pass


    def is_instance(self, clazz):
        try:
            data_type    = clazz.data_type
            data_subtype = clazz.data_subtype
        except AttributeError:
            return False
        return self.data_type    == data_type    and \
               self.data_subtype == data_subtype
