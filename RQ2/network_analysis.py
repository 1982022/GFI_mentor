import csv
import networkx as nx
from networkx.algorithms import bipartite
import numpy as np
import matplotlib.pyplot as plt
from itertools import count
from random import sample

def construct_network(repo_id, data):
    edges = data[repo_id]
    #print(edges)
    G = nx.Graph()
    for edge in edges:
        G.add_nodes_from([(edge[0], {"label": "newcomer"}),(edge[1], {"label": "expert"})])
    G.add_weighted_edges_from(edges)
    return G

def calcu_attri(G):
    number_of_nodes = G.number_of_nodes()
    number_of_edges = G.number_of_edges()
    expert = dict( (n,d['label']) for n,d in G.nodes().items() if d['label'] == 'expert')
    newcomer = dict( (n,d['label']) for n,d in G.nodes().items() if d['label'] == 'newcomer')
    
    ratio_of_expert = len(expert)/number_of_nodes
    ratio_of_newcomer = len(newcomer)/number_of_nodes
    
    avg_degree = (2*number_of_edges)/number_of_nodes
    weighted_avg_degree = (2*sum([item[1] for item in G.degree(weight='weight')]))/number_of_nodes
   
    degree_variance = np.average([(item[1]-avg_degree)**2 for item in nx.degree(G)])
    weighted_degree_variance = np.average([(item[1]-weighted_avg_degree)**2 for item in G.degree(weight='weight')])
    
    degree_centrality = nx.degree_centrality(G)
    degree_centrality = np.average(list(degree_centrality.values()))
    
    closeness_centrality = nx.closeness_centrality(G)
    closeness_centrality = np.average(list(closeness_centrality.values()))
    
    betweenness_centrality = nx.betweenness_centrality(G) 
    betweenness_centrality = np.average(list(betweenness_centrality.values()))
    
    number_connected_components = nx.number_connected_components(G)
    """
    print('ratio_of_expert: ', ratio_of_expert)
    print('ratio_of_newcomer: ', ratio_of_newcomer)
    print('avg_degree: ', avg_degree)
    print('weighted_avg_degree: ', weighted_avg_degree)
    print('degree_variance: ', degree_variance)
    print('weighted_degree_variance: ', weighted_degree_variance)
    print("degree centrality: ", degree_centrality.values())
    print("closeness centrality: ", closeness_centrality.values())
    print("betweenness centrality: ", betweenness_centrality.values())
    print("number_connected_components: ", number_connected_components)
    """
    return ratio_of_expert, ratio_of_newcomer, avg_degree, weighted_avg_degree, degree_variance, weighted_degree_variance, degree_centrality, closeness_centrality, betweenness_centrality, number_connected_components

def draw_network(G, picname):
    # simple way
    # nx.draw(G, with_labels=False)
    # node color
    groups = set(nx.get_node_attributes(G,'label').values())
    mapping = dict(zip(sorted(groups),count()))
    nodes = G.nodes()
    #colors = [mapping[G.nodes[n]['label']] for n in nodes]
    colors = []
    for node in G.nodes(data=True):
        if 'newcomer' in node[1]['label']:
            colors.append('darkorange')
        if 'expert' in node[1]['label']:
            colors.append('dodgerblue')
    # drawing nodes and edges separately so we can capture collection for colobar
    # pos = nx.spiral_layout(G,resolution=5)
    # pos = nx.shell_layout(G)
    pos = nx.spring_layout(G)
    ec = nx.draw_networkx_edges(G, pos, alpha=0.5)
    nc = nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=colors, node_size=[(v+1) * 10 for v in [item[1] for item in nx.degree(G)]], cmap=plt.cm.rainbow)
    #thick of edges
    for edge in G.edges(data='weight'):
        nx.draw_networkx_edges(G, pos, edgelist=[edge], width=edge[2])
    plt.savefig('./picc/'+picname+'.png')
    plt.clf()


if __name__ == '__main__':
    data = dict()
    file1 = open('network.csv', 'r')
    csv_reader = csv.reader(file1)
    next(csv_reader)
    """
    file2 = open('attri.csv', 'w')
    csv_writer = csv.writer(file2)
    csv_writer.writerow(['repo_id', 'ratio_of_expert', 'ratio_of_newcomer', 'weighted_avg_degree', 'weighted_degree_variance', 'degree_centrality', 'closeness_centrality', 'betweenness_centrality', 'number_connected_components'])
    """
    for row in csv_reader:
        if row[0] not in data.keys():
            data[row[0]] = [(row[1],row[2],int(row[3]))]
        else:
            data[row[0]].append((row[1],row[2],int(row[3])))
    numm = 0

    sample_repo = sample(data.keys(), 275)
    for repo_id in sample_repo:
        G = construct_network(repo_id, data)
        num_nodes = len(list(G.nodes))
        draw_network(G, repo_id)
        numm += 1
        print(numm)
        """
        calcu_attri(G)
        ratio_of_expert, ratio_of_newcomer, avg_degree, weighted_avg_degree, degree_variance, weighted_degree_variance, degree_centrality, closeness_centrality, betweenness_centrality, number_connected_components = calcu_attri(G)
        csv_writer.writerow([repo_id, ratio_of_expert, ratio_of_newcomer, weighted_avg_degree, weighted_degree_variance, degree_centrality, closeness_centrality, betweenness_centrality, number_connected_components])
        """
        """
        if repo_id == '54726900':
            draw_network(G, 'type0_54726900')
        if repo_id == '45945255':
            draw_network(G, 'type1_45945255')
        if repo_id == '137941174':
            draw_network(G, 'type2_137941174')
        """
    file1.close()
    #file2.close()