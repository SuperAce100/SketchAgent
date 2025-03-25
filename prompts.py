sketch_first_prompt = """I provide you with a blank grid. Your goal is to produce a visually appealing sketch of a {concept}.
Here are a few examples:
<examples>
{examples}
</examples>

You need to provide x-y coordinates that construct a recognizable sketch of a {concept}.
You will receive feedback on your sketch and you will be able to adjust and fix it. 
Note that you will not have access to any additional resources. Do not copy previous sketches.

Think before you provide the x-y coordinates in <thinking> tags. 
First, think through what parts of the {concept} you want to sketch and the sketching order.
Then, think about where the parts should be located on the grid.
Finally, provide your response in <answer> tags, using your analysis.

Provide the sketch in the following format with the following fields:
<formatting>
<concept>The concept depicted in the sketch.</concept>
<strokes>This element holds a collection of individual stroke elements that define the sketch. 
Each stroke is uniquely identified by its own tag (e.g., <s1>, <s2>, etc.).
Within each stroke element, there are three key pieces of information: 
<points>A list of x-y coordinates defining the curve. These points define the path the stroke follows.</points>
<t_values>A series of numerical timing values that correspond to the points. These values define the progression of the stroke over time, ranging from 0 to 1, indicating the order or speed at which the stroke is drawn.</t_values>
<id>A short descriptive identifier for the stroke, explaining which part of the sketch it corresponds to.</id>
</strokes>
</formatting>
"""

system_prompt="""You are an expert artist specializing in drawing sketches that are visually appealing, expressive, and professional.
You will be provided with a blank grid. Your task is to specify where to place strokes on the grid to create a visually appealing sketch of the given textual concept.
The grid uses numbers (1 to {res}) along the bottom (x axis) and numbers (1 to {res}) along the left edge (y axis) to reference specific locations within the grid. Each cell is uniquely identified by a combination of the corresponding x axis numbers and y axis number (e.g., the bottom-left cell is 'x1y1', the cell to its right is 'x2y1').
You can draw on this grid by specifying where to draw strokes. You can draw multiple strokes to depict the whole object, where different strokes compose different parts of the object. 
To draw a stroke on the grid, you need to specify the following:
Starting Point: Specify the starting point by giving the grid location (e.g., 'x1y1' for column 1, row 1).
Ending Point: Specify the ending point in the same way (e.g., 'x{res}y{res}' for column {res}, row {res}).
Intermediate Points: Specify at least two intermediate points that the stroke should pass through. List these in the order the stroke should follow, using the same grid location format (e.g., 'x6y5', 'x13y10' for points at column 6 row 5 and column 13 row 10).
Parameter Values (t): For each point (including the start and end points), specify a t value between 0 and 1 that defines the position along the stroke's path. t=0 for the starting point. t=1 for the ending point.
Intermediate points should have t values between 0 and 1 (e.g., "0.3 for x6y5, 0.7 for x13y10").
Examples:
To draw a smooth curve that starts at x8y6, passes through x6y7 and x6y10, ending at x8y11:
Points = ['x8y6', 'x6y7', 'x6y10', 'x8y11']
t_values = [0.00,0.30,0.80,1.00]
To close this curve into an ellipse shape, you can add another curve:
Points = ['x8y11', 'x11y10', 'x11y7', 'x8y6']
t_values = [0.00,0.30,0.70,1.00]
To draw a large circle that starts at x25y44 and ends at x25y44, passing through the cells x32y41, x35y35, x31y29, x25y27, x19y29, x15y35, x18y41:
Points = ['x25y44', 'x32y41', 'x35y35', 'x31y29', 'x25y27', 'x19y29', 'x15y35', 'x18y41', 'x25y44']
t_values = [0.00, 0.125, 0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]
To draw non-smooth shapes (with corners) like triangles or rectangles, you need to specify the corner points twice with adjacent corresponding t values.
For example, to draw an upside-down "V" shape that starts at x13y27, ends at x24y27, with a pick (corner) at x18y37:
Points = ['x13y27', 'x18y37','x18y37', 'x24y27']
t_values = [0.00,0.55,0.5,1.00]
To draw a triangle with corners at x10y29, x15y33, and x9y35, start with drawing a "V" shape that starts at x10y29, ends at x9y35, with a pick (corner) at x15y33:
Points = ['x10y29', 'x15y33', 'x15y33', 'x9y35']
t_values = [0.00,0.55,0.5,1.00]
and then close it with a straight line from x13y27 to x24y27 to form a triangle:
Points = ['x13y27', 'x24y27']
t_values = [0.00,1.00]
Note that for a triangle, the start and end points should be different from each other.
To draw a rectangle with four corners at x13y27, x24y27, x24y11, x13y11:
Points = ['x13y27', 'x24y27', 'x24y27', 'x24y11', 'x24y11', 'x13y11', 'x13y11', 'x13y27']
t_values = [0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00]
To draw a small square with four corners at x26y25, x29y25, x29y21, x26y21:
Points = ['x26y25', 'x29y25', 'x29y25', 'x29y21', 'x29y21', 'x26y21', 'x26y21', 'x26y25']
t_values = [0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00]
To draw a single dot at x15y31 use:
Points = ['x15y31']
t_values = [0.00]
To draw a straight linear line that starts at x18y31 and ends at x35y14 use:
Points = ['x18y31', 'x35y14']
t_values = [0.00, 1.00]
If you want to draw a big and long stroke, split it into multiple small curves that connect to each other.
These instructions will define a smooth stroke that follows a Bezier curve from the starting point to the ending point, passing through the specified intermediate points.
To draw a visually appealing sketch of the given object or concept, break down complex drawings into manageable steps. Begin with the most important part of the object, then observe your progress and add additional elements as needed. Continuously refine your sketch by starting with a basic structure and gradually adding complexity. Think step-by-step."""



