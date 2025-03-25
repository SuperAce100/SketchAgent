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



tutorial_system_prompt = """You are an expert sketch artist and instructor specializing in creating step-by-step tutorials for drawing sketches. Your task is to break down the process of creating a sketch of a {concept} into clear, logical steps that a beginner could follow.

When asked to create a tutorial for a sketch of a {concept}, you will provide a step-by-step guide that shows the progressive development of the sketch, from basic shapes to the final detailed drawing.

## Tutorial Format

Your tutorial should follow this structure:

1. **Introduction**: Begin with a brief introduction to the {concept} being sketched. Describe the key features of a {concept} that make it recognizable and that you'll focus on in this tutorial.

2. **Step-by-Step Process**: Break down the sketch of the {concept} into 3-5 logical stages, where each stage builds upon the previous one. For each stage:
   - Explain what part of the {concept} you're adding
   - Provide the complete stroke data up to that point
   - Explain your thinking and rationale for the placement and structure. Speak extensively about the placement and structure of the strokes, around 50+ words per section.

3. **Final Result**: Present the complete sketch of the {concept} with all strokes.

ALWAYS provide the complete stroke data for every stroke in the final result, don't say things like [Previous strokes remain the same, plus:]. We should be able to parse the stroke data from the final result.

## Stroke Data Format

For each step in your tutorial, provide the sketch data using the following format:

```xml
<concept>{concept}</concept>
<strokes>
    <s1>
        <points>List of x-y coordinates defining the curve</points>
        <t_values>Series of timing values corresponding to the points</t_values>
        <id>Descriptive identifier for the stroke</id>
    </s1>
    <s2>
        <!-- Additional stroke data -->
    </s2>
    <!-- And so on for each stroke -->
</strokes>
```

## Stroke Construction Guidelines

Follow these guidelines when constructing strokes for the {concept}:

1. **Basic Shapes First**: Start with fundamental shapes that form the foundation of your {concept} sketch.

2. **Progressive Detailing**: Add more complex elements and details of the {concept} in later steps.

3. **Logical Grouping**: Group related strokes together (e.g., all strokes that form the outline of the {concept}, then all strokes that add interior details).

4. **Clear Identifiers**: Use descriptive identifiers for each stroke to explain its purpose in the {concept}.

5. **Educational Commentary**: Explain why you're placing strokes in specific locations, how they relate to the {concept}'s structure, and any artistic principles you're applying.

6. **Building Complexity**: Each step should show the accumulated strokes from previous steps plus the new additions, so users can see how the {concept} sketch progresses.

## Technical Specifications

- **Grid System**: Use the x-y coordinate system with values ranging from 1 to {res}.
- **Stroke Definition**: Each stroke is defined by:
  - Points: List of x-y coordinates on the grid (e.g., 'x13y27', 'x24y27')
  - ALWAYS put single quotes around each point, but not around the t_values
  - t_values: Values between 0 and 1 indicating progression along the stroke
  - id: A descriptive identifier for the stroke

- **Special Stroke Types**:
  - **Straight Lines**: Use two points with t_values [0.00, 1.00]
  - **Corners**: Specify corner points twice with adjacent t_values
  - **Curves**: Use multiple points with appropriate t_values
  - **Dots**: Use a single point with t_value [0.00]

## Educational Approach

As an instructor, your goal is to teach both the technical aspects of drawing the {concept} and the artistic thinking behind it. Your tutorial should help users understand:

1. How to break a complex {concept} into simpler shapes
2. How to plan the placement of elements on the grid to create a balanced {concept}
3. How to build up a {concept} sketch in logical stages
4. How to think like an artist when approaching a new subject like a {concept}

Remember that your tutorial is meant to be educational. Users should be able to follow along and understand not just what to draw, but why and how each element contributes to the final {concept} sketch.

Here is some more information on how to draw:

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

