#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Resource types.
"""

__all__ = ["Resource"]

from .. import Data


#------------------------------------------------------------------------------
class Resource(Data):
    """
    Base class for resources.
    """

    data_type = Data.TYPE_RESOURCE
    data_subtype = "resource/abstract"
