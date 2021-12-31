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
内部模块之间通信的rpc接口
"""

import requests
import json
import utils.common.log as log
import utils.common.initres as initres

headers = {
    'Authorization': 'self-internal-token'
}


def get_source():
    """获取源信息"""
    global headers
    url = f"http://127.0.0.1:{initres.SVRPORT}/openapi/source"
    ret = []
    retBool = False
    try:
        res = requests.get(url, headers=headers, timeout=5)
    except Exception as e:
        log.logger.warning('error: {}'.format(e))
    else:
        if res.status_code == 200:
            retdic = json.loads(res.text)
            if retdic['success'] is True:
                ret = retdic['data']
                retBool = True
            else:
                log.logger.error('post device mission failed {}'.format(res.text))
    return retBool, ret


def post_media(ids, stream_url, transport_type):
    """向media模块启流"""
    global headers
    url = f"http://127.0.0.1:{initres.initres}/openapi/media/{ids}/stream"
    dic = {"stream": stream_url, "transport": transport_type}
    ret = {}
    retBool = False
    try:
        res = requests.post(url, headers=headers, data=json.dumps(dic),timeout=5)
    except Exception as e:
        log.logger.warning('error: {}'.format(e))
    else:
        if res.status_code == 200:
            retdic = json.loads(res.text)
            if retdic['success'] is True:
                ret = retdic['data']
                retBool = True
            else:
                log.logger.error('post device mission failed {}'.format(res.text))
    return retBool, ret


def delete_media(ids):
    """media模块关闭流"""
    global headers
    url = f"http://127.0.0.1:{initres.SVRPORT}/openapi/media/{ids}/stream"
    try:
        requests.delete(url, headers=headers)
    except Exception as e:
        log.logger.warning('error: {}'.format(e))
