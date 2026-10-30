# Copyright 2020 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Runs a python2_action. Upstream forced Python 2 here; this branch runs Python 3."""

import os
import subprocess
import sys

if sys.version_info.major == 2:
  # If we get here, we're already Python2, so just re-execute the
  # command without the wrapper.
  exe = sys.executable
elif sys.executable.endswith('.exe'):
  # If we get here, we're a Python3 executable likely running on
  # Windows, so look for the Python2 wrapper in depot_tools. We
  # can't invoke it directly because some command lines might exceed the
  # 8K commamand line length limit in cmd.exe, but we can use it to
  # find the underlying executable, which we can then safely call.
  exe = subprocess.check_output(
      ['python.bat', '-c',
       'import sys; print(sys.executable)']).decode('utf8').strip()
else:
  # Python 3 only on this branch: the actions are ported, so run them with
  # the interpreter GN started (script_executable in .gn).
  exe = sys.executable

# A script from a DEPS checkout that still assumes Python 2 has a shim of the same
# name in py3_shims/, which takes the script and its arguments and runs it.
shim = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'py3_shims',
                    os.path.basename(sys.argv[1]))
if os.path.isfile(shim):
  sys.argv[1:1] = [shim]

sys.exit(subprocess.call([exe] + sys.argv[1:]))
