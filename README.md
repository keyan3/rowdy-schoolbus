# rowdy-schoolbus
## Berkeley CS 170 (Algorithms) Project

Approximation algorithm for a modified version of the NP-hard [minimum k-cut problem](https://en.wikipedia.org/wiki/Minimum_k-cut) with additional constraints. Applied [Simulated Annealing](https://en.wikipedia.org/wiki/Simulated_annealing) in final approach, though greedy algorithms were explored as well. Placed in top 12% of class in solution accuracy. 

Project spec can be found [here](https://d1b10bmlvqabco.cloudfront.net/attach/jhadltur59wtu/idril7rumak4d3/jocsqsxf370/CS_170_FA18_Project_Spec.pdf).

### Full problem statement

You are a tired, overworked teacher who has spent the last week organizing a field trip for your entire middle school. The night before the trip, you realize you forgot to plan the most important part – transportation! Fortunately, your school has access to a large fleet of buses. Being the caring teacher you are, you’d like to ensure that students can still end up on the same bus as their friends. After some investigative work on social media, you’ve managed to figure out exactly who is friends with who at your school and begin to assign students to buses with the intent of breaking up as few friendships as possible. You’ve only just begun when you receive a frantic email from one of the chaperones for the trip. The kids this year are particularly rowdy, and the chaperones have given you a list of groups of students who get too rowdy when they are all together. If any of these groups are seated assigned to the same bus, they will all have to be removed from the bus and sent home. Can you plan transportation while keeping both the students and the chaperones happy?

Formally, you’re given an undirected graph G = (V,E), an integer k, and an integer s, where each node in the graph denotes a student, and each edge (v1,v2) denotes that students v1 and v2 are friends. The integer k denotes the number of buses available and the integer s denotes the number of students that can fit on a single bus. Furthermore, you’re given a list L, where each element Lj is some subset of V which corresponds to a group that should be kept apart.

You must return a partition of G – a set of sets of vertices Vi such that V1 ∪ V2 ∪ V3 ∪...∪ Vk = V and ∀i != j, Vi ∩ Vj = ∅. Additionally, ∀i, 0 < |Vi| ≤ s. In other words, every bus must be non-empty, and must not have more students on it than its capacity allows.

Consider a vertex v to be valid if there is no i and j such that v ∈ Lj and Lj ⊆ Vi. In other words, a vertex is valid if it is not in a rowdy group whose members all end up on the same bus. For example, if one of the rowdy groups was ‘Alice’, ‘Bob’, and ‘Carol’, then putting ‘Alice’, ‘Bob’, ‘Carol’, and ’Dan’ on the same bus would lead to ‘Alice’, ‘Bob’, and ‘Carol’ being considered invalid vertices. However, a bus with just ‘Alice’, ‘Bob’, and ‘Dan’ would have no invalid vertices.

We’d like you to produce a partition that maximizes the percent of edges that occur between valid vertices in the same partition in the graph. The score for your partition is the percentage of edges (u, v) where u and v are both valid, and u, v ∈ Vi for some i. You’d like to produce a valid partition with as high a score as possible.
