# lightStream

#### 介绍
基于python简单的onvif、rtsp、rtmp取流服务，方便web播放实时视频

#### 软件架构

![image](https://user-images.githubusercontent.com/6310830/147810239-e01aeb43-4065-4279-8503-5a47260ad2db.png)



### 总体介绍
如上图介绍，在如何取得ipc流并在浏览器中低延时播放，lightstream 只是整体架构中很小的一部分。最核心的是：ffmpeg 、srs和web jsplayer组件。

其中ffmpeg 实现通过rtsp协议转换为rtmp给srs， jsplayer通过http-flv协议从srs获取媒体流；如何做到低延时、无控件播放难点在于jsplayer，其中

我只是举例了一个jsplayer，类似的还有flv.js(高延时、不支持h265）、wxinlineplayer（高延时）等。

### nginx
nginx 作为代理服务器，主要做端口转发，如反向代理lightstream的2233端口、srs的8080端口

~~~
# 支持http-flv
    location /live {
			proxy_pass http://127.0.0.1:8080;
    }	
    
# 支持lightstream
        location /openapi{
			proxy_pass http://127.0.0.1:2233;
        }	
~~~

### 如何支持rtmp

- 启动srs， ./objs/srs -c conf/http.flv.live.conf

- 在海康、大华、宇视web界面设置srs rtmp服务器地址，如 rtmp://192.168.1.10/live/100

- srs日志中会显示收到 /live/100 的流

- 在jsplayer 中输入： http://192.168.1.10/live/100.flv , 实况正常显示


### 如何支持rtsp--依赖lightstream

- 设置好ffmpeg路径

- 启动lightstream (192.168.1.10:2233）

- 启动srs

- 调用接口 post http://192.168.1.10/openapi/source/1  
~~~
body

{
    "source":"rtsp://admin:123456@192.168.1.5:554/cam/realmonitor?channnel=1&subtype",
    "transport":"udp"
}
~~~

lightstream 会自动ffmpeg命令，将rtsp流 转发到srs中，rtsmp://192.168.1.10/live/1

- 在jsplayer 中输入： http://192.168.1.10/live/1.flv , 实况正常显示


### 如何支持onvif相机--依赖lightstream

- 设置好ffmpeg路径

- 启动lightstream (192.168.1.10:2233）

- 启动srs

- 调用接口 post http://192.168.1.10/openapi/onvif/device
~~~
body

{
    "url":"192.168.1.5",
    "port":80,
    "username":"admin",
    "pwd":"123456"
}
~~~

返回数据中包含ipc主辅流的rtsp信息，

- 调用接口 post http://192.168.1.10/openapi/source/1  
~~~
body

{
    "source":"rtsp://admin:123456@192.168.1.5:554/cam/realmonitor?channnel=1&subtype",
    "transport":"udp"
}
~~~
返回数据中包含rtmp和flv地址

lightstream 会自动ffmpeg命令，将rtsp流 转发到srs中，rtsmp://192.168.1.10/live/1

- 在jsplayer 中输入： http://192.168.1.10/live/1.flv , 实况正常显示

### 对hevc（h265）的支持

- 使用onvif2-zeep ，支持onvif media2协议，可以获取到hevc信息

- 修改ffmpeg、srs 源码支持hevc 的flv ，见github仓库 [https://github.com/yingchengpa/livestream]

