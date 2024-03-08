# FOS-itive vibes only

## Installation

1. `pip install -r requirements.txt`

2. Sign up to huggingface, aggree to the T&Cs for https://huggingface.co/google/gemma-7b and place an authentication token at `~/.cache/huggingface/token`.

3. Ask the repository maintainer to share the chroma vector db files with you.

## Usage

For development and testing:

```shell
./fositive-vibes-only test
```

For the actual app:

```shell
./fositive-vibes-only llm
```

This will launch a chat application in your browser.
