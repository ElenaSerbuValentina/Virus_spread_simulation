# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 15:54:19 2023

@author: elens
"""

import igraph
import numpy as np
from igraph import *
from matplotlib import pyplot as plt
g =Graph.Read_GML("C:\\Users\\mayo_\\Desktop\\U Milan\\Cursos\\Graph Theory and Discrete Mathematics\\Assignments\\Fourth\\graph6.gml")




layout = g.layout("fr")
plot(g, layout = layout)




cluster = g.community_edge_betweenness()
cluster.optimal_count
member_list = cluster.as_clustering().membership
member_list = np.array(member_list)




# (r start from, python from id 0)
degree = g.degree()
hub = np.where(np.array(degree)>=7)[0]
hub




cluster.optimal_count




member_list




#color_dict = {0:"red",1:"green", 2:"blue", 3:"violet", 4:"orange", 5:"yellow"}
color_dict = {0:"green",1:"yellow", 2:"blue", 3:"orange"}




vertex_color = [color_dict[n] for n in member_list]
for h in hub:
vertex_color[h] = "red"




# age graph
plot(cluster.as_clustering(), mark_groups = True, layout=layout,
vertex_label=[int(n) for n in g.vs["age"]], vertex_label_color="black", vertex_color=vertex_color,
vertex_size=20)




#path = save + "graphbyage.png"
#p.save(path)
#p




age = np.array(g.vs["age"], dtype=np.int)
cluster0_age = age[member_list==0]
min_max_0 = (np.min(cluster0_age),np.max(cluster0_age))
cluster1_age = age[member_list==1]
min_max_1 = (np.min(cluster1_age),np.max(cluster1_age))
cluster2_age = age[member_list==2]
min_max_2 = (np.min(cluster2_age),np.max(cluster2_age))




cluster3_age = age[member_list==3]
min_max_3 = (np.min(cluster3_age),np.max(cluster3_age))





#id graph
plot(cluster.as_clustering(), mark_groups = True, layout=layout,
vertex_label=[int(n) for n in g.vs["id"]], vertex_label_color="black", vertex_color=vertex_color,
vertex_size=20)




#name graph
plot(cluster.as_clustering(), mark_groups = True, layout=layout,
vertex_label=[int(n) for n in g.vs["name"]], vertex_label_color="black", vertex_color=vertex_color,
vertex_size=20)





nsimulation = 1000
max_t = 50
starting_point = 40




# mean number of infected over time
p_sim = np.zeros((70,max_t))
# mean probability of infection over time
p_sim2 = np.zeros((70,max_t))
adj = g.get_adjacency()





for s in range(0,nsimulation):
infected = [starting_point]
noinf = np.zeros((70,70))
noinf[infected[0], :] = 1
p_hist = np.zeros((70,max_t))
p_hist[infected[0], 0] = 1

p_hist2 = np.zeros((70,max_t))
p_hist2[infected[0], 0] = 1
for t in range(1,max_t):
for i in infected:
noinf[i, :] = 1
noinf[:,i] = adj[:,i]
temp = np.sum(noinf, axis=1, keepdims=True)
p = temp*0.2
p[temp >=5] = 1
u = np.random.uniform(0,1,(70,1))
new = u <= p
infected = np.where(new==True)[0]
p_hist[:,t] = new[:,0]
p_hist2[:,t] = p[:,0]

p_sim = p_sim + p_hist
p_sim2 = p_sim2 + p_hist2




p_sim = p_sim / nsimulation
p_sim2 = p_sim2 / nsimulation





psim_cluster0 = p_sim[member_list==0,:]
psim_cluster1 = p_sim[member_list==1,:]
psim_cluster2 = p_sim[member_list==2,:]
psim_cluster3 = p_sim[member_list==3,:]




mean_inf_cluster0 = np.sum(psim_cluster0,axis=0,keepdims=True)/psim_cluster0.shape[0]
mean_inf_cluster1 = np.sum(psim_cluster1,axis=0,keepdims=True)/psim_cluster1.shape[0]
mean_inf_cluster2 = np.sum(psim_cluster2,axis=0,keepdims=True)/psim_cluster2.shape[0]
mean_inf_cluster3 = np.sum(psim_cluster3,axis=0,keepdims=True)/psim_cluster3.shape[0]




max_time_0 = np.argmax(mean_inf_cluster0)
max_time_1 = np.argmax(mean_inf_cluster1)
max_time_2 = np.argmax(mean_inf_cluster2)
max_time_3 = np.argmax(mean_inf_cluster3)




print(max_time_0)
print(max_time_1)
print(max_time_2)
print(max_time_3)





label0 = "age: " + str(min_max_0[0]) + " - " + str(min_max_0[1])
label1 = "age: " + str(min_max_1[0]) + " - " + str(min_max_1[1])
label2 = "age: " + str(min_max_2[0]) + " - " + str(min_max_2[1])
label3 = "age: " + str(min_max_3[0]) + " - " + str(min_max_3[1])




plt.plot(mean_inf_cluster0.T, color="red", label=label0)
plt.plot(mean_inf_cluster1.T, color="green", label=label1)
plt.plot(mean_inf_cluster2.T, color="blue", label=label2)
plt.plot(mean_inf_cluster3.T, color="orange", label=label3)




plt.vlines(max_time_0,0,1,colors="red", linestyles="dashed")
plt.vlines(max_time_1,0,1,colors="green", linestyles="dashed")
plt.vlines(max_time_2,0,1,colors="blue", linestyles="dashed")
plt.vlines(max_time_3,0,1,colors="orange", linestyles="dashed")




plt.xlabel("time")
plt.ylabel("percentage of infected")
plt.title("percentage of infected by clusters over time starting from node id: " + str(starting_point))
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.xticks([max_time_0,max_time_1,max_time_2]);