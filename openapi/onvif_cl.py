# -*- coding: UTF-8 -*-

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

from flask import Blueprint, request
import json
import utils.common.response as response
import utils.onvif.onvif_cl as onvif_cl

onvif_module = Blueprint('onvif', __name__, url_prefix='/openapi/onvif')


@onvif_module.route('/streamuri', methods=['POST'])
def streamUri():
    """
    获取流和视频信息
    {
    "url":"192.168.1.0",
    "port: 80,
    "username":"admin",
    "pwd":"123456"
    }
    :return:
    """
    if request.method == 'POST':
        dic = json.loads(request.data)
        obj = onvif_cl.COnvifClient()
        ret = obj.conn(dic['url'], dic['port'], dic['username'], dic['pwd'])
        if ret == 1:
            r = {'rtsp': obj.getsteamuri(), 'video': obj.getVideo()}
            return response.make_response_success_data(r)
        elif ret == -1:
            return response.make_response_1100()
        elif ret == -2:
            return response.make_response_1102()


@onvif_module.route('/deviceinfo', methods=['POST'])
def deviceInfo():
    """
    获取设备信息
    {
    "url":"192.168.1.0",
    "port: 80,
    "username":"admin",
    "pwd":"123456"
    }
    :return:
    """
    if request.method == 'POST':
        dic = json.loads(request.data)
        obj = onvif_cl.OnvifClient()
        ret = obj.conn(dic['url'], dic['port'], dic['username'], dic['pwd'])
        if ret == 1:
            return response.make_response_success_data(obj.getDeviceInfo())
        elif ret == -1:
            return response.make_response_1100()
        elif ret == -2:
            return response.make_response_1102()


@onvif_module.route('/device', methods=['POST'])
def device():
    """
    获取设备信息，包括流、设备、视频参数
    {
    "url":"192.168.1.0",
    "port": 80,
    "username":"admin",
    "pwd":"123456"
    }
    :return:
    """
    if request.method == 'POST':
        dic = json.loads(request.data)
        obj = onvif_cl.OnvifClient()
        ret = obj.conn(dic['url'], dic['port'], dic['username'], dic['pwd'])
        if ret == 1:
            r = obj.getDeviceInfo()
            r['rtsp'] = obj.getStreamUri()
            r['video'] = obj.getVideo()
            return response.make_response_success_data(r)
        elif ret == -1:
            return response.make_response_1100()
        elif ret == -2:
            return response.make_response_1102()
