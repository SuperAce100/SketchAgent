import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import dataloader
import utils
import matplotlib.pyplot as plt
from simple_sketch import make_sketch
from prompts import gt_example, icl_example

def choose_examples(concept: str, n: int):
    most_similar = dataloader.most_similar_categories(concept, n=n)
    categories = [cat for cat, _ in most_similar]
    examples = []
    with ThreadPoolExecutor() as executor:
        future_to_category = {executor.submit(dataloader.quickdraw_to_dsl_file_pick_random, category): category for category in categories}
        for future in as_completed(future_to_category):
            result = future.result()
            category = future_to_category[future]
            examples.append((category, result))
    return examples

def format_example(example: tuple):
    category, dsl = example
    return f"<example>\n<concept>{category}</concept>\n{dsl}\n</example>"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concept", type=str, default="airplane", help="Concept to convert to DSL")
    parser.add_argument("--examples", type=int, default=3, help="Number of examples to show")
    parser.add_argument('--output_dir', type=str, default="results/icl", help="Output directory")
    parser.add_argument('--res', type=int, default=50, help="Grid resolution")
    parser.add_argument('--cell_size', type=int, default=12, help="Cell size in pixels")
    parser.add_argument('--stroke_width', type=float, default=7.0, help="Stroke width for SVG")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    examples = choose_examples(args.concept, args.examples)
    examples_prompt = "\n".join([format_example(example) for example in examples])
    icl_prompt = icl_example.format(gt_example=gt_example, examples=examples_prompt)
    print("Generating sketch for concept: ", args.concept)
    make_sketch(args.concept, args.output_dir, args.res, args.cell_size, args.stroke_width, icl_prompt)