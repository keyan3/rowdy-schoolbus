import sys
import os
#import json
import matplotlib.pyplot as plt
from output_scorer import score_output

make_graphs = True
version_name = 'YOURNAME'

path_to_inputs = "./all_inputs"
path_to_outputs = "./outputs"
path_to_graphs = "./graphs"
size_categories = ["small", "medium", "large"]

def score_all_outputs(output_folder, silent=True):
    all_scores = {}
    for size in size_categories:
        category_scores = {}
        category_path = path_to_inputs + "/" + size
        output_category_path = output_folder + "/" + size
        
        loaded_cached = False
        '''
        cached_filename = output_folder + "/" + size + "_cached_scores.json"
        try:
            print("Looking for cached file: {}".format(cached_filename))
            with open(cached_filename, "r") as cached_file:
                print("Loading from cached evaluation scores for " + size + "...")
                category_scores = json.load(cached_file)
                print("Read {} successfully.".format(cached_filename))
                loaded_cached = True
        except FileNotFoundError as e:
            pass
        '''
        
        if not loaded_cached:
        
            category_dir = os.fsencode(category_path)
            
            if not os.path.isdir(output_category_path):
                os.mkdir(output_category_path)

            for input_folder in os.listdir(category_dir):
                input_name = os.fsdecode(input_folder) 
                score, msg = score_output(category_path + "/" + input_name, output_category_path + "/" + input_name + ".out")
                if not silent:
                    print("{}-{} scored {}".format(size, input_name, score))
                category_scores[input_name] = max(score, 0)
            '''
            with open(cached_filename, "w") as cached_file:
                json.dump(category_scores, cached_file)
            '''
        all_scores[size] = category_scores
    return all_scores
    
def make_histogram(name, size, scores):
    fname = path_to_graphs + "/" + name + "-" + size + "-density" +".png"
    unlabeled_scores = []
    for challenge in scores.keys():
        unlabeled_scores.append(scores[challenge])
    plt.hist(unlabeled_scores, 100, (0, 1))
    plt.xlabel("Score")
    plt.ylabel("Number of inputs")
    plt.title("Density of " + size + " " + name)
    plt.savefig(fname)
    plt.clf()

def make_curve_graph(name, size, scores):
    fname = path_to_graphs + "/" + name + "-" + size + "-curve" + ".png"
    unlabeled_scores = []
    for challenge in scores.keys():
        unlabeled_scores.append(scores[challenge])
    unlabeled_scores.sort()
    plt.plot(unlabeled_scores)
    plt.xlabel("(Sorted) input index")
    plt.ylabel("Score")
    plt.axis((0, len(unlabeled_scores), 0, 1))
    plt.title("Sorted scores for " + size + " " + name)
    plt.savefig(fname)
    plt.clf()

def compute_leaderboard_score(all_scores):
    total = 0
    count = 0
    for size in size_categories:
        category_scores = all_scores[size]
        for instance in category_scores.keys():
            total += category_scores[instance]
        count += len(category_scores)
    return total / count

if __name__ == "__main__":
    print("Will do: {}".format(size_categories))
    if not os.path.isdir(path_to_graphs):
        os.mkdir(path_to_graphs)
    
    old_scores = score_all_outputs(path_to_outputs, False)
    
    print("Leaderboard score: {}".format(compute_leaderboard_score(old_scores)))
    
    if make_graphs:
        for size in size_categories:
            make_histogram(version_name, size, old_scores[size])
            make_curve_graph(version_name, size, old_scores[size])
