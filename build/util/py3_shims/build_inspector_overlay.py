# Copyright 2026 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Runs devtools-frontend's scripts/build/build_inspector_overlay.py on Python 3.

At the M88 devtools-frontend revision it hands rollup's stdout, which is bytes on
Python 3, to rjsmin.jsmin; that returns the repr of the bytes, not minified, and
the size check fails. This decodes it first and leaves the rest to the script.

Usage: build_inspector_overlay.py ORIGINAL_SCRIPT [ARGS...] (see python2_action.py)
"""

import os
import runpy
import sys

script = sys.argv[1]
sys.argv = sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(script)))

import rjsmin  # pylint: disable=wrong-import-position

_jsmin = rjsmin.jsmin


def _jsmin_text(text, *args, **kwargs):
  if isinstance(text, bytes):
    text = text.decode('utf-8')
  return _jsmin(text, *args, **kwargs)


rjsmin.jsmin = _jsmin_text
runpy.run_path(script, run_name='__main__')
