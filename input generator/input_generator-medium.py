import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import random


rowdy_list = []

def name_generator(numVertices):
	unique = set()
	names = []
	chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	index = 0
	while index < numVertices:
		value = "".join(random.choice(chars) for _ in range(8))
		if value not in unique: #names need to be unique
			unique.add(value)
			names.append(value)
			index += 1
	return names


def rowdy_generator(k, s, nodes):
	f = open('parameters.txt','w')
	f.write(str(k))
	f.write('\n')
	f.write(str(s))
	f.write('\n')
	#write rowdy crowd
	print('txt written 2')


	for i in range(1, k-1):
		curr_gp = (i * s) + (s-2)
		for j in range(1, k-1):
			if i != j:
				rowdy_list.append([nodes[curr_gp], nodes[j*s]])
				rowdy_list.append([nodes[curr_gp], nodes[j*s+s//2]])
				rowdy_list.append([nodes[curr_gp], nodes[j*s+s//4]])

	print('txt written 3')

	for i in range(s):
		for j in range(1, k-1):
			rowdy_list.append([nodes[i], nodes[j*s]])
			rowdy_list.append([nodes[i], nodes[j*s+s//2]])
			rowdy_list.append([nodes[i], nodes[j*s+s//4]])
	

	#prisoners - prisoners and jocks, prisoners and some people on each bus (pairwise rowdy) 


	print('txt written 4')
	#cross-prisoner rowdiness
	i = 0
	j = 0
	while i < s:
		while j < s:
			if i != j:
				rowdy_list.append([nodes[i], nodes[j]])
			j += 2
		for w in range(1, k - 1):
			index = i * w + (s - 2)
			rowdy_list.append([nodes[index], nodes[i]])
		i += 2

	#prisoner rowdy with good prisoners


	#good prisoners
	print('txt written 5')




	print('txt written 6')
	for l in rowdy_list:
		#towrite = '[' + '%s, '.join(l) + ']\n'
		f.write("{}".format(l))
		f.write('\n')

	print('txt written 7')
	f.close()

def prison_edges(k, s, graph, nodes):
	i = 0
	while i < s:
		j = s 
		while j < (k * s):
			graph.add_edge(nodes[i], nodes[j])
			j += 1
		i += 1

def intra_bus(k, s, graph, nodes):
	i = s 
	while i <= s * (k - 1):
		j = 0
		while j < s:
			graph.add_edge(nodes[i], nodes[i + j])
			graph.add_edge(nodes[i + s//2], nodes[i + j])
			graph.add_edge(nodes[i + s//4], nodes[i + j])
			graph.add_edge(nodes[i + s//6], nodes[i + j])
			graph.add_edge(nodes[i + s//8], nodes[i + j])
			j += 2
		i += s

def inter_bus(k, s, graph, nodes):
	i = s 
	while i < s * (k - 2):
		j = 0
		while j < s:
			#jocks with friends in next busses
			graph.add_edge(nodes[i], nodes[i + s + j])
			graph.add_edge(nodes[i + s//2], nodes[i + s + j])
			graph.add_edge(nodes[i + s//4], nodes[i + s + j])
			graph.add_edge(nodes[i + s//6], nodes[i + s + j])
			graph.add_edge(nodes[i + s//8], nodes[i + s + j])
			rowdy_list.append([nodes[i], nodes[i + s + j - 1], nodes[i + s + j - 2]])
			rowdy_list.append([nodes[i], nodes[i + s + j - 1], nodes[i + s + j - 3 ] ])
			j += 4
		i += s

def arbitrary(k, s, graph, nodes):
	for i in range(k * s):
		graph.add_edge(nodes[random.randint(s + 1, k * s - 1)], nodes[random.randint(s + 1, k * s - 1)])

def pseudo_popular(num, k, s, graph, nodes):
	for i in range(num):
		val = random.randint(s, s * (k - 1))
		for i in range((k//2) * s):
			graph.add_edge(nodes[val - s//2], nodes[random.randint(1, k * s - 1)])
		
		rowdy_list.append([nodes[val - s//2]])
		



def good_prisoners(k, s, graph, nodes): #rowdy with all other jocks except for the ones in their respective bus
	for i in range(1, k - 1):
		index = i * s + (s - 2) 
		for j in range(k * s):
			graph.add_edge(nodes[index], nodes[j])


def main():
	k = 10 #number of buses 
	s = 25 #number of students per bus
	numVertices = 250
	assert(k * s == numVertices)
	nodes = name_generator(numVertices)
	graph = nx.Graph()

	#append all nodes
	for n in nodes:
		graph.add_node(n)
	
	#creates well connected rowdy doods
	prison_edges(k, s, graph, nodes)

	#edges between nodes in a bus
	intra_bus(k, s, graph, nodes)

	#arbitrary edges
	arbitrary(k, s, graph, nodes)

	#inter-bus relations
	inter_bus(k, s, graph, nodes)

	#pseudo_popular people (well connected, rowdy with themselves) 
	pseudo_popular(k, k, s, graph, nodes) 

	#nx.draw(graph)
	#plt.show()

	#parameters
	print('txt written 1')

	rowdy_generator(k, s, nodes)

	print('txt written 5')

	#write to GML file 
	nx.write_gml(graph, "graph.gml")
	
	print('graph gend')

	f1 = open('output.out', 'w')
	for i in range(k):
		local_lst = []
		for j in range(s):
			local_lst.append(nodes[i*s + j])
		f1.write("{}".format(local_lst))
		f1.write('\n')

	f1.close()


if __name__ == '__main__':
    main()


	


