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
        # Count number of lines in the file
        total_lines = sum(1 for _ in open(f"{QUICKDRAW_DATASET_PATH}/{concept}.ndjson", "r"))
        
        # Pick a random line number
        random_line = random.randint(0, total_lines - 1)
        
        # Read the random line
        for i, line in tqdm(enumerate(f), desc=f"Finding random {concept}", total=random_line):
            if i == random_line:
                data = json.loads(line)
                strokes = data["drawing"]
                smoothed_strokes = smooth_quickdraw_drawing(strokes)
                dsl_output = quickdraw_to_dsl(smoothed_strokes, 50)
                sketches.append(dsl_output)
                break
    return random.choice(sketches)

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

    most_similar = most_similar_categories(args.concept, n=args.examples)
    print(f"Most similar categories to '{args.concept}':")
    for i, (category, similarity) in enumerate(most_similar, 1):
        print(f"  {i}. {category}: {similarity[0]:.4f}")
    # Plot most similar categories as a bar chart
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.family'] = 'Inter'
    categories = [cat for cat, _ in most_similar]
    similarities = [sim[0] for _, sim in most_similar]

    plt.bar(categories, similarities)
    plt.ylabel('Cosine Similarity', fontweight='bold')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.ylim(min(similarities)*0.9, min(max(similarities)*1.1, 1))
    plt.title(f'Categories Most Similar to {args.concept.capitalize()}', fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.show()


    examples = []

    # Process categories in parallel
    with ThreadPoolExecutor() as executor:
        
        # Submit all tasks and collect results
        future_to_category = {executor.submit(quickdraw_to_dsl_file_pick_random, category): category for category in categories}
        
        for future in as_completed(future_to_category):
            result = future.result()
            category = future_to_category[future]
            examples.append((category, result))
            utils.show_dsl_popup(result, 50, 12, 7, title=category)
    

    
    