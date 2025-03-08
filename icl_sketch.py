import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import dataloader
import utils
import matplotlib.pyplot as plt
from simple_sketch import make_sketch
from prompts import gt_example, icl_example
import json
import random

def choose_examples(concept: str, n: int):
    # Load examples from JSON
    with open("examples.json", "r") as f:
        examples_data = json.load(f)
    
    # Get embeddings for all example concepts
    example_concepts = list(examples_data.keys())
    concept_embeddings = dataloader.generate_embeddings(", ".join(example_concepts))
    
    # Get embedding for target concept
    target_embedding = dataloader.generate_embedding(concept)[0]
    
    # Calculate similarities
    similarities = dataloader.cosine_similarity(concept_embeddings, target_embedding)
    
    # Sort by similarity and take top n
    sorted_examples = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:n]
    
    # Return random example from each similar concept
    examples = []
    for concept, _ in sorted_examples:
        example_dsl = random.choice(examples_data[concept])
        examples.append((concept, example_dsl))
    
    return examples

def format_example(example: tuple):
    category, dsl = example
    return f"<example>{dsl}\n</example>"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concept", type=str, default="airplane", help="Concept to convert to DSL")
    parser.add_argument("--examples", type=int, default=3, help="Number of examples to show")
    parser.add_argument('--output_dir', type=str, default="results/icl", help="Output directory")
    parser.add_argument('--res', type=int, default=50, help="Grid resolution")
    parser.add_argument('--cell_size', type=int, default=12, help="Cell size in pixels")
    parser.add_argument('--stroke_width', type=float, default=7.0, help="Stroke width for SVG")
    parser.add_argument('--model', type=str, default="anthropic/claude-3.5-sonnet", help="Model to use")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    examples = choose_examples(args.concept, args.examples)
    examples_prompt = "\n".join([format_example(example) for example in examples])
    for category, example in examples:
        utils.show_dsl_popup(example, args.res, args.cell_size, args.stroke_width, category)

    icl_prompt = icl_example.format(gt_example=gt_example, examples=examples_prompt)
    print("Generating sketch for concept: ", args.concept)
    make_sketch(args.concept, args.output_dir, args.res, args.cell_size, args.stroke_width, icl_prompt, args.model)