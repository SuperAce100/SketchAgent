import os
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

import argparse
import os
import json
import cairosvg
from PIL import Image
import utils
from models import llm_call
from prompts import sketch_first_prompt, system_prompt, gt_example

def parse_args():
    parser = argparse.ArgumentParser(description='Simple Sketch Generator')
    parser.add_argument('--concept', type=str, default="cat", help="Concept to draw")
    parser.add_argument('--output_dir', type=str, default="results/simple", help="Output directory")
    parser.add_argument('--res', type=int, default=50, help="Grid resolution")
    parser.add_argument('--cell_size', type=int, default=12, help="Cell size in pixels")
    parser.add_argument('--stroke_width', type=float, default=7.0, help="Stroke width for SVG")
    return parser.parse_args()

def make_sketch(concept: str, output_path: str, res: int, cell_size: int, stroke_width: float, examples: str=gt_example) -> None:
    """
    Make a sketch for a given concept.

    Args:
        `concept`: Concept to draw.
        `output_path`: Output directory.
        `res`: Grid resolution.
        `cell_size`: Cell size in pixels.
        `stroke_width`: Stroke width for SVG.
    """
    output_path = f"{output_path}/{concept.replace(' ', '_')}"
    os.makedirs(output_path, exist_ok=True)

        
    # LLM Call
    prompt = sketch_first_prompt.format(concept=concept, examples=examples)
    system = system_prompt.format(res=res)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]
    llm_output = llm_call(prompt=prompt, system_prompt=system)
    messages.append({"role": "assistant", "content": llm_output})
    
    grid_size = (res + 1) * cell_size
    grid_image, positions = utils.create_grid_image(res=res, cell_size=cell_size, header_size=cell_size)
    cells_to_pixels_map = utils.cells_to_pixels(res, cell_size, header_size=cell_size)
    # Process and save results
    result = utils.parse_dsl(llm_output, res, cells_to_pixels_map, grid_size, stroke_width)
    if result:
        strokes_list, t_values, svg_content = result
        utils.save_results(output_path, concept, llm_output, messages, strokes_list, t_values, svg_content, grid_image)
        print(f"Sketch generation complete! Results saved to {output_path}")
    else:
        print("Error: No valid sketch DSL found in LLM output")

def main():
    args = parse_args()
    make_sketch(args.concept, args.output_dir, args.res, args.cell_size, args.stroke_width)

if __name__ == "__main__":
    main()
