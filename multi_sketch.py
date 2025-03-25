import argparse
from datetime import datetime
import os
from simple_sketch import make_sketch
import utils
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import cv2


RES = 10
CELL_SIZE = 10
STROKE_WIDTH = 1


def image_viewer(image_paths):
    """
    Opens images one by one in a popup window with keyboard navigation.
    
    Controls:
    - Right arrow or 'n': Next image
    - Left arrow or 'p': Previous image
    - ESC or 'q': Quit
    
    Args:
        image_paths (list): List of paths to image files
    """
    if not image_paths:
        print("No images provided")
        return
    
    current_index = 0
    total_images = len(image_paths)
    
    # Create a named window
    window_name = "Image Viewer (Press 'n' for next, 'p' for previous, 'q' to quit)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    while True:
        # Try to load and display the current image
        try:
            img = cv2.imread(image_paths[current_index])
            if img is None:
                print(f"Failed to load image: {image_paths[current_index]}")
                if current_index + 1 < total_images:
                    current_index += 1
                    continue
                else:
                    break
            
            # Resize large images to fit screen better
            height, width = img.shape[:2]
            max_height, max_width = 900, 1600
            if height > max_height or width > max_width:
                scale = min(max_height / height, max_width / width)
                img = cv2.resize(img, (int(width * scale), int(height * scale)))
            
            # Show image title in window
            cv2.setWindowTitle(window_name, f"{window_name} - {current_index + 1}/{total_images}: {image_paths[current_index]}")
            cv2.imshow(window_name, img)
            
        except Exception as e:
            print(f"Error displaying image {image_paths[current_index]}: {e}")
            if current_index + 1 < total_images:
                current_index += 1
                continue
            else:
                break
        
        # Wait for key press
        key = cv2.waitKey(0) & 0xFF
        
        # Handle navigation keys
        if key == ord('q') or key == 27:  # q or ESC
            break
        elif key == ord('n') or key == 83:  # n or right arrow
            current_index = (current_index + 1) % total_images
        elif key == ord('p') or key == 81:  # p or left arrow
            current_index = (current_index - 1) % total_images
    
    cv2.destroyAllWindows()

def n_sketches(n: int, concept: str, model: str="anthropic/claude-3.5-sonnet"):
    """
    Make n sketches for a given concept.
    """
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(make_sketch, concept, RES, CELL_SIZE, STROKE_WIDTH, model) for _ in range(n)]
        results = [future.result() for future in tqdm(as_completed(futures), total=n) if future.result()]
    return results

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--concept", type=str, default="cat")
    parser.add_argument("--model", type=str, default="anthropic/claude-3.5-sonnet")
    parser.add_argument("--output_dir", type=str, default=f"results/multi/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    return parser.parse_args()


if __name__ == "__main__":


    args = parse_args()
    results = n_sketches(args.n, args.concept, args.model)
    output_path = f"{args.output_dir}/{args.concept.replace(' ', '_')}"
    os.makedirs(output_path, exist_ok=True)

    for i, result in enumerate(results):
        new_output_path = f"{output_path}/{i}"
        os.makedirs(new_output_path, exist_ok=True)
        (strokes_list, t_values, svg_content), llm_output, messages = result
        grid_image, positions = utils.create_grid_image(res=RES, cell_size=CELL_SIZE, header_size=CELL_SIZE)

        utils.save_results(new_output_path, args.concept, llm_output, messages, strokes_list, t_values, svg_content, grid_image)

    
    image_paths = [f"{output_path}/{i}/{args.concept}.png" for i in range(len(results))]

    image_viewer(image_paths)