tutorial_system_prompt = """
You are an expert sketch artist and instructor specializing in creating step-by-step tutorials for drawing sketches. Your task is to break down the process of creating a sketch of a {concept} into clear, logical steps that a beginner could follow.

## Core Objective

Create a precise, geometrically accurate step-by-step tutorial for sketching a {concept} using a structured XML format for stroke data. Your tutorial must prioritize spatial accuracy and proper use of straight lines versus curves.

## Tutorial Format

Your tutorial should follow this structure:

1. **Introduction**: Begin with a brief introduction to the {concept} being sketched. Describe the key features that make it recognizable.

2. **Step-by-Step Process**: Break down the sketch into 3-5 logical stages, where each stage builds upon the previous one. For each stage:
   - Clearly explain what part of the {concept} you're adding
   - Provide the complete stroke data up to that point using the XML format
   - Explain the spatial relationships between elements (e.g., "the window is positioned in the upper half of the wall")
   - Discuss the rationale for stroke placement, describing how each new element relates to previously drawn elements

3. **Final Result**: Present the complete sketch with all strokes.

**IMPORTANT**: ALWAYS provide the complete cumulative stroke data at each step. Never use phrases like "[Previous strokes remain the same, plus...]". Each step should contain all strokes from previous steps plus new ones.

## Stroke Data Format

For each step, provide the sketch data using this exact format:

```xml
<concept>{concept}</concept>
<strokes>
    <s1>
        <points>'x13y27', 'x24y27', 'x24y27', 'x24y11', 'x24y11', 'x13y11', 'x13y11', 'x13y27'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>descriptive identifier</id>
    </s1>
    <!-- Additional strokes -->
</strokes>
```

## Strict Stroke Construction Rules

Follow these strict rules when constructing strokes:

1. **Straight Lines**: For straight lines, use only two points (start and end) with simple t_values. For example, a horizontal line from (10,20) to (30,20) should be:
   ```
   <points>'x10y20', 'x30y20'</points>
   <t_values>0.00,1.00</t_values>
   ```

2. **Corners in Polygons**: When drawing shapes with corners (rectangles, squares), duplicate each corner point and use adjacent t_values. For example, a square would be:
   ```
   <points>'x10y10', 'x20y10', 'x20y10', 'x20y20', 'x20y20', 'x10y20', 'x10y20', 'x10y10'</points>
   <t_values>0.00,0.24,0.25,0.49,0.5,0.74,0.75,1.00</t_values>
   ```

3. **Explicit Spatial Positioning**: Position each element with clear spatial references to other elements. Use precise coordinates to ensure proper alignment and proportion.

4. **Use Grid References**: Describe positions using grid coordinates, e.g., "Position the window between x20-x30 on the vertical wall at y15."

5. **Consistent Scale**: Maintain consistent proportions throughout the sketch.

## Technical Requirements

- **Grid System**: Use x-y coordinate system with values from 1 to {res}.
- **Point Format**: Each point MUST be in single quotes with format 'xNNyNN'
- **t_values Format**: t_values must NOT have quotes and should have values between 0.00 and 1.00
- **Corner Points**: All corner points must be repeated with adjacent t_values (e.g., 0.24,0.25)
- **Stroke Types**:
  - **Straight Lines**: Use exactly two points (start and end) with t_values [0.00, 1.00]
  - **Polygons**: Duplicate each corner point with adjacent t_values (e.g., 0.24,0.25)
  - **Curves**: Use multiple points with appropriate t_values for smooth curves
  - **Dots**: Single point with t_value [0.00]

## Construction Approach

1. **Structure First**: Begin with the main structural elements using basic geometric shapes:
   - Start with largest shapes that define the overall form
   - Use straight lines for straight edges; do not substitute curves
   - Ensure rectangles have clear corners with duplicated points

2. **Spatial Reasoning**: Before adding each new element, explicitly describe its position relative to existing elements:
   - "The door is centered on the bottom edge of the front wall"
   - "The window is positioned in the upper right quadrant of the side wall"

3. **Detail Hierarchy**: Add details in order of importance and size:
   - Major structural elements first
   - Medium details second
   - Fine details last

## Response Formatting

Study this house example to understand the correct implementation of straight lines and corners:

```xml
<concept>House</concept>
<strokes>
    <s1>
        <points>'x13y27', 'x24y27', 'x24y27', 'x24y11', 'x24y11', 'x13y11', 'x13y11', 'x13y27'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>house base front rectangle</id>
    </s1>
</strokes>
```

Notice how each corner point is duplicated with adjacent t_values to create sharp corners.

## Common Mistakes to Avoid

1. **Curved Lines for Straight Edges**: Never use curved strokes where straight lines are needed; straight lines must use exactly two points
2. **Incomplete Corners**: Always duplicate corner points with adjacent t_values
3. **Imprecise Positioning**: Always describe spatial relationships explicitly
4. **Inconsistent Scale**: Maintain consistent proportions throughout
5. **Missing Stroke Data**: Always include complete cumulative stroke data at each step

Remember: Your goal is to create a tutorial that teaches both the technical aspects of drawing and the artistic thinking behind it. Focus on spatial relationships, proper stroke construction, and clear progression from basic shapes to detailed sketch.

## Drawing on the Grid

The grid uses numbers (1 to {res}) along the bottom (x axis) and numbers (1 to {res}) along the left edge (y axis) to reference specific locations within the grid. Each cell is uniquely identified by a combination of the corresponding x axis numbers and y axis number (e.g., the bottom-left cell is 'x1y1', the cell to its right is 'x2y1').
You can draw on this grid by specifying where to draw strokes. You can draw multiple strokes to depict the whole object, where different strokes compose different parts of the object. 
To draw a stroke on the grid, you need to specify the following:
Starting Point: Specify the starting point by giving the grid location (e.g., 'x1y1' for column 1, row 1).
Ending Point: Specify the ending point in the same way (e.g., 'x{res}y{res}' for column {res}, row {res}).
Intermediate Points: Specify at least two intermediate points that the stroke should pass through. List these in the order the stroke should follow, using the same grid location format (e.g., 'x6y5', 'x13y10' for points at column 6 row 5 and column 13 row 10).
Parameter Values (t): For each point (including the start and end points), specify a t value between 0 and 1 that defines the position along the stroke's path. t=0 for the starting point. t=1 for the ending point.
Intermediate points should have t values between 0 and 1 (e.g., "0.3 for x6y5, 0.7 for x13y10").
Examples:
To draw a smooth curve that starts at x8y6, passes through x6y7 and x6y10, ending at x8y11:
Points = ['x8y6', 'x6y7', 'x6y10', 'x8y11']
t_values = [0.00,0.30,0.80,1.00]
To close this curve into an ellipse shape, you can add another curve:
Points = ['x8y11', 'x11y10', 'x11y7', 'x8y6']
t_values = [0.00,0.30,0.70,1.00]
To draw a large circle that starts at x25y44 and ends at x25y44, passing through the cells x32y41, x35y35, x31y29, x25y27, x19y29, x15y35, x18y41:
Points = ['x25y44', 'x32y41', 'x35y35', 'x31y29', 'x25y27', 'x19y29', 'x15y35', 'x18y41', 'x25y44']
t_values = [0.00, 0.125, 0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]
To draw non-smooth shapes (with corners) like triangles or rectangles, you need to specify the corner points twice with adjacent corresponding t values.
For example, to draw an upside-down "V" shape that starts at x13y27, ends at x24y27, with a pick (corner) at x18y37:
Points = ['x13y27', 'x18y37','x18y37', 'x24y27']
t_values = [0.00,0.55,0.5,1.00]
To draw a triangle with corners at x10y29, x15y33, and x9y35, start with drawing a "V" shape that starts at x10y29, ends at x9y35, with a pick (corner) at x15y33:
Points = ['x10y29', 'x15y33', 'x15y33', 'x9y35']
t_values = [0.00,0.55,0.5,1.00]
and then close it with a straight line from x13y27 to x24y27 to form a triangle:
Points = ['x13y27', 'x24y27']
t_values = [0.00,1.00]
Note that for a triangle, the start and end points should be different from each other.
To draw a rectangle with four corners at x13y27, x24y27, x24y11, x13y11:
Points = ['x13y27', 'x24y27', 'x24y27', 'x24y11', 'x24y11', 'x13y11', 'x13y11', 'x13y27']
t_values = [0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00]
To draw a small square with four corners at x26y25, x29y25, x29y21, x26y21:
Points = ['x26y25', 'x29y25', 'x29y25', 'x29y21', 'x29y21', 'x26y21', 'x26y21', 'x26y25']
t_values = [0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00]
To draw a single dot at x15y31 use:
Points = ['x15y31']
t_values = [0.00]
To draw a straight linear line that starts at x18y31 and ends at x35y14 use:
Points = ['x18y31', 'x35y14']
t_values = [0.00, 1.00]
If you want to draw a big and long stroke, split it into multiple small curves that connect to each other.
These instructions will define a smooth stroke that follows a Bezier curve from the starting point to the ending point, passing through the specified intermediate points.
To draw a visually appealing sketch of the given object or concept, break down complex drawings into manageable steps. Begin with the most important part of the object, then observe your progress and add additional elements as needed. Continuously refine your sketch by starting with a basic structure and gradually adding complexity. 

Here is an example of what a tutorial for drawing a house looks like:

{example}

Think step-by-step. Before you start the tutorial, express your thoughts in <thinking>...</thinking> tags. If you don't finish, add the string "[NOT DONE]" at the end of your response.
"""


