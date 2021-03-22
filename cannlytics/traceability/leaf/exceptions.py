# -*- coding: utf-8 -*-
"""
cannlytics.traceability.leaf.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Exceptions used in Leaf Data Systems.
"""


class TraceabilityException(Exception):
    """A base class for Leaf Data System's exceptions."""


class APIError(TraceabilityException):
    def __init__(self, response):

        super(APIError, self).__init__(self._extract_text(response))
        self.response = response

    def _extract_text(self, response):
        return self._text_from_detail(response) or response.text

    def _text_from_detail(self, response):
        try:
            errors = response.json()
            return errors['error']
        except (AttributeError, KeyError, ValueError):
            return None
