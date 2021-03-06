import networkx as nx
import matplotlib.pyplot as plt


class Road:
    
    def __init__(self, src, dest, time_func, name=None):
        ''' Constructs a Road from src to dest, using the flow function time_func, with a label. '''
        self.G = None
        self.name = name
        self.src = src
        self.dest = dest
        self.time_func = time_func
        self.vehicles = []
        self.flow_time = time_func(0)
        self.free_flow_time = self.flow_time
    
    def recalc(self):
        ''' Recalculates the flow time for the current traffic. '''
        self.flow_time = self.time_func(len(self.vehicles))
    
    def number_of_vehicles(self):
        ''' Returns the amount of vehicles on this road. '''
        return len(self.vehicles)
    
    def add_vehicle(self, n=1):
        ''' Adds a starting vehicle on this road. Updates the flow time. '''
        self.vehicles.append(0)
        self.recalc()
    
    def pop_vehicle(self, n=1):
        ''' Removes a vehicle from this road. Updates the flow time. '''
        # TODO: iterate through and pop all expired vehicles at once
        if n is 1:
            self.vehicles.pop(0)
        else:
            for i in range(n):
                self.vehicles.pop(0)
        self.recalc()
    
    def __repr__(self):
        return 'Road(\'{}\': \'{}\'->\'{}\')'.format(self.name, self.src, self.dest)


class Network:
    
    def __init__(self):
        ''' Constructs an empty network. '''
        self.G = nx.MultiDiGraph()
    
    def add_city(self, n):
        ''' Adds a city with the name n. '''
        self.G.add_node(n)
    
    def add_cities_from(self, cities):
        ''' Adds cities whose names are in the list cities. '''
        self.G.add_nodes_from(cities)
    
    def remove_city(self, n):
        ''' Removes a city with the name n. '''
        self.G.remove_node(n)
    
    def remove_cities_from(self, cities):
        ''' Removes cities whose names are in the list cities. '''
        self.G.remove_nodes_from(cities)
    
    def add_road(self, road):
        ''' Adds a road to the network. '''
        road.G = self
        self.G.add_edge(road.src, road.dest, road=road)
    
    def add_roads_from(self, roads):
        ''' Adds roads to the network. '''
        edges = len(roads) * [None] 
        for i, road in enumerate(roads):
            edges[i] = (road.src, road.dest, {'road': road, 'free_flow_time': road.free_flow_time})
            road.G = self
        self.G.add_edges_from(edges)
    
    def remove_road(self, n1, n2):
        ''' Removes road from n1 to n2. '''
        self.G.remove_edge(n1, n2)
    
    def remove_roads_from(self, roads):
        ''' Removes roads in list of pairds roads. '''
        self.G.remove_edges_from(roads)
    
    def draw(self, save=None):
        ''' Draws/Saves a visual representation of the network. '''
        plt.clf()
        nx.draw(self.G, with_labels=True, node_color='lightgrey', font_weight='bold', font_color='black')
        plt.show()
        if save is not None:
            plt.savefig(save)
        
    def fastest_path(self, source, attr, visited, total_time):
        ''' Seeks the fastest path from source using attr key. '''
        neighbors = self.G[source]
        if len(neighbors) is 0:
            return visited, total_time
        
        best, best_key, best_time = None, None, float('inf')
        for key, succ in neighbors.items():
            for edge in succ.values():
                road = edge['road']
                time = road.__getattribute__(attr)
                if time <= best_time:
                    best, best_key, best_time = road, key, time

        total_time += best_time
        visited.append((source, best_key))
        return self.fastest_path(best_key, attr, visited, total_time)
    
    #def social_path(self, src):
    #    ''' Returns the fastest social path. '''
    #    return self.fastest_path(src, 'flow_time', [], 0)
    
    def egoist_path(self, src):
        ''' Returns the fastest egoist path. '''
        return self.fastest_path(src, 'flow_time', [], 0)

    
G = Network()
G.add_city('Start')
G.add_city('End')
G.add_city('A')
G.add_city('B')
G.add_road(Road('Start', 'A', lambda N: N/100, 't=N/100'))
G.add_road(Road('Start', 'B', lambda N: 45, 't=45'))
G.add_road(Road('A', 'B', lambda N: 0, 't=0'))
G.add_road(Road('A', 'End', lambda N: 45, 't=45'))
G.add_road(Road('B', 'End', lambda N: N/100, 't=N/100'))
G.draw()

for i in range(4000):
    for node in G.G.nodes():
        for edges in G.G[node].values():
            for edge in edges.values():
                edge['road'].add_vehicle()

#print("social:", list(G.social_path('Start')))
print("egoist:", list(G.egoist_path('Start')))