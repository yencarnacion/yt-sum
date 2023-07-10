# yt-sum.py - YouTube Video Summarizer

This is a Python script that summarizes a youtube video from a YouTube URL
using llamaindex.

## Prerequisites

OpenAI API Key
Python 3.6 or later.

## Installation

Before running the script, you need to install the required Python libraries.

1. Open a terminal.
2. Navigate to the project directory where `requirements.txt` is located.
3. Run the following command:

```bash
pip install -r requirements.txt
```

This will install the required libraries

Also

```bash
cp env.example env.py
```

And enter your openai API Key into the variable OPENAI_API_KEY in env.py

Usage
To summarize a YouTube video, you need to provide the YouTube URL as an argument
when you run the go.sh script.

Here is an example of how to run the script:

```bash
./go.sh https://www.youtube.com/watch?v=wbiEGHjlE4Y
```

This command will generate an output.html file in the ./output directory.

Note:

The script is a work in progress.  It blows up on certain videos for reasons I
have not debugged yet.  Also, if you pass a url with the character &amp;
on *nix, it will give an
error (e.g., https://www.youtube.com/watch?v=-hxeDjAxvJ8&t=108s ).
This is a *nix thing I will correct at some later point in time.

The prompts that follow were copied from https://github.com/daveshap/Quickly_Extract_Science_Papers which has an MIT license.
```
>>>
can you give me a very clear explanation of the core assertions, implications, and mechanics elucidated in this paper?
<<<
---
>>>
can you explain the value of this in basic terms? Like you're talking to a ceo. so what? what's the bottom line here?
<<<
---
can you give me an analogy or metaphor that will help explain this to a broad audience
<<<
```