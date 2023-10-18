# Note generator for Cambly lessons

this program is used to generate lesson notes from a video file recorded by Cambly app. This program is used to generate lesson notes from a video file recorded by Cambly app. The video file is first transcribed by Whisper, then the transcription is used to generate a lesson note by using OpenAI API. The lesson note is written in markdown format and then converted to pdf file.

# .env
```
OPENAI_API_KEY=sk-xxx
https_proxy=https://IP:PORT
model=gpt-3.5-turbo  # gpt-3.5-turbo, gpt-4
```


## Installation

```
pip install -U openai-whisper
conda install -c conda-forge ffmpeg
pip install setuptools-rust
pip install langchain
```

# Usage

``` 
python main.py 
```
