# Annotated Ground Truth Sketches

## Car
1. front wheel
2. rear wheel
3. bottom front bumper
4. front fender
5. chassis bottom
6. rear fender
7. bottom rear bumper
8. rear bumper
9. rear windshield
10. roof
11. windshield
12. hood
13. front bumper
14. front window
15. rear window
16. front headlight
17. rear headlight
18. front door handle
19. rear door handle

```xml
<concept>Car</concept>
<strokes>
    <s1>
        <points>'x17y20', 'x16y20', 'x15y20', 'x14y19', 'x13y18', 'x13y17', 'x12y16', 'x12y15', 'x13y14', 'x14y13', 'x16y12', 'x17y12', 'x18y12', 'x18y13', 'x19y13', 'x20y14', 'x21y15', 'x21y16', 'x21y19', 'x20y20', 'x19y20'</points>
        <t_values>0.00, 0.04, 0.08, 0.16, 0.21, 0.25, 0.29, 0.32, 0.39, 0.42, 0.51, 0.54, 0.58, 0.59, 0.61, 0.65, 0.71, 0.76, 0.88, 0.94, 1.00</t_values>
        <id>front wheel</id>
    </s1>
    <s2>
        <points>'x28y19', 'x28y18', 'x27y17', 'x27y16', 'x27y15', 'x28y14', 'x28y13', 'x29y13', 'x30y13', 'x31y12', 'x32y13', 'x33y13', 'x34y13', 'x34y14', 'x35y14', 'x35y15', 'x35y16', 'x35y17', 'x35y18', 'x34y19', 'x33y19', 'x32y20', 'x31y20', 'x30y20'</points>
        <t_values>0.00, 0.06, 0.11, 0.15, 0.18, 0.24, 0.27, 0.30, 0.34, 0.37, 0.42, 0.43, 0.48, 0.49, 0.52, 0.54, 0.60, 0.65, 0.68, 0.75, 0.80, 0.85, 0.91, 1.00</t_values>
        <id>rear wheel</id>
    </s2>
    <s3>
        <points>'x4y18', 'x5y18', 'x6y18', 'x7y18', 'x8y18', 'x9y18', 'x10y18', 'x11y18'</points>
        <t_values>0.00, 0.05, 0.13, 0.20, 0.30, 0.48, 0.66, 1.00</t_values>
        <id>bottom front bumper</id>
    </s3>
    <s4>
        <points>'x11y18', 'x11y19', 'x12y21', 'x13y22', 'x14y22', 'x15y22', 'x16y22', 'x19y22', 'x20y22', 'x21y22', 'x21y21', 'x22y21', 'x22y20', 'x22y19'</points>
        <t_values>0.00, 0.03, 0.10, 0.19, 0.21, 0.26, 0.34, 0.56, 0.60, 0.70, 0.77, 0.85, 0.89, 1.00</t_values>
        <id>front fender</id>
    </s4>
    <s5>
        <points>'x23y19', 'x24y19', 'x25y19', 'x26y19'</points>
        <t_values>0.00, 0.53, 0.78, 1.00</t_values>
        <id>chassis bottom</id>
    </s5>
    <s6>
        <points>'x26y19', 'x26y20', 'x27y21', 'x28y22', 'x29y22', 'x30y22', 'x31y22', 'x32y22', 'x33y22', 'x34y22', 'x35y22', 'x35y21', 'x36y20', 'x36y19', 'x36y18'</points>
        <t_values>0.00, 0.04, 0.08, 0.14, 0.20, 0.27, 0.33, 0.40, 0.47, 0.49, 0.55, 0.63, 0.76, 0.83, 1.00</t_values>
        <id>rear fender</id>
    </s6>
    <s7>
        <points>'x37y18', 'x38y18', 'x39y18', 'x40y18', 'x41y18', 'x42y18'</points>
        <t_values>0.00, 0.12, 0.25, 0.54, 0.77, 1.00</t_values>
        <id>bottom rear bumper</id>
    </s7>
    <s8>
        <points>'x42y18', 'x42y19', 'x42y20', 'x42y21', 'x42y22'</points>
        <t_values>0.00, 0.17, 0.33, 0.62, 1.00</t_values>
        <id>rear bumper</id>
    </s8>
    <s9>
        <points>'x42y22', 'x42y23', 'x41y24', 'x40y25', 'x40y26', 'x39y27', 'x38y28', 'x37y29', 'x36y30', 'x35y31', 'x34y31', 'x34y32', 'x33y32'</points>
        <t_values>0.00, 0.02, 0.05, 0.09, 0.12, 0.20, 0.27, 0.34, 0.42, 0.51, 0.59, 0.82, 1.00</t_values>
        <id>rear windshield</id>
    </s9>
    <s10>
        <points>'x33y32', 'x32y32', 'x31y32', 'x30y32', 'x29y32', 'x28y32', 'x27y32', 'x26y32', 'x25y32', 'x20y32', 'x19y32', 'x18y32', 'x17y32', 'x16y32'</points>
        <t_values>0.00, 0.03, 0.05, 0.07, 0.09, 0.11, 0.14, 0.23, 0.28, 0.60, 0.68, 0.78, 0.88, 1.00</t_values>
        <id>roof</id>
    </s10>
    <s11>
        <points>'x16y32', 'x15y31', 'x14y29', 'x14y28', 'x13y28', 'x13y27'</points>
        <t_values>0.00, 0.09, 0.39, 0.72, 0.87, 1.00</t_values>
        <id>windshield</id>
    </s11>
    <s12>
        <points>'x13y27', 'x12y27', 'x11y27', 'x10y27', 'x9y27', 'x8y27', 'x7y27', 'x6y27', 'x5y27'</points>
        <t_values>0.00, 0.02, 0.08, 0.12, 0.23, 0.42, 0.51, 0.69, 1.00</t_values>
        <id>hood</id>
    </s12>
    <s13>
        <points>'x5y27', 'x4y26', 'x4y25', 'x3y25', 'x3y24', 'x3y23', 'x3y22', 'x3y21', 'x3y20', 'x3y19', 'x3y18', 'x4y18'</points>
        <t_values>0.00, 0.07, 0.12, 0.19, 0.21, 0.35, 0.43, 0.56, 0.67, 0.74, 0.82, 1.00</t_values>
        <id>front bumper</id>
    </s13>
    <s14>
        <points>'x16y30', 'x16y29', 'x15y28', 'x16y27', 'x17y27', 'x18y27', 'x19y27', 'x20y27', 'x21y27', 'x22y27', 'x25y28', 'x25y29', 'x25y30', 'x25y31', 'x24y31', 'x23y31', 'x22y31', 'x21y31', 'x20y31', 'x19y31', 'x18y31', 'x17y31', 'x16y31'</points>
        <t_values>0.00, 0.02, 0.06, 0.44, 0.44, 0.45, 0.46, 0.48, 0.50, 0.53, 0.76, 0.78, 0.79, 0.80, 0.87, 0.89, 0.90, 0.91, 0.92, 0.94, 0.95, 0.97, 1.00</t_values>
        <id>front window</id>
    </s14>
    <s15>
        <points>'x27y30', 'x27y29', 'x27y28', 'x28y28', 'x29y28', 'x30y28', 'x31y28', 'x32y28', 'x33y28', 'x34y28', 'x35y28', 'x35y29', 'x34y30', 'x33y31', 'x32y31', 'x31y31', 'x30y31', 'x29y31'</points>
        <t_values>0.00, 0.03, 0.11, 0.23, 0.25, 0.28, 0.31, 0.35, 0.38, 0.42, 0.48, 0.61, 0.70, 0.82, 0.90, 0.95, 0.98, 1.00</t_values>
        <id>rear window</id>
    </s15>
    <s16>
        <points>'x5y26', 'x6y25', 'x6y24', 'x6y23', 'x5y23'</points>
        <t_values>0.00, 0.27, 0.54, 0.86, 1.00</t_values>
        <id>front headlight</id>
    </s16>
    <s17>
        <points>'x40y25', 'x40y24', 'x39y24', 'x39y23', 'x39y22', 'x40y21', 'x41y21'</points>
        <t_values>0.00, 0.12, 0.19, 0.33, 0.54, 0.86, 1.00</t_values>
        <id>rear headlight</id>
    </s17>
    <s18>
        <points>'x21y25', 'x22y25'</points>
        <t_values>0.00, 1.00</t_values>
        <id>front door handle</id>
    </s18>
    <s19>
        <points>'x34y25', 'x35y25', 'x36y25'</points>
        <t_values>0.00, 0.27, 1.00</t_values>
        <id>rear door handle</id>
    </s19>
</strokes>
```


