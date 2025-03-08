from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from typing import Dict, List
import json
import argparse
from matplotlib import pyplot as plt
import numpy as np
from openai import OpenAI
import utils
from functools import lru_cache
from tqdm import tqdm
QUICKDRAW_DATASET_PATH = ".data/quickdraw_dataset/simplified"
client = OpenAI()

# ================================
# Category Handling Functions
# ================================

@lru_cache(maxsize=None)
def load_categories():
    with open(f"{QUICKDRAW_DATASET_PATH}/../categories.txt", "r") as f:
        return [line.strip() for line in f]
    
@lru_cache(maxsize=None)
def generate_embedding(text: str):
    """
    Uses OpenAI API to get embeddings for each category
    """
    embeddings = client.embeddings.create(input=text, model="text-embedding-3-small")
    return [embedding.embedding for embedding in embeddings.data]

@lru_cache(maxsize=None)
def generate_embeddings(categories: str):
    """
    Uses OpenAI API to get embeddings for each category
    """
    import os
    
    categories = categories.split(", ")
    embeddings = {}
    
    # Check if embeddings cache exists
    os.makedirs(".cache", exist_ok=True)
    cache_path = ".cache/embeddings.json"
    
    # Try to load from cache first
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r") as f:
                cached_embeddings = json.load(f)
                
            # Only process categories not in cache
            categories_to_process = [c for c in categories if c not in cached_embeddings]
            embeddings = {k: v for k, v in cached_embeddings.items() if k in categories}
            print(f"Loaded {len(embeddings)} embeddings from cache")
        except Exception as e:
            print(f"Error loading embeddings cache: {e}")
            categories_to_process = categories
    else:
        categories_to_process = categories
    
    if categories_to_process:
        def process_category(category):
            embedding = generate_embedding(category)
            return category, embedding
        
        with ThreadPoolExecutor() as executor:
            results = list(tqdm(
                executor.map(process_category, categories_to_process),
                total=len(categories_to_process),
                desc="Generating embeddings"
            ))
            
        # Update embeddings with new results
        for category, embedding in results:
            embeddings[category] = embedding
            
        # Update cache with all embeddings
        try:
            all_embeddings = cached_embeddings if 'cached_embeddings' in locals() else {}
            all_embeddings.update(embeddings)
            
            with open(cache_path, "w") as f:
                json.dump(all_embeddings, f)
        except Exception as e:
            print(f"Error saving embeddings cache: {e}")
    
    return embeddings

def cosine_similarity(a: Dict[str, float], b: List[float]):
    """
    Uses cosine similarity to find similarity between two vectors
    """
    similarities = {}
    
    def calculate_similarity(item):
        category, embedding = item
        return category, np.dot(embedding, b) / (np.linalg.norm(embedding) * np.linalg.norm(b))
    
    with ThreadPoolExecutor() as executor:
        results = list(tqdm(
            executor.map(calculate_similarity, a.items()),
            total=len(a),
            desc="Calculating similarities"
        ))
    
    for category, similarity in results:
        similarities[category] = similarity
    return similarities

def most_similar_categories(concept: str, n: int = 5):
    """
    Uses cosine similarity to find similar categories
    """
    categories = load_categories()
    concept_embedding = generate_embedding(concept)[0]
    category_embeddings = generate_embeddings(", ".join(categories))


    similarities = cosine_similarity(category_embeddings, concept_embedding)


    sorted_categories = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    return sorted_categories[:n]



    
# ================================
# DSL Conversion Functions
# ================================

def smooth_quickdraw_drawing(drawing):
    """
    Smooth the quickdraw drawing by estimating t_values
    """
    # Normalize coordinates to 0-1 range
    x_min = min(min(stroke[0]) for stroke in drawing)
    x_max = max(max(stroke[0]) for stroke in drawing)
    y_min = min(min(stroke[1]) for stroke in drawing)
    y_max = max(max(stroke[1]) for stroke in drawing)
    
    smoothed_drawing = []
    for stroke in drawing:
        x_coords, y_coords = stroke[0], stroke[1]
        
        # Calculate cumulative distance for t values
        distances = [0]
        for i in range(1, len(x_coords)):
            dx = x_coords[i] - x_coords[i-1]
            dy = y_coords[i] - y_coords[i-1]
            distances.append(distances[-1] + np.sqrt(dx**2 + dy**2))
        
        # Normalize t values to 0-1 range
        if distances[-1] > 0:
            t_values = [d/distances[-1] for d in distances]
        else:
            t_values = [i/(len(x_coords)-1) for i in range(len(x_coords))]
        
        # Normalize coordinates
        x_norm = [(x - x_min)/(x_max - x_min) for x in x_coords]
        y_norm = [(y - y_min)/(y_max - y_min) for y in y_coords]

        smoothed_drawing.append([x_coords, y_coords, t_values])
    
    return smoothed_drawing

