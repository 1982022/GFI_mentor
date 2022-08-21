import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file1 = open('types.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)

repo_type = dict()
for row in csv_reader:
    repo_type[row[0]] = row[1]
file1.close()
# print(repo_type)

file2 = open('../attri.csv', 'r')
csv_reader = csv.reader(file2)
next(csv_reader)
type_attri = dict()
for row in csv_reader:
    if row[0] in repo_type.keys(): # sample repos
        if repo_type[row[0]] not in type_attri.keys():
            type_attri[repo_type[row[0]]] = [list(row[1:])]
        else:
            type_attri[repo_type[row[0]]].append(list(row[1:]))
    else:
        continue
file2.close()

frame_centralized = pd.DataFrame(type_attri['centralized mentoring'], columns = ['ratio_of_expert','ratio_of_newcomer','weighted_avg_degree','weighted_degree_variance','degree_centrality','closeness_centrality','betweenness_centrality','number_connected_components'])
frame_centralized.insert(frame_centralized.shape[1], 'type', 'centralized mentoring')

frame_decentralized = pd.DataFrame(type_attri['decentralized mentoring'], columns = ['ratio_of_expert','ratio_of_newcomer','weighted_avg_degree','weighted_degree_variance','degree_centrality','closeness_centrality','betweenness_centrality','number_connected_components'])
frame_decentralized.insert(frame_decentralized.shape[1], 'type', 'decentralized mentoring')

frame_collaborative = pd.DataFrame(type_attri['collaborative mentoring'], columns = ['ratio_of_expert','ratio_of_newcomer','weighted_avg_degree','weighted_degree_variance','degree_centrality','closeness_centrality','betweenness_centrality','number_connected_components'])
frame_collaborative.insert(frame_collaborative.shape[1], 'type', 'collaborative mentoring')

frame_distributed = pd.DataFrame(type_attri['distributed mentoring'], columns = ['ratio_of_expert','ratio_of_newcomer','weighted_avg_degree','weighted_degree_variance','degree_centrality','closeness_centrality','betweenness_centrality','number_connected_components'])
frame_distributed.insert(frame_distributed.shape[1], 'type', 'distributed mentoring')

frame = pd.concat([frame_centralized, frame_decentralized, frame_collaborative, frame_distributed], ignore_index = True)

frame.to_csv('sample_network_attri.csv')