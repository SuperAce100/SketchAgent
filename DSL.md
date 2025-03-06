# Sketch DSL Documentation

## Basic Structure
The DSL follows this basic structure:
```xml
<strokes>
  <s1>
    <points>x1y1,x2y2,x3y3,...</points>
    <t_values>t1,t2,t3,...</t_values>
  </s1>
  <s2>
    <points>x1y1,x2y2,x3y3,...</points>
    <t_values>t1,t2,t3,...</t_values>
  </s2>
  ...
</strokes>
```

## Elements

### `<concept>`
- Explains the overall concept of the sketch

### `<strokes>`
- Root element containing all stroke definitions
- Contains one or more `<sN>` elements

### `<sN>`
- Defines a single stroke where N is the stroke number (1-based index)
- Contains:
  - `<points>`: Comma-separated list of grid coordinates
  - `<t_values>`: Comma-separated list of parameter values for Bézier curve

### `<points>`
- Defines the control points for the stroke
- Format: x1y1,x2y2,x3y3,...
- Coordinates are grid-based (e.g., x1y1 = column 1, row 1)
- Coordinates are bounded by the grid resolution (1 to res)

### `<t_values>`
- Defines the parameter values for the Bézier curve
- Format: t1,t2,t3,...
- Values are floats between 0 and 1
- Used for calculating the curve between control points

### `<id>`
- Semantic identifier for the stroke

## Example
For a simple two-stroke sketch:
```xml
<concept>airplane</concept>
<strokes>
  <s1>
    <points>x1y1,x2y2,x3y3</points>
    <t_values>0.0,0.5,1.0</t_values>
    <id>first stroke</id>
  </s1>
  <s2>
    <points>x4y4,x5y5</points>
    <t_values>0.0,1.0</t_values>
    <id>second stroke</id>
  </s2>
</strokes>
```