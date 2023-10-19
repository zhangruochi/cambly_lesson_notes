#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /home/richard/projects/cambly/src/utils.py
# Project: /home/richard/projects/cambly/src
# Created Date: Tuesday, October 17th 2023, 5:40:34 pm
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

import subprocess
import sys
import json

import markdown
import pdfkit

from langchain.text_splitter import RecursiveCharacterTextSplitter


def is_json(text):
    try:
        json.loads(text)
    except:
        return False
    return True


def create_chunks(text_content: str = ""):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
    )

    text_chunks = text_splitter.create_documents([text_content])
    return text_chunks


def convert_markdown_to_pdf(input_file, output_file):
    # 从文件读取 markdown 内容
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 使用 markdown 库将其转换为 html
    html_content = markdown.markdown(md_content)

    # 使用 pdfkit 将 html 转换为 pdf
    pdfkit.from_string(html_content, output_file)


def convert_markdown_to_docx(input_file, output_file):
    try:
        result = subprocess.run(['pandoc', input_file, '-o', output_file],
                                check=True)
        if result.returncode == 0:
            print(f"Successfully converted {input_file} to {output_file}")
        else:
            print("Conversion failed.")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
    except FileNotFoundError:
        print("Pandoc not found. Ensure it's installed and available in PATH.")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script_name.py input_file.md output_file.docx")
        sys.exit(1)

    input_md_file = sys.argv[1]
    output_file = sys.argv[2]

    # convert_markdown_to_docx(input_md_file, output_docx_file)

    convert_markdown_to_pdf(input_md_file, output_file)