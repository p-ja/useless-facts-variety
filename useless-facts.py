#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
"""
Variety quotes plugin sourcing useless facts from https://uselessfacts.jsph.pl/
@author: p-ja
"""

import logging

from locale import gettext as _
from variety.plugins.IQuoteSource import IQuoteSource
from variety.Util import Util
from variety.Util import cache

logger = logging.getLogger("variety")

default_fact = {
    "text": "The number pi approximately equals 3.14159",
    "source": None,
    "source_url": None,
    "permalink": None
}

class UselessFactsSource(IQuoteSource):

    def __init__(self):
        super(IQuoteSource, self).__init__()

    @classmethod
    def get_info(cls):
        return {
            "name": "Useless facts",
            "description": _("Useless but true facts"),
            "version": "0.1",
            "author": "p-ja"
        }

    def activate(self):
        if self.active:
            return
        super(UselessFactsSource, self).activate()
        self.active = True

    def deactivate(self):
        self.active = False

    def needs_internet(self):
        '''
        Normaly this plugin requires internet access,
        but it fails gracefully if the internet access
        is not granted.
        '''
        return False

    def supports_search(self):
        return False

    def get_random(self):
        fact = self._get_fact()
        return [
            {
                "quote": fact['text'],
                "author": fact.get('source', None),
                "sourceName": fact.get('source_url', None),
                "link": fact.get('permalink', None)
            }
        ]

    def _get_fact(self):
        if not Util.internet_enabled:
            return default_fact

        try:
            fact = self._fetch_fact()
        except Exception as err:
            logger.warning("Failed to fetch fact {}".format(err))
            return default_fact

        if not isinstance(fact, dict):
            return default_fact

        if 'text' not in fact:
            return default_fact

        return fact

    @cache(ttl_seconds=30, debug=True)
    def _fetch_fact(self):
        logger.debug("Fetching useless fact...")
        URL = "https://uselessfacts.jsph.pl/random.json?language=en"
        return Util.fetch_json(URL)
