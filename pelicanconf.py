#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Joseph Long'
SITENAME = 'Joseph Long'
SITEURL = ''

PATH = 'content'
PAGE_PATHS = ['pages']
ARTICLE_PATHS = ['articles']
STATIC_PATHS = ['articles', 'static']
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['render_math']
MATH_JAX = {
    'auto_insert': False,
    'math_tag_class': 'tex2jax_process',
}

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

THEME = 'sitetheme'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

ARTICLE_URL = 'writing/{slug}/'
ARTICLE_SAVE_AS = 'writing/{slug}/index.html'
DRAFT_URL = 'drafts/{slug}/index.html'
DRAFT_SAVE_AS = 'drafts/{slug}/index.html'
PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}/index.html'

AUTHOR_SAVE_AS = ''
TAG_SAVE_AS = ''
CATEGORY_SAVE_AS = ''

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