## Lighthouse

## Tree
1. trunk left
2. trunk right
3. foliage left bottom
4. foliage left top
5. foliage right bottom
6. foliage right top

```xml
<concept>Tree</concept>
<strokes>
    <s1>
        <points>'x20y25', 'x20y24', 'x21y23', 'x21y22', 'x21y21', 'x21y20', 'x21y19', 'x21y18', 'x20y16', 'x20y15', 'x20y14', 'x19y13', 'x19y12', 'x18y11', 'x18y10', 'x17y9', 'x17y8', 'x16y7', 'x16y6', 'x15y6'</points>
        <t_values>0.00, 0.05, 0.09, 0.12, 0.16, 0.20, 0.24, 0.28, 0.37, 0.40, 0.45, 0.50, 0.54, 0.60, 0.63, 0.68, 0.74, 0.85, 0.93, 1.00</t_values>
        <id>trunk left</id>
    </s1>
    <s2>
        <points>'x26y25', 'x26y24', 'x26y23', 'x26y22', 'x26y21', 'x26y20', 'x26y19', 'x26y18', 'x26y17', 'x26y16', 'x26y15', 'x26y14', 'x26y13', 'x27y12', 'x27y11', 'x28y10', 'x28y9', 'x29y8', 'x30y7', 'x31y6'</points>
        <t_values>0.00, 0.04, 0.09, 0.13, 0.20, 0.25, 0.30, 0.34, 0.39, 0.41, 0.45, 0.50, 0.55, 0.61, 0.66, 0.77, 0.83, 0.88, 0.94, 1.00</t_values>
        <id>trunk right</id>
    </s2>
    <s3>
        <points>'x19y17', 'x18y17', 'x17y17', 'x16y17', 'x15y17', 'x14y17', 'x13y17', 'x12y18', 'x11y19', 'x10y20', 'x9y21', 'x9y24', 'x9y25', 'x9y26', 'x10y26', 'x10y27', 'x11y27'</points>
        <t_values>0.00, 0.09, 0.13, 0.16, 0.19, 0.21, 0.25, 0.29, 0.34, 0.40, 0.45, 0.65, 0.68, 0.74, 0.83, 0.91, 1.00</t_values>
        <id>foliage left bottom</id>
    </s3>
    <s4>
        <points>'x13y26', 'x12y27', 'x12y28', 'x11y29', 'x11y30', 'x11y31', 'x11y32', 'x11y33', 'x11y34', 'x11y35', 'x12y36', 'x13y37', 'x13y38', 'x14y38', 'x14y39', 'x15y39', 'x16y40', 'x17y40', 'x18y40', 'x19y40', 'x20y40', 'x21y39', 'x22y39', 'x22y38', 'x23y38'</points>
        <t_values>0.00, 0.07, 0.08, 0.13, 0.15, 0.18, 0.20, 0.22, 0.25, 0.27, 0.30, 0.35, 0.37, 0.39, 0.40, 0.42, 0.49, 0.51, 0.54, 0.56, 0.66, 0.74, 0.85, 0.89, 1.00</t_values>
        <id>foliage left top</id>
    </s4>
    <s5>
        <points>'x23y36', 'x23y37', 'x24y38', 'x25y39', 'x26y40', 'x27y40', 'x29y41', 'x30y41', 'x31y41', 'x32y41', 'x33y41', 'x34y41', 'x35y40', 'x36y39', 'x37y38', 'x38y37', 'x38y36', 'x38y35', 'x38y34', 'x37y33', 'x37y32'</points>
        <t_values>0.00, 0.04, 0.07, 0.09, 0.11, 0.13, 0.17, 0.19, 0.23, 0.27, 0.29, 0.32, 0.38, 0.45, 0.50, 0.61, 0.66, 0.74, 0.80, 0.90, 1.00</t_values>
        <id>foliage right bottom</id>
    </s5>
    <s6>
        <points>'x36y30', 'x37y29', 'x37y28', 'x38y27', 'x38y26', 'x38y25', 'x37y24', 'x37y23', 'x37y22', 'x36y21', 'x35y20', 'x35y19', 'x34y18', 'x33y18', 'x33y17', 'x32y17', 'x30y16', 'x29y16', 'x28y16'</points>
        <t_values>0.00, 0.05, 0.10, 0.14, 0.17, 0.23, 0.29, 0.33, 0.39, 0.43, 0.51, 0.54, 0.62, 0.68, 0.70, 0.73, 0.87, 0.93, 1.00</t_values>
        <id>foliage right top</id>
    </s6>
</strokes>
```

