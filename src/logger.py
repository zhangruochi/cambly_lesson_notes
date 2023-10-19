#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /home/richard/projects/cambly/src/logger.py
# Project: /home/richard/projects/cambly/src
# Created Date: Thursday, October 19th 2023, 10:20:56 pm
# Author: Ruochi Zhang
# Email: zrc720@gmail.com
# -----
# Last Modified: Thu Oct 19 2023
# Modified By: Ruochi Zhang
# -----
# Copyright (c) 2023 Bodkin World Domination Enterprises
#
# MIT License
#
# Copyright (c) 2023 Ruochi Zhang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----
###
import logging


class StdLogger():

    def __init__(self, file_path="", stream=False, level=logging.INFO):
        formatter = logging.Formatter(fmt='%(asctime)s %(message)s',
                                      datefmt="%H:%M:%S")
        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(level)
        self.file_path = file_path

        if file_path:
            file_hander = logging.FileHandler(file_path)
            file_hander.setFormatter(formatter)
            self.logger.addHandler(file_hander)

        if stream:
            stream_handler = logging.StreamHandler(stream=sys.stderr)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

    def std_print(self, str_):
        """ Print to stdout
        """
        self.logger.info(str_)
