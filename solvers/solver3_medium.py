import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import random
import math

###########################################
# Change this variable to the path to 
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./all_inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a 
# different folder
###########################################
path_to_outputs = "./outputs"

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []
    
    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints

def solve(graph, num_buses, size_bus, constraints):
    nodes = [n for n in graph.nodes()]
    rowdy_sets = [set(c) for c in constraints]
    total_edges = graph.number_of_edges()

    best_par, best_score = best_random_par(graph, nodes, num_buses, size_bus, constraints, total_edges, rowdy_sets)
    print(best_score)
    sim_par, sim_score = sim_anneal(num_buses, size_bus, best_par, nodes, graph, total_edges, best_score, rowdy_sets)
    print(sim_score)
    if sim_score > best_score:
        best_par = sim_par
        best_score = sim_score
    #mk_par, mk_score = capped_min_k_cut(graph, nodes, best_par, num_buses, size_bus, rowdy_sets)
    #print(mk_score)
    #if mk_score > best_score:
     #   best_par = mk_par
     #   best_score = mk_score

    return [[nodes[i] for i in p] for p in best_par]



def best_random_par(graph, nodes, num_buses, size_bus, constraints, total_edges, rowdy_sets):
    max_par = []
    max_par_score = -1
    rgcm = 0
    for _ in range(5000):
        cp = random_partit(graph.number_of_nodes(), num_buses, size_bus)
        c_graph = graph.copy()
        rgc = 0
        torem = set()
        for bus in cp:
            bus_names = set([nodes[i] for i in bus])
            for rg in rowdy_sets:
                if len(rg.intersection(bus_names)) == len(rg):
                    for r in rg: 
                    	torem.add(r)
        for r in torem:
        	c_graph.remove_node(r)
        c_score = score(nodes, c_graph, cp, total_edges)
        if c_score > max_par_score:
            max_par_score = c_score
            max_par = cp
    return max_par, max_par_score

# Returns a random (num_bus)-partition of the integers {0,..n-1} inclusive 
# where each partition contains less than size_bus items
def random_partit(n, num_buses, size_bus):
    par = [set() for i in range(num_buses)]
    remaining = n
    items = [i for i in range(n)]
    for i in range(len(par)):
        if items:
            pick = random.randint(0, remaining - 1)
            par[i].add(items[pick])
            items.pop(pick)
            remaining -= 1
    for item in items:
        success = False
        while not success:
            pick = random.randint(0, num_buses - 1)
            if len(par[pick]) <= size_bus - 1: 
                par[pick].add(item)
                success = True
    return par

def neighbor(num_buses, size_bus, partition, par_factor):
    #print("In neighbor:", partition)
    par = [set() for i in range(par_factor)]
    c_partition = [set(p) for p in partition]
    items = []
    shuffle_index = random.sample(range(0, num_buses), par_factor)
    shuffle_index.sort(reverse = True)
    #print(len(partition))
    #print(shuffle_index)
    for i in shuffle_index:
        for n in c_partition[i]:
            items.append(n)
        c_partition.pop(i)
    remaining = len(items)
    for i in range(len(par)):
        if items:
            pick = random.randint(0, remaining - 1)
            par[i].add(items[pick])
            items.pop(pick)
            remaining -= 1
    for item in items:
        success = False
        while not success:
            pick = random.randint(0, par_factor - 1)
            if len(par[pick]) <= size_bus - 1: 
                par[pick].add(item)
                success = True
    #print(par)
    return c_partition + par

def sim_anneal(num_buses, size_bus, start, nodes, graph, total_edges, cur_score, rowdy_sets):
    T = 20000
    i = 0
    par_factor = int(0.75 * num_buses)
    old_score = cur_score
    partition = start
    while T >= 0: 
        #print("Before neighbor:", partition)
        cp = neighbor(num_buses, size_bus, partition, par_factor)
        #print("After neighbor:", partition)
        c_graph = graph.copy()
        torem = set()
        for bus in cp:
            bus_names = set([nodes[i] for i in bus])
            for rg in rowdy_sets:
                if len(rg.intersection(bus_names)) == len(rg):
                    for r in rg: 
                        torem.add(r)
        for r in torem:
            c_graph.remove_node(r)
        c_score = score(nodes, c_graph, cp, total_edges)
        if c_score > old_score:
            old_score = c_score
            partition = cp
        #a = math.exp((-1 * c_score - (- 1 * old_score)/ T ))
        #if a > random.random():
        #    old_score = c_score
        #    partition = cp
            #print(1)
        i += 1
        T -= 1
        if i == 80:
            par_factor = int(0.75 * par_factor) + 1

            i = 0
    return partition, old_score


