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
日志文件
"""

import logging
from logging.handlers import TimedRotatingFileHandler
import utils.common.comfunc as comfunc

log_fmt = '%(asctime)s %(filename)s:%(lineno)d[%(levelname)s]:%(message)s'
formatter = logging.Formatter(log_fmt)
logging.basicConfig(level=logging.DEBUG, format=log_fmt)
logger = logging.getLogger()

log_pre = "daily.log"


def logfile_init():
    """
    循环写入日志初始化
    :return:
    """
    log_path = comfunc.getExePath()
    log_file_handler = TimedRotatingFileHandler(filename=log_path + "/{}".format(log_pre),
                                                when="D", interval=1, backupCount=7, encoding='utf-8')
    log_file_handler.suffix = "%Y-%m-%d.log"
    log_file_handler.setFormatter(formatter)
    log_file_handler.setLevel(logging.INFO)
    logger.addHandler(log_file_handler)


logfile_init()
