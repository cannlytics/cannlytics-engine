# -*- coding: utf-8 -*-
"""
cannlytics.traceability.metrc.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Exceptions used when interfacing with the Metrc API.
"""


class TraceabilityException(Exception):
    """A base class for traceability system exceptions."""


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