"""
def neighbor(graph, partition, shuffle, num_buses, size_bus):
	g = graph
	if shuffle == num_buses:
		return random_partit(g.number_of_nodes(), num_buses, size_bus)

	else:
		shuffle_list = []
		num_shuffle = num_buses - shuffle
		shuffle_index = random.sample(range(0, num_buses), shuffle)
		shuffle_index.sort(reverse = True)
		
		for i in shuffle_index:
			for n in partition[i]:
				shuffle_list.append(n)
			partition.pop(i)

		random.shuffle(shuffle_list)
"""
		
			
"""
def capped_min_k_cut(graph, nodes, par, num_buses, size_bus, rowdy_sets):
    n = graph.number_of_nodes()
    c_graph = graph.copy()
    #cp = best_random_par(graph, num_buses, size_bus, constraints)[0]
    node_to_part = {}
    p = 0
    for p_i in par:
        for n in p_i:
            node_to_part[nodes[n]] = p
        p += 1
    count = 0
    found_swap = True
    while found_swap and count < 10:
        found_swap = False
        for v in range(n):
            for u in range(n):
                if v != u and node_to_part[nodes[v]] != node_to_part[nodes[u]]:
                    swp_diff = swap_diff(nodes, graph, par, v, node_to_part[nodes[v]], u, node_to_part[nodes[u]], node_to_part)
                    if swp_diff > 0:
                        found_swap = True
                        par[node_to_part[nodes[v]]].add(u)
                        par[node_to_part[nodes[v]]].remove(v)
                        par[node_to_part[nodes[u]]].add(v)
                        par[node_to_part[nodes[u]]].remove(u)
                        temp = node_to_part[nodes[v]]
                        node_to_part[nodes[v]] = node_to_part[nodes[u]]
                        node_to_part[nodes[u]] = temp
        count += 1
    torem = set()
    for bus in par:
        bus_names = set([nodes[i] for i in bus])
        for rg in rowdy_sets:
            if len(rg.intersection(bus_names)) == len(rg):
                for r in rg: 
                    torem.add(r)
    for r in torem:
        c_graph.remove_node(r)
    return par, score(nodes, c_graph, par, graph.number_of_edges())

"""

def swap_diff(nodes, graph, par, v, p1, u, p2, node_to_part):
    w_v_p1 = len([1 for e in graph.edges([nodes[v]]) if node_to_part[e[1]] == p1])
    w_u_p2 = len([1 for e in graph.edges([nodes[u]]) if node_to_part[e[1]] == p2])
    w_u_p1 = len([1 for e in graph.edges([nodes[u]]) if node_to_part[e[1]] == p1])
    w_v_p2 = len([1 for e in graph.edges([nodes[v]]) if node_to_part[e[1]] == p2])
    return (w_v_p1 + w_u_p2) - (w_u_p1 + w_v_p2)


def score(nodes, c_graph, par, total_edges):
    node_to_part = {}
    p = 1
    for p_i in par:
        for n in p_i:
            node_to_part[nodes[n]] = p
        p += 1
    valid_ct = 0
    for u, v in c_graph.edges():
        if node_to_part[u] == node_to_part[v]:
            valid_ct += 1
    return valid_ct / total_edges


def test_min_cut():
    graph, num_buses, size_bus, constraints = parse_input("small")
    print(num_buses)
    print(size_bus)
    solution = best_random_par(graph, num_buses, size_bus, constraints)
    print(solution)

def test_sol():
    sum_score = 0
    for i in range(1035, 1047):
        graph, num_buses, size_bus, constraints = parse_input(str(i))
        print(num_buses)
        print(size_bus)
        solution = solve(graph, num_buses, size_bus, constraints)
        sum_score += solution[1]
    print(sum_score)


def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = ["medium"]
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    count_done = 0
    for size in size_categories:
        category_path = path_to_inputs + "/" + size
        output_category_path = path_to_outputs + "/" + size
        category_dir = os.fsencode(category_path)
        
        if not os.path.isdir(output_category_path):
            os.mkdir(output_category_path)

        for input_folder in os.listdir(category_dir):
            input_name = os.fsdecode(input_folder) 
            print(input_name)
            graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
            solution = solve(graph, num_buses, size_bus, constraints)
            count_done += 1
            progress = count_done / 331
            print("count done:", count_done)
            print("Percentage done:", progress)
            output_file = open(output_category_path + "/" + input_name + ".out", "w")

            #TODO: modify this to write your solution to your 
            #      file properly as it might not be correct to 
            #      just write the variable solution to a file
            for bus in solution:
                output_file.write("{}".format(bus))
                output_file.write('\n')

            output_file.close()

if __name__ == '__main__':
    main()





"""
def baked_in(graph, num_buses, size_bus, constraints):
    nodes = [n for n in graph.nodes()]
    for u, v in graph.edges():
        graph[u][v]['weight'] = 1
    rowdy_sets = [set(c) for c in constraints]
    cp = [['QARNSQQW', 'JRZZFXSD', 'NFLAVTPA', 'NDQGNCMO', 'IQMTWJVH', 'PTSDESJS', 'YQJWCFVV', 'CCIEUMJZ'],
        ['QHOEJNHQ', 'BAOATGZP', 'UETCKVAI', 'VYZBHITB', 'RIGSDSHF', 'RILDLSOT', 'PMOJZJYR', 'EEFAFIDH'],
        ['RVCBUYCZ', 'HVJTGNXD', 'YGZAAITD', 'TIOFGZNL', 'RWELWDOK', 'ZENYLVYC', 'ASZTUCPI', 'DYOVGRWP'],
        ['CBMPCGMY', 'VYYMUBDM', 'LNVVCAUB', 'TCBHLVRB', 'JXNBUNZI', 'SYVJOLOF', 'ICZIXTNX', 'QIASSHYQ'],
        ['AGKRUBAG', 'EXZSVOMY', 'IQHKLNID', 'VYFKHOCR', 'TFKZCDMP', 'QZZVAPOC', 'YBYZXUSL', 'CMIZRXVU']]
    c_graph = graph.copy()
    total_edges = c_graph.number_of_edges()
    rgc = 0
    torem = set()
    for bus in cp:
        bus_names = set(bus)
        for rg in rowdy_sets:
            if len(rg.intersection(bus_names)) == len(rg):
                rgc += 1
                for r in rg:
                    torem.add(r)
    for r in torem:
        	c_graph.remove_node(r)
    node_to_part = {}
    p = 1
    for p_i in cp:
        for n in p_i:
            node_to_part[n] = p
        p += 1
    valid_ct = 0
    for u, v in c_graph.edges():
        if node_to_part[u] == node_to_part[v]:
            valid_ct += 1
    print(rgc)
    return valid_ct / total_edges
"""
