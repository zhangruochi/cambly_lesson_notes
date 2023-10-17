#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /home/richard/projects/cambly/src/extraction.py
# Project: /home/richard/projects/cambly/src
# Created Date: Tuesday, October 17th 2023, 2:17:52 pm
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
import os
from dotenv import load_dotenv

import openai
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import ReduceDocumentsChain, MapReduceDocumentsChain

from tqdm import tqdm

# load .env
load_dotenv()


class LessonsNoteGenerator():

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

    def generate_dialogue(self):

        template = """
            The text delimited by triple single quotes is a real conversation between two people, one being an English tutor and the other a student. The student want the tutor to help him improve his spoken english. Please organize the conversation between the two and use the output format I provide.

            '''{sample_text}'''
            
            IMPORTANT: Do not modify any words or phrases in the conversation, do not rephrase the sentences.

            OUTPUT FORMAT:
            ```
            **Tutor**: <The sentences tutor have talked about>

            **Student**: <The sentences student have talked about>

            **Tutor**: <The sentences tutor have talked about>

            **Student**: <The sentences student have talked about>

            continue the above format until the end of the conversation.
            
            ```
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

        return "\n".join(dialogues)

    def generate_summary(self):

        # Map
        map_template = """The following text delimited by triple single quotes is a set of dialogues between an english tutor and a student:

        ```
        {docs}
        ```
        
        I want to summarize the key points in the conversation and create a english learning note. Please help the student identify the advanced words and phrases that appeared in the conversation. For any sentence the student said, please help the student to correct the grammar and rephrase the sentence in a more authentic way. 
        You should use the following output format:

        ```
        ### words and phrases:
        1. **word or phrase 1**:
        2. **word or phrase 2**:

        continue to find the words and phrases until the end of the conversation.
        
        ### Expression1:
        - Original: <original sentence 1>
        - Authentic: <more authentic expression 1>

        ### Expression2:
        - Original: <original sentence 2>
        - Authentic: <more authentic expression 2>

        continue to find all the expressions until the end of the conversation.

        Output:
        """

        map_prompt = PromptTemplate.from_template(map_template)
        map_chain = LLMChain(llm=self.llm, prompt=map_prompt, verbose=True)

        # Reduce
        reduce_template = """The following text delimited by triple single quotes is set of Key words、phrases and expressions:

        '''
        {docs}
        '''
        
        Take these and organize them into a summary of the lesson note. Please use the following output format:
        
        ```
        ### words and phrases:
        1. **word or phrase 1**
        2. **word or phrase 2**

        please list all the words and phrases
        
        ### Expression1:
        - Original: <original sentence 1>
        - Authentic: <more authentic expression 1>

        ### Expression2:
        - Original: <original sentence 2>
        - Authentic: <more authentic expression 2>

        please list all the expressions

        Output:
        """
        reduce_prompt = PromptTemplate.from_template(reduce_template)

        # Run chain
        reduce_chain = LLMChain(llm=self.llm,
                                prompt=reduce_prompt,
                                verbose=True)

        # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="docs")

        # Combines and iteravely reduces the mapped documents
        reduce_documents_chain = ReduceDocumentsChain(
            # This is final chain that is called.
            combine_documents_chain=combine_documents_chain,
            # If documents exceed context for `StuffDocumentsChain`
            collapse_documents_chain=combine_documents_chain,
            # The maximum number of tokens to group documents into.
            token_max=8000,
        )

        # Combining documents by mapping a chain over them, then combining results
        map_reduce_chain = MapReduceDocumentsChain(
            # Map chain
            llm_chain=map_chain,
            # Reduce chain
            reduce_documents_chain=reduce_documents_chain,
            # The variable name in the llm_chain to put the documents in
            document_variable_name="docs",
            # Return the results of the map steps in the output
            return_intermediate_steps=False,
        )

        lesson_note = map_reduce_chain.run(self.text_chunks)

        return lesson_note

    def generate_notes(self):

        dialogues = self.generate_dialogue().strip()
        summary = self.generate_summary().strip()

        # combine the dialogues and summary into a single document with markdown formatting

        notes = f"""# Lesson Notes\n\n## Dialogues\n{dialogues}\n\n## Summary\n{summary}\n"""

        return notes

    def run(self, output):
        with open(output, "w") as f:
            f.write(self.generate_notes())
