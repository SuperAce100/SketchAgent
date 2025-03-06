import json
import tempfile
import xml.etree.ElementTree as ET
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
import ast
import cairosvg

# =========================
# ===== Grid related ======
# =========================
def create_grid_image(res=50, cell_size=12, header_size=12):
    # Define the size of the grid
    rows = res
    cols = res
    
    img_width = (cols + 1) * cell_size
    img_height = (rows + 1) * cell_size
    
    # Create a new image with a white background
    img = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", header_size*0.85)
    except IOError:
        font = ImageFont.load_default()
    
    # Draw the headers
    for j in range(cols):
        # Draw column header (letters)
        text = str(j +1)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (j + 1) * cell_size + (cell_size - text_width) / 2
        text_y = img_height - cell_size # - (cell_size - text_height) / 2
        draw.text((text_x, text_y), text, fill="black", font=font)
    
    for i in range(rows):
        # Draw row header (numbers)
        text = str(rows - i)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (cell_size - text_width) / 2
        text_y = i * cell_size + (cell_size - text_height) / 2 - 0.2*text_height
        draw.text((text_x, text_y), text, fill="black", font=font)
    
    # Draw the grid
    i = 1
    draw.line([(i * cell_size, 0), (i * cell_size, img_height)], fill="black")
    # Horizontal lines
    draw.line([(0, img_height -  cell_size), (img_width, img_height -  cell_size)], fill="black")
    
    positions={}
    # Draw the grid
    for i in range(rows)[::-1]:
        for j in range(cols):
            # Draw cell border
            if j == 0:
                draw.rectangle([(j + 0) * cell_size, (i + 0) * cell_size, (j + 1) * cell_size, (i + 1) * cell_size], outline="black")
            if i == rows - 1:
                draw.rectangle([(j + 0) * cell_size, (i + 1) * cell_size, (j + 1) * cell_size, (i + 2) * cell_size], outline="black")
    
            # Calculate the position of the text
            text = f"x{j + 1}y{i + 1}"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = (j + 1) * cell_size + (cell_size - text_width) / 2
            text_y = (i + 1) * cell_size + (cell_size - text_height) / 2
            
            center_y = int(img_height - cell_size - (i * cell_size) - cell_size / 2)
            center_x = int(j * cell_size + cell_size / 2 + cell_size)
            positions[text] = (center_x, center_y)
    return img, positions


def cells_to_pixels(res=50, cell_size=12, header_size=12):
    # Define the size of the grid
    rows = res
    cols = res
    
    img_width = (cols + 1) * cell_size
    img_height = (rows + 1) * cell_size

    positions={}
    # Draw the grid
    for i in range(rows)[::-1]:
        for j in range(cols):
            # Calculate the position of the text
            text = f"x{j + 1}y{i + 1}"
            
            center_y = int(img_height - cell_size - (i * cell_size) - cell_size / 2)
            center_x = int(j * cell_size + cell_size / 2 + cell_size)
            positions[text] = (center_x, center_y)

    return positions


# =========================
# ===== LLM related =======
# =========================
def image_to_str(image: Image):
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    image = base64.b64encode(buffer.read()).decode('utf-8')
    return image



# =================================
# ===== SVG process related =======
# =================================
def bezier_point(P, t):
    """Calculate a point on the Bézier curve for a given t."""
    return (1-t)**3 * P[0] + 3*(1-t)**2 * t * P[1] + 3*(1-t) * t**2 * P[2] + t**3 * P[3]


def estimate_bezier_control_points_helper(sampled_points, t_values):
    n = len(sampled_points)
    
    if n == 1:
        # Linear interpolation: the control points are simply the two points
        P0 = np.array(sampled_points[0])
        P1 = np.array(sampled_points[0]).astype(np.float64) + 0.0001
        return np.array([P0, P1])
        
    if n == 2:
        # Linear interpolation: the control points are simply the two points
        P0 = np.array(sampled_points[0])
        P1 = np.array(sampled_points[1])
        return np.array([P0, P1])

    if n > len(t_values):
        t_values = np.linespace(0,1,n)
    
    elif n == 3:
        # Quadratic Bézier curve: we need to solve for three control points
        A = np.zeros((n, 3))
        for i in range(n):
            t = t_values[i]
            A[i, 0] = (1-t)**2
            A[i, 1] = 2*(1-t)*t
            A[i, 2] = t**2
        
        # Points (flattened)
        B = np.array(sampled_points).reshape(-1, 2)  # Assuming 2D points
        
        # Solve the system (least squares)
        P = np.linalg.lstsq(A, B, rcond=None)[0]
        return P

    # Matrix A
    A = np.zeros((n, 4))
    for i in range(n):
        t = t_values[i]
        A[i, 0] = (1-t)**3
        A[i, 1] = 3*(1-t)**2 * t
        A[i, 2] = 3*(1-t) * t**2
        A[i, 3] = t**3
    
    # Points (flattened)
    B = np.array(sampled_points).reshape(-1, 2)  # Assuming 2D points
    
    # Solve the system (least squares)
    P = np.linalg.lstsq(A, B, rcond=None)[0]
    return P

    
