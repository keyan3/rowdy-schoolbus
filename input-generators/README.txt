Functions:

main
Calls each function once, writes the gml file.

name_generator
- input: number of students
- output: returns a list of unique names 

rowdy generator
- writes to parameters.txt
- introduces all rowdy conditions

prison_edges
Prisoners were defined in the design doc: Essentially well connected but disruptive nodes. This function adds an edge between our specified prisoners with everyone else.

intra_bus
Defines edge relations within the busses or our desired optimal solution. Introduces some well connected people per bus.

inter_bus
Defines edge relations between busses of our desired optimal solution. 

arbitrary
Adds several random edges for nodes that are not prisoners to allow for variability, preserves original properties of the graph and is not enough to significantly affect original solution.

pseudo_popular
Introduces nodes that are popular but are rowdy with themselves.


good_prisoners
Strongly connected nodes that are rowdy if they below on any other bus other than their optimum designated bus



