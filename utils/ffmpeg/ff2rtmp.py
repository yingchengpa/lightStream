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
通过ffmpeg将rtsp/rtmp 码流转封装为rtmp
"""

# 从ffmpeg的输出信息中判断
# 流是否出异常
# 正常码流的信息，比如分辨率、帧率、码率、建流时间

import subprocess
import threading
from datetime import datetime
import psutil
import utils.common.log as log
import os

# 删掉所有ffmpeg 子进程
os.popen('killall {}'.format('ffmpeg'))

def makeFlvUri(ids):
    """构造media模块flv的uri"""
    return '/live/{}.flv'.format(ids)


def makeRtmpUri(ids):
    """构造media模块rtmp的uri"""
    return '/live/{}'.format(ids)


class FF2rtmp:
    """
    ffmpeg  -i rtsp://admin:admin_123@204.204.70.67:554/video1 -vcodec copy -an -f flv rtmp://127.0.0.1:1935/live/1
    """

    def __init__(self, ids):
        self.process = None
        self.mediaHead = ''  # 流的头信息
        self.mediaBit = ''  # 流的实时码流信息
        self.running = False  # 流关闭
        self.thread = None
        self.flvUri = makeFlvUri(ids)
        self.rtmpUri = makeRtmpUri(ids)
        self.ids = ids

    def __del__(self):
        self.stop()

    def _kill(self):
        if self.process:
            self.process.kill()
            self.process = None

    def _checkMedia(self, line):
        """
        :param line: stdout 输出的每一行信息
        :return:建立流失败 返回失败
        """
        if 'Connection refused' in line:
            self.mediaHead += line
            return False

        if '[flv' in line or '[NULL @' in line:
            pass
        elif '[rtsp @' in line:
            pass
        elif 'Non-monotonous' in line:
            pass
        elif 'frame=' in line:
            self.mediaBit = line
        else:
            # 最长只保留2000个字符
            if len(self.mediaHead) < 2000:
                self.mediaHead += line
        return True

    # 仅进行码流转封装，不转码且去掉音频
    def _startFF(self, cmd):
        try:
            # log.logger.info("start :{}".format(commd))
            self.mediaHead = ''
            self.mediaBit = ''
            self.process = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdin=subprocess.PIPE,
                                            stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

            start_time = datetime.now()

            while self.running:
                # 从输出中判断是否正常建立
                line = (str(self.process.stdout.readline()))  # 去掉结尾的换行符
                bMedia = self._checkMedia(line)
                if not bMedia:  # 流建立失败
                    self.running = False

                # 从进程状态判断是否进程已退出
                if (datetime.now() - start_time).total_seconds() > 2:
                    if self.process.poll() is not None:  # 进程已经终止
                        self.running = False

            # 存在多种退出的原因，进程自动退出的，用户手动退出的
            # 主动关闭,向进程输入'q'命令正常退出
            if not self.running:
                self.process.stdin.write('q')
                self.process.communicate()

        except Exception as e:
            log.logger.warning('error: {}'.format(e))
        finally:
            pass

    def rtsp2rtmp(self, stream, transport_type='udp'):
        """
        将流(rtsp）转为rtmp
        :param stream:
        :param encoding: h265 h264
        :param transport_type:udp tcp
        :return rtmp uri,flv uri
        """
        # 超时时间 6s -stimeout 6000000
        # -rtsp_transport tcp  公网环境需要媒体流和rtsp信令都使用tcp同一个通道，减少端口数量
        # ffmpeg_cmd = '''ffmpeg  -rtsp_transport tcp -stimeout 6000000 -i {} -vcodec copy -an -f flv {} '''.format(stream, rtmp)
        # 正常h264格式 ffmpeg -i
        # rtsp://admin:admin_123@204.204.70.67:554/video1 -vcodec copy -an -f hevc - | ffmpeg -f hevc  -i - -c copy
        # -f flv rtmp://127.0.0.1:1935/live/2        h265(hevc) 格式，因为宇视h265 rstp中没有携带sps、pps

        rtmp = 'rtmp://127.0.0.1:1935{}'.format(self.rtmpUri)

        if 'tcp' == transport_type.lower():
            ffmpeg_cmd = """ffmpeg -rtsp_transport tcp -stimeout 6000000 -i \"{}\" -vcodec copy -an -f flv {} """.format(
                    stream, rtmp)
        else:
            ffmpeg_cmd = """ffmpeg  -stimeout 6000000 -i \"{}\" -vcodec copy -an -f flv {} """.format(stream, rtmp)

        log.logger.warning(ffmpeg_cmd)

        self.thread = threading.Thread(target=self._startFF, args=(ffmpeg_cmd,), daemon=True)
        self.thread.start()
        self.running = True
        return

    def rtmp2rtmp(self, inrtmp):
        """
        将流(rtmp）转为rtmp
        :param inrtmp:  inrtmp 规则为 : rtmp://{boxip}:1935/live/ids+1000
        :return rtmp uri,flv uri
        """
        # ffmpeg_cmd = '''ffmpeg   -i {} -vcodec copy -an -f flv {} '''.format(inrtmp, outrtmp)

        rtmp = 'rtmp://127.0.0.1:1935{}'.format(self.rtmpUri)

        ffmpeg_cmd = """ffmpeg  -i \"{}\" -vcodec copy -an -f flv {} """.format(inrtmp, rtmp)

        log.logger.warning(ffmpeg_cmd)

        self.thread = threading.Thread(target=self._startFF, args=(ffmpeg_cmd,), daemon=True)
        self.thread.start()
        self.running = True
        return

    def stop(self):
        try:
            self.running = False
            if self.thread.is_alive():
                self.thread.join(0.5)

        except Exception as e:
            log.logger.warning('error: {}'.format(e))
        finally:
            pass

    def getMediaInfo(self):
        """获取ffmpeg启动的头信息"""
        return self.mediaHead, self.mediaBit

    def getMediaCodec(self):
        """获取实际流的编码信息"""
        if 'h264' in self.mediaHead:
            return 'h264'
        elif 'hevc' in self.mediaHead:
            return 'hevc'
        else:
            return 'unknown'

    def getMediaErr(self):
        """获取ffmpeg创建时的失败信息"""
        code = 0
        des = ''
        if self.getMediaStatus() is False:
            # rtsp 密码错误
            if 'Unauthorized' in self.mediaHead:
                code = 401
                des = 'rtsp 401 Unauthorized (authorization failed)'
            # rtsp 地址不可达，导致链接失败
            elif 'Connection refused' in self.mediaHead:
                code = 402
                des = 'Connection refused, may be ip is unreachable'
            # 本地rtmp地址已经存在转发
            elif 'Already publishing' in self.mediaHead:
                code = 403
                des = 'rtmp server is Already publishing, dont retry'
            # 连接超时
            elif 'Connection timed out' in self.mediaHead:
                code = 404
                des = 'Connection timed out'
            # 输入格式错误
            elif 'Input/output error' in self.mediaHead:
                code = 405
                des = 'Input/output error'
            else:
                pass

        return code, des

    def getMediaStatus(self):
        """获取状态"""
        try:
            psutil.Process(self.process.pid)
        except Exception as e:
            return False
        else:
            return True

    def getRtmpUri(self):
        return self.rtmpUri

    def getFlvUri(self):
        return self.flvUri


if __name__ == '__main__':
    obj = FF2rtmp(2)
    obj.rtsp2rtmp('rtsp://admin:admin_123@204.204.70.67:554/video1', 'rtmp://127.0.0.1:1935/live/1')
    input('按任意键退出')
