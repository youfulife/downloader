# -*- coding: utf-8 -*-

import subprocess

rc = subprocess.check_call(["ls", "-l"])


print(rc)

