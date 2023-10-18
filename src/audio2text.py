#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /home/richard/projects/cambly/src/main.py
# Project: /home/richard/projects/cambly/src
# Created Date: Tuesday, October 17th 2023, 10:01:48 am
# Author: Ruochi Zhang
# Email: zrc720@gmail.com
# -----
# Last Modified: Wed Oct 18 2023
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
import os

import whisper
import openai


class WhisperDecode():

    def __init__(self, model="base", device="cuda:0"):
        self.model = whisper.load_model(model, device=device)

        # Transcription
    def transcribe(self, input_file_path, output_file_path):

        # Get the size of the file in bytes
        file_size = os.path.getsize(input_file_path)

        # Convert bytes to megabytes
        file_size_in_mb = file_size / (1024 * 1024)
        # Check if the file size is less than 25 MB

        if file_size_in_mb < 200:
            result = self.model.transcribe(input_file_path, verbose = True)["text"]

        else:
            result = "Please provide a smaller audio file (less than 200mb)."

        with open(output_file_path, "w") as f:
            f.write(result)

        return result
