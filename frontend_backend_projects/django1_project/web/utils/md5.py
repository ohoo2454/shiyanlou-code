#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib


# md5加密
def gen_md5(origin):
    """
    md5加密
    :param origin:
    :return:
    """
    md_5 = hashlib.md5(b'jk3usodfjwkrsdf')
    md_5.update(origin.encode('utf-8'))
    return md_5.hexdigest()
    