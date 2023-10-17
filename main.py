#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /home/richard/projects/cambly/main.py
# Project: /home/richard/projects/cambly
# Created Date: Tuesday, October 17th 2023, 11:17:12 am
# Author: Ruochi Zhang
# Email: zrc720@gmail.com
# -----
# Last Modified: Tue Oct 17 2023
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
from time import time
import os


def main():

    model = "base"
    input_file_path = "./lessons/2023-10-17-Zariah.mp4"
    transcription_output_path = os.path.join(
        os.path.dirname(input_file_path),
        os.path.basename(input_file_path).split(".")[0] + ".txt")

    if not os.path.exists(transcription_output_path):
        whisper = WhisperDecode(model)
        transcription = whisper.decode(input_file_path,
                                       transcription_output_path)
        print("Transcription complete!")
    else:
        with open(transcription_output_path, "r") as f:
            transcription = f.read()

    lesson_note_output_path = os.path.join(
        os.path.dirname(input_file_path),
        os.path.basename(input_file_path).split(".")[0] + "-lesson-note.md")
    lesson_note_generator = LessonsNoteGenerator(text_content=transcription)
    lesson_note_generator.run(lesson_note_output_path)

    convert_markdown_to_pdf(lesson_note_output_path,
                            lesson_note_output_path.replace(".md", ".pdf"))


if __name__ == "__main__":

    main()