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

def main():
    # Parse arguments
    args = parse_args()
    
    # Create output directory
    output_path = f"{args.output_dir}/{args.concept.replace(' ', '_')}"
    os.makedirs(output_path, exist_ok=True)
    
    # Setup grid parameters
    res = args.res
    cell_size = args.cell_size
    grid_size = (res + 1) * cell_size
    
    # Create grid and mapping
    grid_image, positions = utils.create_grid_image(res=res, cell_size=cell_size, header_size=cell_size)
    cells_to_pixels_map = utils.cells_to_pixels(res, cell_size, header_size=cell_size)
    
    # Call LLM to generate sketch
    print(f"Generating sketch for: {args.concept}")
    prompt = sketch_first_prompt.format(concept=args.concept, gt_sketches_str=gt_example)
    system = system_prompt.format(res=res)
    
    # Get LLM response
    llm_output = llm_call(prompt=prompt, system_prompt=system)
    
    # Save raw LLM output
    with open(f"{output_path}/llm_output.txt", "w") as f:
        f.write(llm_output)
    
    # Extract DSL from response
    if "<strokes>" in llm_output and "</strokes>" in llm_output:
        # Parse DSL to get strokes and t-values
        strokes_list_str, t_values_str = utils.parse_xml_string(llm_output, res)
        
        # Convert to Python objects
        import ast
        strokes_list = ast.literal_eval(strokes_list_str)
        t_values = ast.literal_eval(t_values_str)
        
        # Get control points for SVG
        control_points = utils.get_control_points(strokes_list, t_values, cells_to_pixels_map)
        
        # Convert to SVG
        svg_content = utils.format_svg(control_points, dim=(grid_size, grid_size), stroke_width=args.stroke_width)
        
        # Save SVG
        svg_path = f"{output_path}/{args.concept.replace(' ', '_')}.svg"
        with open(svg_path, "w") as f:
            f.write(svg_content)
        
        # Generate PNG
        png_path = f"{output_path}/{args.concept.replace(' ', '_')}.png"
        cairosvg.svg2png(url=svg_path, write_to=png_path, background_color="white")
        
        # Generate PNG with grid
        canvas_png_path = f"{output_path}/{args.concept.replace(' ', '_')}_canvas.png"
        cairosvg.svg2png(url=svg_path, write_to=canvas_png_path)
        foreground = Image.open(canvas_png_path)
        grid_image.paste(Image.open(canvas_png_path), (0, 0), foreground)
        grid_image.save(canvas_png_path)
        
        # Save experiment log
        log_data = {
            "concept": args.concept,
            "llm_output": llm_output,
            "strokes": strokes_list,
            "t_values": t_values
        }
        with open(f"{output_path}/experiment_log.json", "w") as f:
            json.dump(log_data, f, indent=4)
        
        print(f"Sketch generated and saved to {output_path}")
    else:
        print("No valid sketch DSL found in LLM output")

if __name__ == "__main__":
    main()
