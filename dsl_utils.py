def format_strokes_to_dsl(strokes_data):
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
    
    for i, stroke in enumerate(strokes_data):
        # Extract x, y, t values
        x_coords, y_coords, t_values = stroke
        
        # Format points
        points = ",".join(f"x{int(x)}y{int(y)}" for x, y in zip(x_coords, y_coords))
        
        # Format t values
        t_str = ",".join(f"{t:.2f}" for t in t_values)
        
        # Add stroke to DSL
        dsl_lines.append(f"  <s{i+1}>")
        dsl_lines.append(f"    <points>{points}</points>")
        dsl_lines.append(f"    <t_values>{t_str}</t_values>")
        dsl_lines.append(f"  </s{i+1}>")
    
    dsl_lines.append("</strokes>")
    
    return "\n".join(dsl_lines)

# Example usage
if __name__ == "__main__":
    example_strokes = [
        [
            [1, 2, 3, 4],  # x coords
            [5, 6, 7, 8],  # y coords 
            [0.0, 0.3, 0.7, 1.0]  # t values
        ],
        [
            [10, 11, 12],
            [20, 21, 22],
            [0.0, 0.5, 1.0]
        ]
    ]
    
    dsl_output = format_strokes_to_dsl(example_strokes)
    print(dsl_output) 