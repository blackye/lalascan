#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
HTML document.
"""

__all__ = ["HTML"]

from lalascan.data.information import File
from lalascan.libs.net.web_utils import HTMLParser
from lalascan.utils.text_utils import to_utf8


#------------------------------------------------------------------------------
class HTML(File):
    """
    HTML document.

    This object contains all of relevant tags of a HTML document:

    - title
    - links
    - forms
    - images
    - objects
    - metas
    - css_links
    - css_embedded
    - javascript_links
    """

    #--------------------------------------------------------------------------
    def __init__(self, data):
        """
        :param data: Raw HTML content.
        :type data: str
        """

        # Raw HTML content
        self.__raw_data = to_utf8(data)

        # Parent constructor
        super(HTML, self).__init__()


    #--------------------------------------------------------------------------
    @property
    def display_name(self):
        return "HTML Content"


    #--------------------------------------------------------------------------
    @property
    def raw_data(self):
        """
        :return: Raw HTML content.
        :rtype: str
        """
        return self.__raw_data


    #--------------------------------------------------------------------------
    @property
    def elements(self):
        """
        :return: All HTML elements.
        :rtype: list(HTMLElement)
        """
        return HTMLParser(self.raw_data).elements


    #--------------------------------------------------------------------------
    @property
    def forms(self):
        """
        :return: HTML form tags.
        :rtype: list(HTMLElement)
        """
        return HTMLParser(self.raw_data).forms


    #--------------------------------------------------------------------------
    @property
    def images(self):
        """
        :return: Image tags.
        :rtype: list(HTMLElement)
        """
        return HTMLParser(self.raw_data).images


    #--------------------------------------------------------------------------
    @property
    def url_links(self):
        """
        :return: Link tags.
        :rtype: list(HTMLElement)
        """
        return HTMLParser(self.raw_data).url_links


    #--------------------------------------------------------------------------
    @property
    def css_links(self):
        """
        :return: CSS links.
        :rtype: list(HTMLElement)
        """
        return HTMLParser(self.raw_data).css_links


    #--------------------------------------------------------------------------
    @property
    def javascript_links(self):
        """
        :return: JavaScript links.
        :rtype: list(HTMLElement)
        """
        return HTMLParser(self.raw_data).javascript_links


    #--------------------------------------------------------------------------
    @property
    def css_embedded(self):
        """
        :return: Embedded CSS.
        :rtype: list(HTMLElement)
        """
        return HTMLParser(self.raw_data).css_embedded


    #--------------------------------------------------------------------------
    @property
    def javascript_embedded(self):
        """
        :return: Embedded JavaScript.
        :rtype: list(HTMLElement)
        """
        return HTMLParser(self.raw_data).javascript_embedded


    #--------------------------------------------------------------------------
    @property
    def metas(self):
        """
        :return: Meta tags.
        :rtype: list(HTMLElement)
        """
        return HTMLParser(self.raw_data).metas


    #--------------------------------------------------------------------------
    @property
    def title(self):
        """
        :return: Document title.
        :rtype: HTMLElement
        """
        return HTMLParser(self.raw_data).title


    #--------------------------------------------------------------------------
    @property
    def objects(self):
        """
        :return: Object tags.
        :rtype: list(HTMLElement)
        """
        return HTMLParser(self.raw_data).objects
