# -*- coding: utf-8 -*-

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

from flask import Flask
import utils.common.log as log
import utils.common.initres as initres
import logging

from openapi.onvif_cl import onvif_module
from openapi.source import source_module
from openapi.media import media_module


SVR_NAME = 'lightStream'
SVR_VERSION = '0.0.1'

app = Flask(__name__)

app.register_blueprint(media_module)
app.register_blueprint(onvif_module)
app.register_blueprint(source_module)


@app.route('/', methods=['HEAD'])
def head():
    """
    支持head方法，检查接口是否正常
    :return:
    """
    return '200'


if __name__ == '__main__':

    # 启动时，首先向注册中心注册本服务
    # 去掉info级别日志
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

    # 启动 http 服务
    log.logger.info(f"{SVR_NAME} start ......")

    app.run(host="0.0.0.0", port=initres.SVRPORT, debug=False)  # 调试环境