## Cactus
1. top middle branch
2. left branch
3. right branch
4. bottom middle branch left
5. bottom middle branch right
6. pot top
7. pot right
8. pot detail
9. pot left
10. pot bottom

```xml
<concept>Cactus</concept>
<strokes>
    <s1>
        <points>'x20y25', 'x20y26', 'x20y27', 'x20y28', 'x20y29', 'x20y30', 'x20y31', 'x20y32', 'x20y33', 'x20y34', 'x20y35', 'x21y36', 'x21y37', 'x21y38', 'x22y39', 'x23y39', 'x24y39', 'x25y38', 'x26y38', 'x26y37', 'x27y36', 'x27y35', 'x27y34', 'x27y33', 'x27y32', 'x27y31', 'x27y30', 'x27y29', 'x27y28', 'x27y27', 'x27y26', 'x27y25', 'x27y24', 'x27y23', 'x27y22', 'x27y21', 'x27y20'</points>
        <t_values>0.00, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.16, 0.18, 0.20, 0.22, 0.25, 0.28, 0.33, 0.37, 0.42, 0.46, 0.50, 0.53, 0.56, 0.59, 0.61, 0.65, 0.67, 0.70, 0.72, 0.74, 0.76, 0.79, 0.81, 0.83, 0.86, 0.89, 0.93, 0.96, 1.00</t_values>
        <id>top middle branch</id>
    </s1>
    <s2>
        <points>'x20y25', 'x19y25', 'x18y25', 'x17y26', 'x16y27', 'x16y28', 'x16y29', 'x15y30', 'x15y31', 'x15y32', 'x14y33', 'x13y33', 'x12y33', 'x11y32', 'x10y32', 'x10y31', 'x10y30', 'x10y29', 'x10y28', 'x10y27', 'x10y26', 'x10y25', 'x10y24', 'x10y23', 'x10y22', 'x10y21', 'x11y20', 'x12y19', 'x13y19', 'x15y18', 'x16y18', 'x17y18', 'x18y18', 'x19y18', 'x20y18'</points>
        <t_values>0.00, 0.02, 0.05, 0.10, 0.16, 0.18, 0.20, 0.24, 0.25, 0.27, 0.31, 0.35, 0.39, 0.44, 0.47, 0.49, 0.52, 0.55, 0.56, 0.59, 0.63, 0.66, 0.68, 0.71, 0.74, 0.78, 0.83, 0.89, 0.90, 0.92, 0.94, 0.95, 0.96, 0.96, 1.00</t_values>
        <id>left branch</id>
    </s2>
    <s3>
        <points>'x27y20', 'x28y20', 'x29y20', 'x30y21', 'x31y21', 'x32y23', 'x32y24', 'x32y25', 'x32y26', 'x32y27', 'x33y28', 'x34y28', 'x35y28', 'x36y27', 'x37y26', 'x37y25', 'x37y24', 'x37y23', 'x37y22', 'x36y20', 'x36y19', 'x36y18', 'x35y17', 'x35y16', 'x34y16', 'x34y15', 'x33y15', 'x32y14', 'x31y14', 'x30y13', 'x29y13', 'x28y13'</points>
        <t_values>0.00, 0.01, 0.03, 0.05, 0.07, 0.15, 0.18, 0.21, 0.22, 0.25, 0.30, 0.32, 0.36, 0.42, 0.50, 0.53, 0.56, 0.59, 0.62, 0.67, 0.69, 0.72, 0.75, 0.77, 0.79, 0.80, 0.81, 0.83, 0.85, 0.89, 0.92, 1.00</t_values>
        <id>right branch</id>
    </s3>
    <s4>
        <points>'x21y17', 'x21y16', 'x21y15', 'x21y14', 'x21y13', 'x21y12', 'x21y11', 'x21y10', 'x21y9'</points>
        <t_values>0.00, 0.06, 0.12, 0.18, 0.26, 0.40, 0.55, 0.68, 1.00</t_values>
        <id>bottom middle branch left</id>
    </s4>
    <s5>
        <points>'x28y13', 'x28y12', 'x28y11', 'x28y10'</points>
        <t_values>0.00, 0.10, 0.35, 1.00</t_values>
        <id>bottom middle branch right</id>
    </s5>
    <s6>
        <points>'x18y10', 'x19y10', 'x20y10', 'x21y10', 'x23y10', 'x24y10', 'x25y10', 'x26y10', 'x27y10', 'x28y10', 'x29y10', 'x30y10', 'x31y10', 'x32y10'</points>
        <t_values>0.00, 0.05, 0.06, 0.08, 0.11, 0.13, 0.15, 0.18, 0.21, 0.26, 0.35, 0.51, 0.66, 1.00</t_values>
        <id>pot top</id>
    </s6>
    <s7>
        <points>'x32y9', 'x32y8', 'x32y7', 'x33y5', 'x32y4', 'x31y3', 'x30y2', 'x29y1'</points>
        <t_values>0.00, 0.05, 0.13, 0.28, 0.72, 0.77, 0.83, 1.00</t_values>
        <id>pot right</id>
    </s7>
    <s8>
        <points>'x21y1'</points>
        <t_values>0.00</t_values>
        <id>pot detail</id>
    </s8>
    <s9>
        <points>'x21y1', 'x20y1', 'x19y2', 'x18y3', 'x17y3', 'x16y4', 'x16y5', 'x16y6', 'x16y7', 'x17y9', 'x17y10'</points>
        <t_values>0.00, 0.07, 0.13, 0.23, 0.29, 0.41, 0.60, 0.63, 0.67, 0.80, 1.00</t_values>
        <id>pot left</id>
    </s9>
    <s10>
        <points>'x21y1', 'x22y1', 'x23y1', 'x24y1', 'x25y1', 'x26y1', 'x27y1', 'x28y1'</points>
        <t_values>0.00, 0.11, 0.15, 0.19, 0.27, 0.47, 0.86, 1.00</t_values>
        <id>pot bottom</id>
    </s10>
</strokes>
```

## Clock

## Ice Cream

## Dog

## Chair

