# -*- coding: utf-8 -*-

from flask import make_response, jsonify


def _response_success_data(data):
    return {'success': True, 'code': 200, 'msg': 'success', 'data': data}


def _response_success():
    return {'success': True, 'code': 200, 'msg': 'success'}


def _response_error(msg, code):
    return {'success': False, 'msg': msg, 'code': code}


# --------------------------  成功 -----------------------------------

def make_response_success():
    return make_response(jsonify(_response_success()), 200)


def make_response_success_data(data):
    return make_response(jsonify(_response_success_data(data)), 200)


# --------------------------  通用错误码 -----------------------------------

def make_response_400():
    return make_response(jsonify(_response_error('请求无效', 400)), 400)


def make_response_401():
    return make_response(jsonify(_response_error('权限不足', 401)), 401)


def make_response_403():
    return make_response(jsonify(_response_error('禁止访问', 403)), 403)


def make_response_404():
    return make_response(jsonify(_response_error('请求不存在', 404)), 404)


def make_response_500():
    return make_response(jsonify(_response_error('无法连接到服务器', 500)), 500)


def make_response_1000():
    return make_response(jsonify(_response_error('操作失败', 1000)), 200)


# ---------------------  onvif 模块 ----------------------------------------
def make_response_1100():
    return make_response(jsonify(_response_error('连接超时', 1100)), 200)


def make_response_1102():
    return make_response(jsonify(_response_error('鉴权失败', 1102)), 200)


