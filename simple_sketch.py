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
    print(f"Starting sketch generation with arguments: {args}")
    
    # Create output directory
    output_path = f"{args.output_dir}/{args.concept.replace(' ', '_')}"
    os.makedirs(output_path, exist_ok=True)
    print(f"Created output directory at: {output_path}")
    
    # Setup grid parameters
    res = args.res
    cell_size = args.cell_size
    grid_size = (res + 1) * cell_size
    print(f"Grid setup - resolution: {res}, cell size: {cell_size}, grid size: {grid_size}")
    
    # Create grid and mapping
    print("Creating grid image and position mapping...")
    grid_image, positions = utils.create_grid_image(res=res, cell_size=cell_size, header_size=cell_size)
    cells_to_pixels_map = utils.cells_to_pixels(res, cell_size, header_size=cell_size)
    
    # Call LLM to generate sketch
    print(f"Generating sketch for concept: {args.concept}")
    prompt = sketch_first_prompt.format(concept=args.concept, gt_sketches_str=gt_example)
    system = system_prompt.format(res=res)
    
    # Track messages
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]
    
    # Get LLM response
    print("Calling LLM to generate sketch...")
    llm_output = llm_call(prompt=prompt, system_prompt=system)
    messages.append({"role": "assistant", "content": llm_output})
    print("Received LLM response")
    
    # Save raw LLM output
    with open(f"{output_path}/llm_output.txt", "w") as f:
        f.write(llm_output)
    print("Saved raw LLM output")
    
    # Extract DSL from response
    if "<strokes>" in llm_output and "</strokes>" in llm_output:
        print("Parsing DSL from LLM response...")
        # Parse DSL to get strokes and t-values
        strokes_list_str, t_values_str = utils.parse_xml_string(llm_output, res)
        
        # Convert to Python objects
        import ast
        strokes_list = ast.literal_eval(strokes_list_str)
        t_values = ast.literal_eval(t_values_str)
        print(f"Parsed {len(strokes_list)} strokes from DSL")
        
        # Get control points for SVG
        print("Calculating control points...")
        control_points = utils.get_control_points(strokes_list, t_values, cells_to_pixels_map)
        
        # Convert to SVG
        print("Generating SVG content...")
        svg_content = utils.format_svg(control_points, dim=(grid_size, grid_size), stroke_width=args.stroke_width)
        
        # Save SVG
        svg_path = f"{output_path}/{args.concept.replace(' ', '_')}.svg"
        with open(svg_path, "w") as f:
            f.write(svg_content)
        print(f"Saved SVG to {svg_path}")
        
        # Generate PNG
        png_path = f"{output_path}/{args.concept.replace(' ', '_')}.png"
        cairosvg.svg2png(url=svg_path, write_to=png_path, background_color="white")
        print(f"Generated PNG at {png_path}")
        
        # Generate PNG with grid
        canvas_png_path = f"{output_path}/{args.concept.replace(' ', '_')}_canvas.png"
        cairosvg.svg2png(url=svg_path, write_to=canvas_png_path)
        foreground = Image.open(canvas_png_path)
        grid_image.paste(Image.open(canvas_png_path), (0, 0), foreground)
        grid_image.save(canvas_png_path)
        print(f"Generated PNG with grid at {canvas_png_path}")
        
        # Save experiment log
        log_data = {
            "concept": args.concept,
            "messages": messages,  # Track all messages
            "llm_output": llm_output,
            "strokes": strokes_list,
            "t_values": t_values
        }
        with open(f"{output_path}/experiment_log.json", "w") as f:
            json.dump(log_data, f, indent=4)
        print("Saved experiment log")
        
        print(f"Sketch generation complete! Results saved to {output_path}")
    else:
        print("Error: No valid sketch DSL found in LLM output")

if __name__ == "__main__":
    main()