def quickdraw_to_dsl(drawing, res):
    """
    Convert stroke data to DSL format string
    
    Args:
        strokes_data: List of strokes in format [
            [ [x0,x1,...], [y0,y1,...], [t0,t1,...] ],
            [ [x0,x1,...], [y0,y1,...], [t0,t1,...] ],
            ...
        ]
    
    Returns:
        DSL formatted string
    """
    dsl_lines = ["<strokes>"]
    
    for i, stroke in enumerate(drawing):
        # Extract x, y, t values
        x_coords, y_coords, t_values = stroke
        x_coords = [(x / 256) * res for x in x_coords]
        y_coords = [(256 - y) / 256 * res for y in y_coords]
        # Format points
        points = "'" + "','".join(f"x{int(x)}y{int(y)}" for x, y in zip(x_coords, y_coords)) + "'"  
        
        # Format t values
        t_str = ",".join(f"{t:.2f}" for t in t_values)
        
        # Add stroke to DSL
        dsl_lines.append(f"  <s{i+1}>")
        dsl_lines.append(f"    <points>{points}</points>")
        dsl_lines.append(f"    <t_values>{t_str}</t_values>")
        dsl_lines.append(f"  </s{i+1}>")
    
    dsl_lines.append("</strokes>")
    
    return "\n".join(dsl_lines)

def quickdraw_to_dsl_file(concept: str):
    sketches = []
    with open(f"{QUICKDRAW_DATASET_PATH}/{concept}.ndjson", "r") as f:
        # Count number of lines in the file
        total_lines = sum(1 for _ in open(f"{QUICKDRAW_DATASET_PATH}/{concept}.ndjson", "r"))
        
        # Reopen the file for processing
        with open(f"{QUICKDRAW_DATASET_PATH}/{concept}.ndjson", "r") as count_f:
            for line in tqdm(count_f, desc=f"Converting {concept} to DSL", total=total_lines):
                data = json.loads(line)
                strokes = data["drawing"]
                smoothed_strokes = smooth_quickdraw_drawing(strokes)
                dsl_output = quickdraw_to_dsl(smoothed_strokes, 50)
                sketches.append(dsl_output)
    return sketches

def quickdraw_to_dsl_file_pick_random(concept: str):
    sketches = []
    with open(f"{QUICKDRAW_DATASET_PATH}/{concept}.ndjson", "r") as f:
        # First pass: collect all recognized line numbers
        recognized_lines = []
        total_lines = 0
        with open(f"{QUICKDRAW_DATASET_PATH}/{concept}.ndjson", "r") as temp_f:
            for i, line in enumerate(temp_f):
                data = json.loads(line)
                if data["recognized"]:
                    recognized_lines.append(i)
                total_lines += 1

        if not recognized_lines:
            raise ValueError(f"No recognized drawings found for {concept}")
        
        
        # Pick a random recognized line
        random_line = random.choice(recognized_lines)
        f.seek(0)  # Reset file pointer
        
        # Get the selected line
        for i, line in enumerate(f):
            if i == random_line:
                data = json.loads(line)
                strokes = data["drawing"]
                smoothed_strokes = smooth_quickdraw_drawing(strokes)
                dsl_output = quickdraw_to_dsl(smoothed_strokes, 50)
                return dsl_output, i

    return random.choice(sketches), random_line

# ================================
# Main Section
# ================================

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concept", type=str, default="airplane", help="Concept to convert to DSL")
    parser.add_argument("--examples", type=int, default=3, help="Number of examples to show")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    chosen_categories = ["car", "lighthouse", "tree", "cactus", "clock", "ice cream", "dog", "chair", "umbrella"]

    n_trials = 10
    from concurrent.futures import ThreadPoolExecutor

    sketches = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for category in chosen_categories:
            for i in range(n_trials):
                futures.append(executor.submit(quickdraw_to_dsl_file_pick_random, category))
        
        for idx, future in tqdm(enumerate(futures), total=len(futures), desc="Processing categories"):
            category = chosen_categories[idx // n_trials]
            dsl_output, line_number = future.result()
            sketches.append((dsl_output, category, line_number))

    for sketch, category, line_number in sketches:
        utils.show_dsl_popup(
            sketch,
            50, 12, 7,
            title=category + f" {line_number}"
        )
    

    
    