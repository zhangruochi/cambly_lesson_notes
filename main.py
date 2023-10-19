#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /home/richard/projects/cambly/main.py
# Project: /home/richard/projects/cambly
# Created Date: Tuesday, October 17th 2023, 11:17:12 am
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

from src.audio2text import WhisperDecode
from src.extraction import LessonsNoteGenerator
from src.utils import convert_markdown_to_pdf
from src.logger import StdLogger
import datetime
import os
import argparse






def main(input_file_path, log_dir):

    logger = StdLogger(file_path=os.path.join(
        log_dir, "{}-{}.log".format(
            os.path.basename(input_file_path).split(".")[0],
            datetime.datetime.now().strftime("%Y-%m-%d"))))

    model = "small.en"
    transcription_output_path = os.path.join(
        os.path.dirname(input_file_path),
        os.path.basename(input_file_path).split(".")[0] + ".txt")

    if not os.path.exists(transcription_output_path):
        whisper = WhisperDecode(model)
        transcription = whisper.transcribe(input_file_path,
                                       transcription_output_path)
        logger.std_print(transcription)
        logger.std_print(logger)

    else:
        with open(transcription_output_path, "r") as f:
            transcription = f.read()

    lesson_note_output_path = os.path.join(
        os.path.dirname(input_file_path),
        os.path.basename(input_file_path).split(".")[0] + "-lesson-note.md")
    lesson_note_generator = LessonsNoteGenerator(transcription=transcription, logger = logger)
    lesson_note_generator.run(lesson_note_output_path)

    convert_markdown_to_pdf(lesson_note_output_path,
                            lesson_note_output_path.replace(".md", ".pdf"))


if __name__ == "__main__":

    # use argparse to parse command line arguments
    parser = argparse.ArgumentParser(description='Cambly lesson note generator')
    parser.add_argument('-i', '--input', help='input audio file path', required=True)
    parser.add_argument('-l', '--log_dir', help='log directory', default="logs", required=False)

    args = parser.parse_args()
    main(args.input, args.log_dir)