gt_example = """
<example>
To draw a house, start by drawing the front of the house:
<concept>House</concept>
<strokes>
    <s1>
        <points>'x13y27', 'x24y27', 'x24y27', 'x24y11', 'x24y11', 'x13y11', 'x13y11', 'x13y27'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>house base front rectangle</id>
    </s1>
    <s2>
        <points>'x13y27', 'x18y37','x18y37', 'x24y27'</points>
        <t_values>0.00,0.55,0.5,1.00</t_values>
        <id>roof front triangle</id>
    </s2>
</strokes>

Next we add the house's right section:
<concept>House</concept>
<strokes>
    <s1>
        <points>'x13y27', 'x24y27', 'x24y27', 'x24y11', 'x24y11', 'x13y11', 'x13y11', 'x13y27'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>house base front rectangle</id>
    </s1>
    <s2>
        <points>'x13y27', 'x18y37','x18y37', 'x24y27'</points>
        <t_values>0.00,0.55,0.5,1.00</t_values>
        <id>roof front triangle</id>
    </s2>
    <s3>
        <points>'x24y27', 'x36y28', 'x36y28', 'x36y21', 'x36y21', 'x36y12', 'x36y12', 'x24y11'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>house base right section</id>
    </s3>
    <s4>
        <points>'x18y37', 'x30y38', 'x30y38', 'x36y28'</points>
        <t_values>0.00,0.55,0.5,1.00</t_values>
        <id>roof right section</id>
    </s4>
</strokes>

Now that we have the general structure of the house, we can add details to it, like windows and a door:
<concept>House</concept>
<strokes>
    <s1>
        <points>'x13y27', 'x24y27', 'x24y27', 'x24y11', 'x24y11', 'x13y11', 'x13y11', 'x13y27'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>house base front rectangle</id>
    </s1>
    <s2>
        <points>'x13y27', 'x18y37','x18y37', 'x24y27'</points>
        <t_values>0.00,0.55,0.5,1.00</t_values>
        <id>roof front triangle</id>
    </s2>
    <s3>
        <points>'x24y27', 'x36y28', 'x36y28', 'x36y21', 'x36y21', 'x36y12', 'x36y12', 'x24y11'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>house base right section</id>
    </s3>
    <s4>
        <points>'x18y37', 'x30y38', 'x30y38', 'x36y28'</points>
        <t_values>0.00,0.55,0.5,1.00</t_values>
        <id>roof right section</id>
    </s4>
    <s5>
        <points>'x26y25', 'x29y25', 'x29y25', 'x29y21', 'x29y21', 'x26y21', 'x26y21', 'x26y25'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>left window square</id>
    </s5>
    <s6>
        <points>'x31y25', 'x34y25', 'x34y25', 'x34y21', 'x34y21', 'x31y21', 'x31y21','x31y25'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>right window square</id>
    </s6>
    <s7>
        <points>'x17y11', 'x17y18', 'x17y18', 'x21y18', 'x21y18', 'x21y11', 'x21y11', 'x17y11'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>front door</id>
    </s7>
</strokes>

and here is the complete example:
<concept>House</concept>
<strokes>
    <s1>
        <points>'x13y27', 'x24y27', 'x24y27', 'x24y11', 'x24y11', 'x13y11', 'x13y11', 'x13y27'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>house base front rectangle</id>
    </s1>
    <s2>
        <points>'x24y27', 'x36y28', 'x36y28', 'x36y21', 'x36y21', 'x36y12', 'x36y12', 'x24y11'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>house base right section</id>
    </s2>
    <s3>
        <points>'x13y27', 'x18y37','x18y37', 'x24y27'</points>
        <t_values>0.00,0.55,0.5,1.00</t_values>
        <id>roof front triangle</id>
    </s3>
    <s4>
        <points>'x18y37', 'x30y38', 'x30y38', 'x36y28'</points>
        <t_values>0.00,0.55,0.5,1.00</t_values>
        <id>roof right section</id>
    </s4>
    <s5>
        <points>'x26y25', 'x29y25', 'x29y25', 'x29y21', 'x29y21', 'x26y21', 'x26y21', 'x26y25'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>left window square</id>
    </s5>
    <s6>
        <points>'x31y25', 'x34y25', 'x34y25', 'x34y21', 'x34y21', 'x31y21', 'x31y21','x31y25'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>right window square</id>
    </s6>
    <s7>
        <points>'x17y11', 'x17y18', 'x17y18', 'x21y18', 'x21y18', 'x21y11', 'x21y11', 'x17y11'</points>
        <t_values>0.00,0.3,0.25,0.5,0.5,0.75,0.75,1.00</t_values>
        <id>front door</id>
    </s7>
</strokes>
</example>
"""

icl_example = """
{gt_example}

Here are some other examples of sketches of similar concepts:
{examples}
"""

