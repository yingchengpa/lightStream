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


from onvif2 import ONVIFCamera
from zeep.transports import Transport
import utils.common.log as log
import json
import utils.common.comfunc as common


class OnvifClient:

    def __init__(self):
        self.myCam = None
        self.media_service = None
        self.media2_service = None
        self.name = ''
        self.pwd = ''
        self.info = {}  # 记录设备基础信息字典

    def __del__(self):
        pass

    def conn(self, ip, port, name, pwd) -> int:
        """
        通过鉴权对设备进行连接.
        media\media2  默认加载，其他模块按需加载
        :param ip:
        :param port:
        :param name:
        :param pwd:
        :return: 成功 1  超时 -1  鉴权失败 -2
        """
        try:
            # 设置操作时间 
            transport = Transport(operation_timeout=10)

            # 设置wsdl 文件夹目录，需要把 Lib\site-packages\wsdl 复制到当前可执行文件目录
            self.myCam = ONVIFCamera(ip, port, name, pwd, wsdl_dir=common.getExePath() + '/wsdl',
                                     transport=transport)
        except Exception as e:
            log.logger.warning('error: {}'.format(e))
            return -1
        finally:
            pass

        self.getMedia()

        # GetDeviceInformation 时进行账号校验
        """
           获取onvif设备基础信息
           "FirmwareVersion": "IPC_Q1207-B0006D1904",
           "HardwareId": "xdfd@SH-FA-VA",
           "Manufacturer": "bbb",
           "Model": "xdfd@SH-FA-VA",
           "SerialNumber": "210235C3EN3193000033"
        """
        try:
            resp = self.myCam.devicemgmt.GetDeviceInformation()
        except Exception as e:
            log.logger.warning('error: {}'.format(e))
            return -2
        else:
            self.info = {'manufacturer': resp.Manufacturer,
                         'model': resp.Model,
                         'firmwareversion': resp.FirmwareVersion,
                         'serialnumber': resp.SerialNumber,
                         'hardwareid': resp.HardwareId}
        finally:
            pass

        self.name = name
        self.pwd = pwd

        return 1

    # ---------------------------------- media \ media2 -------------------------------------------
    def getMedia(self):
        """
        获取media： 分为media2、media，其中media2支持h265，media只支持h264
        :return:
        # 先使用media2，再使用media： media2支持h265
        # 比如海康、大华、宇视都支持media2， 有的只支持media
        """
        try:
            self.media2_service = self.myCam.create_media2_service()
        except Exception as e:
            log.logger.warning('error: {}'.format(e))
        finally:
            pass

        # media 获取h264
        if self.media2_service is None:
            try:
                self.media_service = self.myCam.create_media_service()
            except Exception as e:
                log.logger.warn('error: {}'.format(e))
                return False
            finally:
                pass

        return True

    def _getStreamUri(self) -> list:
        """通过media1.0 获取rtsp地址"""
        profiles = self.media_service.GetProfiles()

        urlLst = []
        for profile in profiles:
            o = self.media_service.create_type('GetStreamUri')
            o.ProfileToken = profile.token
            o.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
            r = self.media_service.GetStreamUri(o)

            # 携带鉴权信息
            if self.pwd != '':
                dic = {'token': profile.token,
                       'rtsp': "rtsp://{}:{}@{}".format(self.name, self.pwd, r['Uri'][7:])}
            else:
                dic = {'token': profile.token,
                       'rtsp': r['Uri']}
            urlLst.append(dic)

        return urlLst

    def _getVideo(self) -> list:
        """通过media1.0 获取编码参数"""
        configurations = self.media_service.GetVideoEncoderConfigurations()

        lns = []
        for configuration in configurations:
            if configuration['Encoding'].lower() == 'h264':
                width = configuration['Resolution']['Width']
                height = configuration['Resolution']['Height']
                dic = {'token': configuration['token'],
                       'encoding': configuration['Encoding'],
                       'ratio': "{}*{}".format(width, height),
                       'fps': configuration['RateControl']['FrameRateLimit'],
                       'bitrate': configuration['RateControl']['BitrateLimit'],
                       'gop': configuration['H264']['GovLength'],
                       'profile': configuration['H264']['H264Profile'],
                       'quality': configuration['Quality']}

            else:
                dic = {'token': configuration['Name'], 'encoding': configuration['Encoding']}

            lns.append(dic)

        return lns

    def _getStreamUri2(self) -> list:
        """通过media2.0 版本获取rtsp地址"""
        profiles = self.media2_service.GetProfiles()

        uriLst = []
        for profile in profiles:
            o = self.media2_service.create_type('GetStreamUri')
            o.ProfileToken = profile.token
            o.Protocol = 'RTSP'
            uri = self.media2_service.GetStreamUri(o)

            # 携带鉴权信息
            if self.pwd != '':
                dic = {'token': profile.token,
                       'rtsp': "rtsp://{}:{}@{}".format(self.name, self.pwd, uri[7:])}
            else:
                dic = {'token': profile.token,
                       'rtsp': uri}

            uriLst.append(dic)

        return uriLst

    def _getVideo2(self) -> list:
        """通过media2获取编码配置，media2支持h265"""
        configurations = self.media2_service.GetVideoEncoderConfigurations()

        lns = []
        for configuration in configurations:
            if configuration['Encoding'].lower() == 'h264' or configuration['Encoding'].lower() == 'h265':
                width = configuration['Resolution']['Width']
                height = configuration['Resolution']['Height']
                dic = {'token': configuration['token'],
                       'encoding': configuration['Encoding'],
                       'ratio': "{}*{}".format(width, height),
                       'fps': configuration['RateControl']['FrameRateLimit'],
                       'bitrate': configuration['RateControl']['BitrateLimit'],
                       'gop': configuration['GovLength'],
                       'profile': configuration['Profile'],
                       'quality': configuration['Quality']}
            else:
                dic = {'token': configuration['Name'], 'encoding': configuration['Encoding']}

            lns.append(dic)

        return lns

    def getStreamUri(self) -> list:
        """
        获取流地址
        :return:
        """
        if self.media2_service is not None:
            urls = self._getStreamUri2()
        else:
            urls = self._getStreamUri()

        return urls

    def getVideo(self) -> list:
        """
        获取视频信息
        :return:
        """
        if self.media2_service is not None:
            vidoes = self._getVideo2()
        else:
            vidoes = self._getVideo()

        return vidoes

    def getDeviceInfo(self) -> dict:
        return self.info


if __name__ == '__main__':
    obj = OnvifClient()
    r = obj.conn('204.204.50.191', 80, 'admin', 'admin_123')
    if r == 1:
        print(json.dumps(obj.getDeviceInfo()))
    elif r == -2:
        print("鉴权失败")
    elif r == -1:
        print("超时")
