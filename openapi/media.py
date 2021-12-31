# -*- coding: UTF-8 -*-

############################################################################
#
#   Copyright (c) 2020  yingcheng, Inc. All Rights Reserved.
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
############################################################################

"""
media 模块
负责引流到rtmp
"""

from flask import Blueprint, request
import json
import utils.common.response as response
import utils.ffmpeg.ff2rtmp as ff2rtmp
import utils.common.pkgrpc as pkgrpc
import threading
import time

media_module = Blueprint('media', __name__, url_prefix='/openapi/media')

_ff2rtmp = {}


def _start_rtsp_media(ids, rtsp, transport_type='udp'):
    if ids not in _ff2rtmp:
        _ff2rtmp[ids] = ff2rtmp.FF2rtmp(ids)

    if _ff2rtmp[ids].getMediaStatus() is False:
        _ff2rtmp[ids].rtsp2rtmp(rtsp, transport_type)


def _start_rtmp_media(ids, inrtmp):
    if ids not in _ff2rtmp:
        _ff2rtmp[ids] = ff2rtmp.FF2rtmp(ids)

    if _ff2rtmp[ids].getMediaStatus() is False:
        _ff2rtmp[ids].rtmp2rtmp(inrtmp)


def _media_restore():
    """每ns定时恢复流"""
    time.sleep(10)
    while True:
        b, lst = pkgrpc.get_source()
        for item in lst:
            if 'rtsp' in item['source']:
                _start_rtsp_media(item['id'], item['rtsp'], item['transport'])
            elif 'rtmp' in item['source']:
                _start_rtmp_media(item['id'], item['rtsp'])

        time.sleep(45)


# 启动时恢复流媒体
# 延时恢复，等待media模块端口启动
t1 = threading.Thread(target=_media_restore, daemon=True)
t1.start()


@media_module.route('/<int:ids>/stream', methods=['POST', 'DELETE'])
def stream(ids):
    """
    增加通道流 支持从rtsp--->rtmp
    增加通道流 支持从rtmp--->rtmp
    删除通道流
    {
    "source":"rtsp://admin:123456@192.168.1.0/sdf",
    "transport":"udp"
    }
    :param ids:
    :return:
    """
    global _ff2rtmp
    if request.method == 'POST':
        dic = json.loads(request.data)

        if 'rtsp' in dic['source']:
            _start_rtsp_media(ids, dic['source'], dic['transport'])
        elif 'rtmp' in dic['source']:
            _start_rtmp_media(ids, dic['source'])
        else:
            return response.make_response_400()

        r = {'flv': _ff2rtmp[ids].getFlvUri(), 'rtmp': _ff2rtmp[ids].getRtmpUri()}

        return response.make_response_success_data(r)

    else:
        if ids in _ff2rtmp:
            _ff2rtmp[ids].stop()
        return response.make_response_success()


@media_module.route('/<int:ids>/mediainfo', methods=['GET'])
def mediainfo(ids):
    """获取流媒体信息"""
    dic = {}
    if ids in _ff2rtmp:
        code, des = _ff2rtmp[ids].getMediaErr()
        head, bit = _ff2rtmp[ids].getMediaInfo()
        dic = {'head': head,
               'bit': bit,
               'encoding': _ff2rtmp[ids].getMediaCodec(),
               'errcode': code,
               'describe': des}
    return response.make_response_success_data(dic)


@media_module.route('/status', methods=['GET'])
def status():
    """获取所有通道流状态"""
    lst = []
    for k in _ff2rtmp:
        dic = {'id': k, 'status': _ff2rtmp[k].getMediaStatus()}
        lst.append(dic)

    return response.make_response_success_data(lst)
