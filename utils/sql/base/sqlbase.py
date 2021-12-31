# -*- coding: utf-8 -*-

###########################################################################
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
###########################################################################

"""
sql base
"""


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def dic2insertsql(dic, tblname):
    sql_key = ', '.join(dic.keys())
    sql_val = ''
    for key in dic:
        if type(dic[key]) is str:
            sql_val = sql_val + '\'' + dic[key] + '\','
        else:
            sql_val = sql_val + str(dic[key]) + ' ,'

    # 移除 sql_val最后一个 ','
    return "insert into {} ({}) values ({}) ".format(tblname, sql_key, sql_val[:-1])


# 调用者需要自己补充 where之后的条件语句
def dic2updatesql(dic, tblname):
    sql_key = ''
    for key in dic:
        if type(dic[key]) is str:
            sql_key = sql_key + key + ' = \'' + dic[key] + '\','
        else:
            sql_key = sql_key + key + ' = ' + str(dic[key]) + ' ,'

    # 移除 sql_key 最后一个 ','
    return "update {} set {} where  ".format(tblname, sql_key[:-1])


def dic2replacesql(dic, tblname):
    sql_key = ', '.join(dic.keys())
    sql_val = ''
    for key in dic:
        if type(dic[key]) is str:
            sql_val = sql_val + '\'' + dic[key] + '\','
        else:
            sql_val = sql_val + str(dic[key]) + ' ,'

    # 移除 sql_val最后一个 ','
    return "replace into {} ({}) values ({}) ".format(tblname, sql_key, sql_val[:-1])