def estimate_bezier_control_points( sampled_points, t_values):
    if len(sampled_points) != len(t_values):
        t_values = np.linspace(0,1, len(sampled_points))
    P = estimate_bezier_control_points_helper(sampled_points, t_values)

    if len(sampled_points) > 4:
        # Calculate the mean squared error between sampled points and the fitted Bézier curve.
        errors = []
        for i, t in enumerate(t_values):
            B_t = bezier_point(P, t)
            error = np.linalg.norm(B_t - sampled_points[i])
            errors.append(error)
        error = np.mean(errors)
        
        if error > 5 and len(sampled_points) >= 7:
            mid = len(sampled_points) // 2
            left_sampled_points = sampled_points[:mid+1]
            right_sampled_points = sampled_points[mid:]
            left_t_values = np.array(t_values[:mid+1])
            right_t_values = np.array(t_values[mid:])

            if len(left_sampled_points) == 3: # this applies in case we have 7 points
                left_sampled_points.append(right_sampled_points[0])
                left_t_values.append(right_t_values[0])
                
            # Normalize t_values for each segment
            left_t_values = (left_t_values - left_t_values[0]) / (left_t_values[-1] - left_t_values[0])
            right_t_values = (right_t_values - right_t_values[0]) / (right_t_values[-1] - right_t_values[0])

            # Recursively fit curves to each segment
            P_left = estimate_bezier_control_points_helper(left_sampled_points, left_t_values)
            P_right = estimate_bezier_control_points_helper(right_sampled_points, right_t_values)
            P_right[0] = P_left[-1] # I added this to have the long strokes look more connected
            return [P_left, P_right]
    return [P]


def get_control_points(strokes_all, t_values_all, cells_to_pixels_map):
    net_points = []      
    for j in range(len(strokes_all)):
        sampled_cells = strokes_all[j]
        t_values = t_values_all[j]
        sampled_points = []
        for cell in sampled_cells:
            y,x = cells_to_pixels_map[cell]
            sampled_points.append([y,x])
        points_lst = estimate_bezier_control_points(sampled_points, t_values)
        net_points.append(points_lst)
    return net_points


def get_control_points_single_stroke(strokes_all, t_values_all, cells_to_pixels_map):
    sampled_points = []
    for cell in strokes_all:
        y,x = cells_to_pixels_map[cell]
        sampled_points.append([y,x])
    points_lst = estimate_bezier_control_points(sampled_points, t_values_all)
    return points_lst


def create_svg_path_data(control_points):
    # Start the path with 'M' for the first point
    # print("control_points", control_points[0])
    path_data = 'M ' + np.array2string(np.array(control_points[0]), formatter={'float_kind':lambda x: "%.2f" % x}, separator=' ')[1:-1]    
    # Add 'L' for each subsequent point

    # check if point
    if len(control_points) == 1:
        path_data += ' '
    # check if line
    elif len(control_points) == 2:
        path_data += ' L '
    # check if quadratic
    elif len(control_points) == 3:
        path_data += ' Q '
    # check if cubic
    elif len(control_points) == 4:
        path_data += ' C '
    
    # path_data += ' C '
    for point in control_points[1:]:
        # print("pt", point[0], point[1])
        path_data += str(point[0]) + " " + str(point[1]) + " "
    
    # Return the complete 'd' attribute string
    return path_data


def format_svg(all_control_points, dim, stroke_width):
    svg_width, svg_height = dim
    sketch_text_svg = f"""<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">\n"""        
    for i, path in enumerate(all_control_points):
        gropu_text = f"""<g id="s{i + 1}" stroke="black" stroke-width="{stroke_width}" fill="none" stroke-linecap="round">\n"""
        for sub_path_cp in path:  #sometimes 1 or 2 
            path_data = create_svg_path_data(sub_path_cp)
            gropu_text += f"""<path d="{path_data}"/>\n"""
        gropu_text += "</g>\n"
        sketch_text_svg += gropu_text
    sketch_text_svg += "</svg>"
    return sketch_text_svg


