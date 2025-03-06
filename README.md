# SketchAgent with In-Context Learning
Forked from yael-vinker/sketch-agent

## Setup

```bash
conda env create -f mac-environment.yml
```

Download dataset:

```bash
mkdir .data; cd .data; mkdir quickdraw; cd quickdraw; mkdir simplified; cd simplified;
gsutil -m cp -r gs://quickdraw_dataset/full/simplified/* .
```

Setup `.env` file:

Add your OpenAI API key to the `.env` file:

## Usage

In Context Learning:
```bash
python icl_sketch.py --concept "airplane" --examples 3
```

Simple Sketch:
```bash
python simple_sketch.py --concept "airplane"
```

Read more about the [DSL](./DSL.md)







