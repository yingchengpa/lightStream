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
#############################################################################

from flask import Blueprint, request
import utils.sql.source.source as sqlsource
import json
import utils.common.response as response
import utils.common.pkgrpc as pkgrpc


source_module = Blueprint('source', __name__, url_prefix='/openapi/source')


@source_module.route('/', methods=['GET'])
def sourceList():
    """获取所有通道信息"""
    if request.method == 'GET':
        obj = sqlsource.TblSource()
        lst = obj.getAll()
        return response.make_response_success_data(lst)


@source_module.route('/<int:ids>', methods=['PUT', 'DELETE', 'POST'])
def source(ids):
    """通道增--post
           删--delete
           改--put
    {
    "source":"rtsp://admin:123@192.168.1.1" or "rtmp:/192.168.1.1:1935/live/1"
    "transport":"udp"
    }
    """
    if request.method == 'POST':
        dic = json.loads(request.data)
        obj = sqlsource.TblSource()

        # 启动流
        b, ret = pkgrpc.post_media(ids, dic['source'], dic['transport'])
        if b :
            dic['rtmp'] = ret['rtmp']
            dic['flv'] = ret['flv']
            obj.modify(ids, dic)
            return response.make_response_success_no_data()
        else:
            return response.make_response_1000()
    elif request.method == 'DELETE':
        obj = sqlsource.TblSource()
        obj.delete(ids)
        # 发送请求到media模块，关闭该通道的ffmpeg流媒体
        pkgrpc.delete_media(ids)

        return response.make_response_success_no_data()
    elif request.method == 'PUT':
        dic = json.loads(request.data)
        if 'name' in dic:
            obj = sqlsource.TblSource()
            obj.modifyName(ids, dic['name'])
        return response.make_response_success_no_data()

