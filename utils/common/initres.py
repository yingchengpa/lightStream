# -*- coding: utf-8 -*-

############################################################################
#
#   Copyright (c) 2020  yingchengpa, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#############################################################################

"""
创建初始资源
"""

import os
import sys

# ----------------------------  目录资源 ---------------------------------
# 微服务的根目录
if 'win' in sys.platform:
    rootpath = 'd:/lightStream'
else:
    rootpath = '/opt/lightStream'

SVRPORT = 2233

# 服务的db目录
SQLITEPATH = rootpath + '/sql'

# 日志收集 目录
LOGSPATH = rootpath + '/logs'

# config 目录
CFGPATH = rootpath + '/config'

# 创建目录
os.makedirs(rootpath, exist_ok=True)

# 创建目录
os.makedirs(SQLITEPATH, exist_ok=True)

# 创建目录
os.makedirs(LOGSPATH, exist_ok=True)

# 创建目录
os.makedirs(CFGPATH, exist_ok=True)


def mkpath(path):
    """递归创建目录"""
    os.makedirs(path, exist_ok=True)
