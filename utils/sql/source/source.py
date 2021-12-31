# -*- coding: utf-8 -*-

#############################################################################
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
##############################################################################

import utils.sql.base.sqlbase as sqlbase
import utils.sql.base.sqlitebase as sqlitebase
import utils.common.initres as initres


_DB_SCRIPT = """
CREATE TABLE tbl_source (
            "id" INTEGER NOT NULL default 0,
            "name" VARCHAR(64) NOT NULL default '',
            "url"  VARCHAR(64) NOT NULL default '',
            "port" INTEGER NOT NULL default 0,
            "state" INTEGER NOT NULL default 0,
            "username" VARCHAR(64) NOT NULL default '',
            "pwd" VARCHAR(64) NOT NULL default '',
            "manufacturer" VARCHAR(64) NOT NULL default '',
            "model" VARCHAR(128) NOT NULL default '',
            "hardwareid" VARCHAR(128) NOT NULL default '',
            "firmwareversion" VARCHAR(128) NOT NULL default '',
            "serialnumber" VARCHAR(128)  NOT NULL default '',
            "source" VARCHAR(256)  NOT NULL default '',
            "rtmp" VARCHAR(256)  NOT NULL default '',
            "flv" VARCHAR(256)  NOT NULL default '',
            "hls" VARCHAR(256)  NOT NULL default '',
            "gop" INTEGER NOT NULL default 0,
            "encoding" VARCHAR(32)  NOT NULL default '',
            "ratio" VARCHAR(32)  NOT NULL default '',
            "fps" INTEGER NOT NULL default 0,
            "profile" VARCHAR(32)  NOT NULL default '',
            "quality" INTEGER NOT NULL default 0,
            "bitrate" INTEGER NOT NULL default 0,
            "transport" VARCHAR(32)  NOT NULL default udp,
            PRIMARY KEY ("id")
            );

insert into tbl_source (id) values (1);
insert into tbl_source (id) values (2);
insert into tbl_source (id) values (3); 
insert into tbl_source (id) values (4);
insert into tbl_source (id) values (5); 
insert into tbl_source (id) values (6); 
insert into tbl_source (id) values (7); 
insert into tbl_source (id) values (8); 
insert into tbl_source (id) values (9);
insert into tbl_source (id) values (10);
insert into tbl_source (id) values (11); 
insert into tbl_source (id) values (12);
insert into tbl_source (id) values (13); 
insert into tbl_source (id) values (14); 
insert into tbl_source (id) values (15); 
insert into tbl_source (id) values (16); 
"""

TBL_NAME = 'tbl_source'
DB_NAME = initres.SQLITEPATH + '/source.db'


class TblSource:

    def __init__(self):
        self.sqlbase = sqlitebase.SqliteBase(DB_NAME)

    def __del__(self):
        pass

    # 修改
    def modify(self, ids, dic):
        sql = sqlbase.dic2updatesql(dic, TBL_NAME) + " id = {} ".format(ids)
        return self.sqlbase.exec(sql)

    def delete(self, ids):
        """逻辑删除通道，把字段清空而已"""
        dic = {'name': '', 'url': '', 'port': 0, 'state': 0, 'username': '', 'pwd': '', 'manufacturer': '', 'model': '',
               'hardwareid': '', 'firmwareversion': '', 'serialnumber': '', 'source': '', 'rtmp': '', 'flv': '',
               'hls': '', 'gop': 0, 'encoding': '', 'ratio': '', 'fps': 0, 'profile': 0, 'quality': 0, 'bitrate': 0,
               'transport': 'udp'}
        return self.modify(ids, dic)

    # 获取所有信息
    def getAll(self):
        sql = "select * from {} limit 100".format(TBL_NAME)
        return self.sqlbase.exec_fetchall(sql)

    def modifyName(self, ids, name):
        sql = "update {} set name = \"{}\" where id = {}".format(TBL_NAME, name, ids)
        return self.sqlbase.exec_fetchall(sql)


sqlitebase.SqliteBase.initdb(DB_NAME, _DB_SCRIPT)


