import glob
import networkx as nx
import matplotlib.pyplot as plt
import yaml

charts = glob.glob("Helm stable Charts/*/Chart.yaml")
# sub_folder = glob.glob("Helm stable Charts/*/charts")
# req_file = glob.glob("Helm stable Charts/*/requirements.yaml")
#
# dep_charts = sub_folder + req_file
# dep_charts_unique = []
#
#
#
# for chart in dep_charts:
#     split_chart = chart.split("/")
#     conc_chart = split_chart[1]
#
#     if conc_chart not in dep_charts_unique:
#         dep_charts_unique.append(conc_chart)
#     else:
#         print(conc_chart, " is already in the array")
#
# print(len(dep_charts_unique), "charts with dependencies found")
# print(len(charts), "charts analyzed in total")

# create directed graph
G = nx.DiGraph()

for chart in charts:
    # add node to graph
    with open(chart, 'r') as stream:
        try:
            node_yaml = yaml.safe_load(stream)
            node = node_yaml['name'] + ' ' + node_yaml['version']
            G.add_node(node)
        except yaml.YAMLError as exc:
            print(exc)

    # find dependencies
    # method 1: charts/ directory
    # go one directory above (to get into the charts/ directory)
    split = chart.split("/")[:2]
    sub_directory = "/".join(split[:2]) + "/charts"
    sub_charts = glob.glob(sub_directory + "/*/Chart.yaml")

    for sub_chart in sub_charts:
        with open(sub_chart, 'r') as stream:
            try:
                dep_node_yaml = yaml.safe_load(stream)
                dep_node = dep_node_yaml['name'] + ' ' + dep_node_yaml['version']
                G.add_node(dep_node)
                G.add_edge(node, dep_node)
                print(node, "depends on", dep_node)

            except yaml.YAMLError as exc:
                print(exc)

    # method 2: requirements.yaml file
    split = chart.split("/")[:2]
    sub_directory = "/".join(split[:2])
    sub_charts = glob.glob(sub_directory + "/requirements.yaml")

    for sub_chart in sub_charts:
        with open(sub_chart, 'r') as stream:
            try:
                dep_node_yaml = yaml.safe_load(stream)['dependencies']
                # loop through all dependencies stored in the requirements.yaml file
                for dep in dep_node_yaml:
                    dep_node = dep['name'] + ' ' + dep['version']
                    G.add_node(dep_node)
                    G.add_edge(node, dep_node)
                    print(node, "depends on", dep_node)

            except yaml.YAMLError as exc:
                print(exc)


def trim_nodes(G, d):
    Gt = G.copy()
    to_be_removed = []
    dn = nx.degree(Gt)
    for n in Gt.nodes():
        if dn[n] <= d:
            to_be_removed.append(n)

    for i in to_be_removed:
        Gt.remove_node(i)

    return Gt


def run_statistics(G):
    degree = nx.degree_assortativity_coefficient(G)
    print("''''''''''''''''''''''''''''''''''''''''''''''''''''''")
    print("Graph Statistics")
    print("''''''''''''''''''''''''''''''''''''''''''''''''''''''")
    print("Degree Assortativity Coefficient", degree)
    print("''''''''''''''''''''''''''''''''''''''''''''''''''''''")


Gt = trim_nodes(G, d=0)
nx.draw_spring(Gt, with_labels=True, node_size=50, alpha=0.8, font_size=6, font_weight="light")
run_statistics(Gt)

plt.savefig('dependency-graph-helm.pdf')
