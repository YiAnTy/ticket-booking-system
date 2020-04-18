# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Yao Tong
# Created Time: 2020-4-18
'''
BEGIN
function:
    Comment API
return:
    code:0 success
END
'''

import time
import random
from flask import Flask, request, jsonify
from nameko.standalone.rpc import ClusterRpcProxy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="app running port", type=int, default=5000)
parse_args = parser.parse_args()

app = Flask(__name__)

CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}


@app.route('/api/v1/register', methods=['POST'])
def register():
    """
    Register API

    Parameters Explain:

        timestamp    注册时间
        email        注册邮箱
        name         名称
        language     语言
        country      国家
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: data
          properties:
            timestamp:
              type: integer
            email:
              type: string
            name:
              type: string
            language:
              type: string
            country:
              type: string
    responses:
      code:
        description: 0 register success.
      message:
        description: Error Message!
      data:
          description: return u_id
    """

    user_data = request.json
    email = user_data.get("email")
    code, message = 0, ""
    if not email:
        code, message = 10000, "email is null."
        response = dict(code=code, message=message, data="")
        return jsonify(response)
    u_id = None
    with ClusterRpcProxy(CONFIG) as rpc:
        u_id, message = rpc.register.register(email, user_data)
    if message:
        code = 10001
    data = dict(u_id=u_id)
    response = dict(code=code, message=message, data=data)
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(parse_args.port), debug=True)
