import cfg
import dvg
# Matplotlib is optional; only used when printing graphs
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None
import networkx as nx

flow_edges = ""

def to_pdg(func, p = False, line_mapping = None):
    
    global flow_edges
    pdg = cfg.to_cfg(func, p, line_mapping)
    d = dvg.to_dvg(func, p, line_mapping)

    for g in d:
                
        for edge in g[1].edges:

            if pdg.has_edge(edge[0],edge[1], edge[2]):
                if 'label' in pdg.edges.get((edge[0],edge[1], edge[2])).keys():
                    l = pdg.edges.get((edge[0],edge[1], edge[2]))['label']
                    pdg.remove_edge(edge[0],edge[1], edge[2])
                    pdg.add_edge(edge[0],edge[1], edge[2], color='g', label = (l + '.' + g[0]))
                else:
                    pdg.remove_edge(edge[0],edge[1], edge[2])
                    pdg.add_edge(edge[0],edge[1], edge[2], color='g', label = g[0])
            else:

                pdg.add_edge(edge[0],edge[1], edge[2], color='r', label = g[0])


    colors = nx.get_edge_attributes(pdg,'color').values()
    lab = nx.get_edge_attributes(pdg,'label')

    if(p):
        print(pdg.edges)
        if plt is not None:
            nx.draw(pdg, with_labels = True, edge_color=colors)
            plt.show()

    labels = [x[1] for x in pdg.nodes if x[1] != "" and x != "return"]
    ret = len([x[1] for x in pdg.nodes if x == "return"]) > 0 
	
    return (pdg, labels, ret, len(d))


