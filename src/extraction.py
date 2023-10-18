#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /home/richard/projects/cambly/src/extraction.py
# Project: /home/richard/projects/cambly/src
# Created Date: Tuesday, October 17th 2023, 2:17:52 pm
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
from dotenv import load_dotenv

import openai
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from tqdm import tqdm
import json
from typing import Dict, List
from collections import defaultdict

# load .env
load_dotenv()


class LessonsNoteGenerator():
    """
    This module defines the LessonsNoteGenerator class, which is responsible for generating dialogue, summary, and comments for a given text content. The class uses the ChatOpenAI and LLMChain models to generate the output. 

    Attributes:
        text_content (str): The text content to be processed.

    Methods:
        __init__(self, text_content: str = ""): Initializes the LessonsNoteGenerator object.
        preprocess(self, text_content: str = ""): Preprocesses the text content by splitting it into chunks.
        generate_dialogue(self) -> Dict: Generates a dialogue between an English tutor and a student using the given text content.
        generate_summary(self) -> Dict: Generates a summary of the given text content by identifying advanced words and phrases and correcting grammar and rephrasing expressions.
        generate_comments(self) -> str: Generates comments on the less authentic parts of the students' expressions and provides suggestions on how to improve their English speaking skills.
    """

    def __init__(self, text_content: str = ""):

        self.llm = ChatOpenAI(model_name=os.getenv("model"),
                              temperature=0,
                              openai_api_key=os.getenv("OPENAI_API_KEY"))

        self.text_chunks = self.preprocess(text_content)

    def preprocess(self, text_content: str = ""):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False,
        )

        text_chunks = text_splitter.create_documents([text_content])
        return text_chunks

    def generate_dialogue(self) -> Dict:

        template = """
            The text delimited by triple single quotes is a real conversation between two people, one being an English tutor and the other a student. The student want the tutor to help him improve his spoken english. Please organize the conversation between the two and use the output format I provide.

            '''{sample_text}'''
            
            IMPORTANT: Do not modify any words or phrases in the conversation, do not rephrase the sentences. Folloing the JSON format below strictly is the key to success.

            OUTPUT JSON FORMAT:
            {{
                dialogues: [
                    {{tutor: <tutor's expression 1>, student: <student's expression 1>}},
                    {{tutor: <tutor's expression 2>, student: <student's expression 2>}},
                    {{tutor: <tutor's expression 3>, student: <student's expression 3>}},
                    ... 
            }}
            Output:
            """
        prompt_template = PromptTemplate.from_template(template=template)

        # initialize LLMChain by passing LLM and prompt template
        llm_chain = LLMChain(llm=self.llm,
                             prompt=prompt_template,
                             verbose=True)

        dialogues = []
        for text in tqdm(self.text_chunks,
                         total=len(self.text_chunks),
                         desc="Generating dialogues"):
            dialogues.append(llm_chain.run(text.page_content))

        dialogues_dict = defaultdict(list)
        for _ in dialogues:
            _ = json.loads(_)
            dialogues_dict["dialogues"].extend(_["dialogues"])

        return dialogues_dict

    def generate_summary(self) -> Dict:

        # Map
        map_template = """The following text delimited by triple single quotes is a set of dialogues between an english tutor and a student:

        ```
        {docs}
        ```
        
        Please identify the advanced words and phrases that appeared in the conversation. For each paragraph spoken by the student(do not separate into sentences, use the students' each complete expression.), please correct the grammar and rephrase the expression in a more native and authentic way. 
        IMPORTANT: Folloing the JSON format below strictly is the key to success:

        ```
        {{
            "words": [
                {{"word": <word1>, "definition": <definition1>}},
                {{"word": <word2>, "definition": <definition2>}},
                {{"word": <word3>, "definition": <definition3>}},
                ...
            ]
            "phrases": [
                {{"phrase": <phrase1>, "definition": <definition1>}},
                {{"phrase": <phrase2>, "definition": <definition2>}},
                {{"phrase": <phrase3>, "definition": <definition3>}},
                ...
            ]
            "expressions": [
                {{"original": <original expression 1>, "authentic": <more authentic expression 1>}},
                {{"original": <original expression 2>, "authentic": <more authentic expression 2>}},
                {{"original": <original expression 3>, "authentic": <more authentic expression 3>}},
                ...
            ]
        }}
        ```     
        Output:
        """

        map_prompt = PromptTemplate.from_template(map_template)
        llm_chain = LLMChain(llm=self.llm, prompt=map_prompt, verbose=True)

        json_notes_list = []
        for text in tqdm(self.text_chunks,
                         total=len(self.text_chunks),
                         desc="Generating dialogues"):
            json_notes_list.append(llm_chain.run(text.page_content))

        lesson_note = defaultdict(list)
        for _ in json_notes_list:
            _ = json.loads(_)
            for key in _:
                lesson_note[key].extend(_[key])

        return lesson_note

    def generate_comments(self) -> str:

        map_template = """I will give you some dialogues between students and an English teacher. Your task is to find the less authentic parts of the students' expressions and provide some comments.
        {text}

        Output:
        """
        map_prompt = PromptTemplate.from_template(map_template)

        combine_prompt = """The following text contains some less authentic expressions and detailed comments given by the English teacher. Please use this content to create a comprehensive feedback report and provide suggestions on how students can improve their English speaking skills, preferably using students' expressions as examples.
        {text}

        Output:
        """

        combine_prompt = PromptTemplate.from_template(combine_prompt)

        llm_chain = load_summarize_chain(
            self.llm,
            chain_type="map_reduce",
            map_prompt=map_prompt,
            combine_prompt=combine_prompt,
            combine_document_variable_name="text",
            map_reduce_document_variable_name="text")

        comments = llm_chain.run(self.text_chunks)

        return comments

    def generate_notes(self) -> str:

        dialogues = self.generate_dialogue()
        summary = self.generate_summary()
        comments = self.generate_comments()

        dialogues_text = ""
        for _ in dialogues["dialogues"]:
            dialogues_text += "**Tutor**: " + _["tutor"] + "\n\n"
            dialogues_text += "**Student**: " + _["student"] + "\n\n"

        cache = set()

        summary_text = ""
        summary_text += "###Words:\n"
        for _ in summary["words"]:
            if _["word"] in cache:
                continue

            summary_text += "**{}**: ".format(
                _["word"]) + _["definition"] + "\n\n"

            cache.add(_["word"])

        summary_text += "###Phrases:\n"
        for _ in summary["phrases"]:
            if _["phrase"] in cache:
                continue

            summary_text += "**{}**: ".format(
                _["phrase"]) + _["definition"] + "\n\n"

            cache.add(_["phrase"])

        expression_text = ""
        for _ in summary["expressions"]:
            expression_text += "**Original**: " + _["original"] + "\n\n"
            expression_text += "**Authentic**: " + _["authentic"] + "\n\n\n"

        # combine the dialogues and summary into a single document with markdown formatting

        notes = f"""# Lesson Notes\n\n##Dialogues:\n{dialogues_text}\n\n##Advanced words and phrases:\n{summary_text}\n\n##Expressions:\n{expression_text}\n\n## Comments\n{comments}\n"""

        return notes

    def run(self, output):
        """
        Writes the notes generated by `generate_notes` to a file at the given `output` path.

        Args:
            output (str): The path to the file where the notes will be written.
        """
        with open(output, "w") as f:
            f.write(self.generate_notes())