def format_svg_single_stroke(group, dim, stroke_width, stroke_counter, stroke_color="black"):
    sketch_text_svg = ""      
    gropu_text = f"""<g id="s{stroke_counter}" stroke="{stroke_color}" stroke-width="{stroke_width}" fill="none" stroke-linecap="round">\n"""
    for sub_path_cp in group: 
        path_data = create_svg_path_data(sub_path_cp)
        gropu_text += f"""<path d="{path_data}"/>\n"""
    gropu_text += "</g>\n"
    sketch_text_svg += gropu_text
    return sketch_text_svg


# Note that this parse only the *first* part in the text in which you have the <strokes> </strokes> tags.
def parse_xml_string(llm_output, res):

    strokes_start_marker = "<strokes>"
    strokes_end_marker = "</strokes>"

    # Find the start and end indices of the JSON string
    start_index = llm_output.find(strokes_start_marker)
    if start_index != -1:
        # start_index += len(strokes_start_marker)  # Move past the marker
        end_index = llm_output.find(strokes_end_marker, start_index)
    else:
        return None  # XML markers not found

    if end_index == -1:
        return None  # End marker not found

    # Extract the JSON string
    strokes_str = llm_output[start_index:end_index + len(strokes_end_marker)].strip()#[:-1]
    xml_str = f"<wrap>{strokes_str}</wrap>"
    # Parse the XML string
    root = ET.fromstring(xml_str)
    
    # Initialize lists to hold strokes and t_values
    strokes_list = "[\n"
    t_values_list = "[\n"
    
    # Iterate over all the strokes
    for stroke in root.find('strokes'):
        # Extract points and clean them up
        points_text = stroke.find('points').text
    
        # Extract t_values and convert them to float
        t_values_text = stroke.find('t_values').text
    
        # Append to the lists
        strokes_list += f"[{points_text}],\n"
        t_values_list += f"[{t_values_text}],\n"
    
    strokes_list = re.sub(r'\d+', lambda x: str(min(int(x.group()), res)), strokes_list)
    strokes_list = re.sub(r'\d+', lambda x: str(max(int(x.group()), 1)), strokes_list)
    
    strokes_list += "]"
    t_values_list += "]"
    return strokes_list, t_values_list


def parse_xml_string_single_stroke(llm_output, res, stroke_counter):
    strokes_start_marker = f"<s{stroke_counter}>"
    strokes_end_marker = f"</s{stroke_counter}>"

    # Find the start and end indices of the JSON string
    start_index = llm_output.find(strokes_start_marker)
    if start_index != -1:
        # start_index += len(strokes_start_marker)  # Move past the marker
        end_index = llm_output.find(strokes_end_marker, start_index)
    else:
        return None  # XML markers not found

    if end_index == -1:
        return None  # End marker not found

    # Extract the JSON string
    strokes_str = llm_output[start_index:end_index + len(strokes_end_marker)].strip()#[:-1]
    xml_str = f"<wrap>{strokes_str}</wrap>"
    # Parse the XML string
    root = ET.fromstring(xml_str)
    
    # Iterate over all the strokes
    stroke = root.find(f"s{stroke_counter}")
    points_text = stroke.find('points').text

    # Extract t_values and convert them to float
    t_values_text = stroke.find('t_values').text

    # Append to the lists
    strokes_list = f"[{points_text}]"
    t_values_list = f"[{t_values_text}]"
    
    strokes_list = re.sub(r'\d+', lambda x: str(min(int(x.group()), res)), strokes_list)
    strokes_list = re.sub(r'\d+', lambda x: str(max(int(x.group()), 1)), strokes_list)
    
    return strokes_list, t_values_list


def parse_xml_with_ids(llm_output, res):
    """Parse XML with stroke IDs"""
    import xml.etree.ElementTree as ET
    import re
    
    strokes_start_marker = "<strokes>"
    strokes_end_marker = "</strokes>"
    
    start_index = llm_output.find(strokes_start_marker)
    if start_index == -1:
        return None, None, None
    
    end_index = llm_output.find(strokes_end_marker, start_index)
    if end_index == -1:
        return None, None, None
    
    strokes_str = llm_output[start_index:end_index + len(strokes_end_marker)].strip()
    xml_str = f"<wrap>{strokes_str}</wrap>"
    root = ET.fromstring(xml_str)
    
    strokes_list = "[\n"
    t_values_list = "[\n"
    id_list = "[\n"
    
    for stroke in root.find('strokes'):
        points_text = stroke.find('points').text
        t_values_text = stroke.find('t_values').text
        id_text = stroke.find('id').text if stroke.find('id') is not None else ""
        
        strokes_list += f"[{points_text}],\n"
        t_values_list += f"[{t_values_text}],\n"
        id_list += f"'{id_text}',\n"
    
    strokes_list = re.sub(r'\d+', lambda x: str(min(int(x.group()), res)), strokes_list)
    strokes_list = re.sub(r'\d+', lambda x: str(max(int(x.group()), 1)), strokes_list)
    
    strokes_list += "]"
    t_values_list += "]"
    id_list += "]"
    
    return strokes_list, t_values_list, id_list


