"""
Test specific settings
"""

import os

from .base import * # noqa


# fix the stats file path for the tests
WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = os.path.join(os.path.dirname(BASE_DIR), 'webpack-stats.json')