# =====================================
# ===== Collaborative Sketching =======
# =====================================
def get_cur_stroke_text(stroke_counter, llm_output):
    start_marker = f"<s{stroke_counter}>"
    end_marker = f"</s{stroke_counter}>"

    # Find the start and end indices of the JSON string
    start_index = llm_output.find(start_marker)
    if start_index != -1:
        # start_index += len(strokes_start_marker)  # Move past the marker
        end_index = llm_output.find(end_marker, start_index)
    else:
        return ""  # XML markers not found

    if end_index == -1:
        return ""  # End marker not found

    # Extract the JSON string
    strokes_str = llm_output[start_index:end_index + len(end_marker)].strip()#[:-1]
    return strokes_str

# =====================================
# ===== DSL related ====================
# =====================================

def parse_dsl(dsl, res, cells_to_pixels_map, grid_size, stroke_width):
    """
    Parse the DSL output from the LLM and return the strokes, t_values, and SVG content.
    """

    if "<strokes>" not in dsl or "</strokes>" not in dsl:
        return None

    strokes_list_str, t_values_str = parse_xml_string(dsl, res)
    
    strokes_list = ast.literal_eval(strokes_list_str)
    t_values = ast.literal_eval(t_values_str)
    
    control_points = get_control_points(strokes_list, t_values, cells_to_pixels_map)
    svg_content = format_svg(control_points, dim=(grid_size, grid_size), stroke_width=stroke_width)
    
    return strokes_list, t_values, svg_content


def save_results(output_path, concept, llm_output, messages, strokes_list, t_values, svg_content, grid_image):
    """
    Save the results of the experiment.
    Saves the following files:
    - `llm_output.txt`
    - `svg_content.svg`
    - `png_content.png`
    - `canvas_content.png`
    - `experiment_log.json`
    """

    # Save raw LLM output
    with open(f"{output_path}/llm_output.txt", "w") as f:
        f.write(llm_output)

    # Save SVG
    svg_path = f"{output_path}/{concept.replace(' ', '_')}.svg"
    with open(svg_path, "w") as f:
        f.write(svg_content)

    # Generate PNG
    png_path = f"{output_path}/{concept.replace(' ', '_')}.png"
    cairosvg.svg2png(url=svg_path, write_to=png_path, background_color="white")

    # Generate PNG with grid
    canvas_png_path = f"{output_path}/{concept.replace(' ', '_')}_canvas.png"
    cairosvg.svg2png(url=svg_path, write_to=canvas_png_path)
    foreground = Image.open(canvas_png_path)
    grid_image.paste(Image.open(canvas_png_path), (0, 0), foreground)
    grid_image.save(canvas_png_path)

    # Save experiment log
    log_data = {
        "concept": concept,
        "messages": messages,
        "llm_output": llm_output,
        "strokes": strokes_list,
        "t_values": t_values
    }
    with open(f"{output_path}/experiment_log.json", "w") as f:
        json.dump(log_data, f, indent=4)


def show_dsl_popup(dsl, res, cell_size, stroke_width, title=""):
    grid_size = (res + 1) * cell_size
    cells_to_pixels_map = cells_to_pixels(res, cell_size, header_size=cell_size)
    # Process and save results
    result = parse_dsl(dsl, res, cells_to_pixels_map, grid_size, stroke_width)
    if result:
        _, _, svg_content = result
        
        from PIL import Image
        import matplotlib.pyplot as plt

        # Convert SVG to PNG
        temp_png = tempfile.NamedTemporaryFile(suffix=".png").name
        cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=temp_png)

        # Display image
        img = Image.open(temp_png)
        plt.imshow(img)
        plt.axis('off')
        plt.title(title.capitalize(), fontweight='bold', fontsize=14)
        plt.rcParams['font.family'] = 'Inter'
        plt.show()
    
    else:
        print("Error: No valid sketch DSL found in LLM output")