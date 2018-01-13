
'''


*****************************************************************************************
Copyright (c) 2017 Jorge Borreicho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*****************************************************************************************


'''

import sys
import math 
import networkx as nx
import matplotlib.pyplot as plt


from PyQt5.QtWidgets import (QWidget, QMainWindow, QGridLayout, QTextEdit, QLineEdit, QToolTip, QPushButton, QApplication, QMessageBox, QLabel)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.QtCore import QCoreApplication

#
# dijkstra_shortest_path() 
#
# This function uses the Dijkstra's Algorithm to determine the shortest path between nodes
#
def dijkstra_shortest_path(source_node, destination_node, connection_weights):
    
    #create a set with all the nodes
    nodes = set()
    nodes.add(source_node)
    nodes.add(destination_node)
    for node_a, node_b in connection_weights.keys():
        nodes.add(node_a)
        nodes.add(node_b)

    #create two dictionaries to store distances and paths to be used in algorithm execution   
    dist = dict()
    via = dict()
    for node in nodes:
        dist[node] = math.inf
        via[node] = None
    dist[source_node] = 0
    
    #create an empty set to keep track of the visited nodes
    visited_nodes = set()
    
    #run Dijkstra's 
    
    for _ in range(len(nodes)):#while there are nodes left to visit 
        min_dist = math.inf
        for node in (nodes - visited_nodes):#determine the next node to be visited
            if dist[node] < min_dist:
                min_dist = dist[node]
                visited_node = node
                
        for node in nodes:
            try:
                if dist[visited_node] + connection_weights[(visited_node, node)] < dist[node]:
                    dist[node] = dist[visited_node] + connection_weights[(visited_node, node)]
                    via[node] = visited_node
            except KeyError: #exception occurs when there is no connection between the visited_node and this node 
                pass
            try:
                if dist[visited_node] + connection_weights[(node, visited_node)] < dist[node]: #same if clause but considering the oposite direction 
                    dist[node] = dist[visited_node] + connection_weights[(node, visited_node)] 
                    via[node] = visited_node                
            except KeyError: #exception occurs when there is no connection between the visited_node and this node 
                pass
    
        visited_nodes.add(visited_node)
    

    #finaly use the via to retrieve the shortest path
    #dist stores the minimal distance to all visited nodes
    shortest_path = [destination_node]
    node = destination_node
    while via[node] is not None:
        shortest_path.insert(0, via[node])
        node = via[node]
        
    return shortest_path, dist[destination_node]

#
# draw_shortest_path()
#
# This function calls dijkstra_shortest_path() and draws the shortest path  
#    
    
def draw_shortest_path(source_node, destination_node, connection_weights):
    
    #create a set with all the nodes
    nodes = set()
    nodes.add(source_node)
    nodes.add(destination_node)
    for node_a, node_b in connection_weights.keys():
        nodes.add(node_a)
        nodes.add(node_b)

    #create a graph    
    graph = nx.Graph()
    for node in nodes:
        graph.add_node(node)
    for node_a, node_b in connection_weights.keys():
        graph.add_edge(node_a, node_b, label = connection_weights[(node_a, node_b)], color='black',weight=1)
    
    #run Dijkstra's algorithm
    shortest_path, distance_to_destination = dijkstra_shortest_path(source_node, destination_node, connection_weights)
    
    #highlight the shortest path in the graph
    edge_labels = nx.get_edge_attributes(graph,'label')
    
    for i in range(len(shortest_path)):
        try:
            graph.remove_edge(shortest_path[i], shortest_path[i+1])
            graph.add_edge(shortest_path[i], shortest_path[i+1], label = edge_labels[(shortest_path[i], shortest_path[i+1])], color='r',weight=4)
        except IndexError:
            pass
        except KeyError: #when edge_labels dict key are inverted
            graph.add_edge(shortest_path[i], shortest_path[i+1], label = edge_labels[(shortest_path[i+1], shortest_path[i])], color='r',weight=4)
    
    
    #draw the graph
    #nx.draw(graph, with_labels=True, node_color='skyblue', node_size=1500, width=2.0, edge_cmap=plt.cm.Blues)
    pos = nx.spring_layout(graph)
    edges = graph.edges()
    colors = [graph[u][v]['color'] for u,v in edges]
    weights = [graph[u][v]['weight'] for u,v in edges]
    edge_labels = nx.get_edge_attributes(graph,'label')
    
    fig = plt.figure(num="Draw Dijkstra")
    fig.suptitle("Shortest Path from " + source_node + " to " + destination_node + " (Distance = " + str(distance_to_destination) + ")\n Path: " + str(shortest_path), fontsize=14)
    ax = fig.add_subplot(1,1,1) # one rows, one column, first plot
    
    nx.draw(graph, ax = ax, with_labels=True, pos = pos, edges=edges, edge_color=colors, width=weights, node_color='skyblue', node_size=1500)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels = edge_labels)

    plt.show()
    
    return fig


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()  
        
        self.button_map = dict()
        self.initUI()
               
    def initUI(self):
    
    
        self.input = QTextEdit()
        self.input.setText('''{
    ("A","B"):10,
    ("A","C"):100,
    ("B","D"):100,
    ("C","D"):10,
    ("A","E"):200,
    ("B","F"):200,
    ("C","G"):200,
    ("D","H"):200,
    ("G","H"):10,
    ("F","E"):10,
    ("F","G"):100,
    ("E","H"):100,
    ("A","I"):1000,
    ("B","J"):1000,
    ("I","J"):10,
    ("F","L"):1000,
    ("E","M"):1000,
    ("L","M"):10
}''')
        
        self.label_a_node = QLabel('Origin Node')
        self.a_node = QLineEdit()
        self.a_node.setText("F")
        
        self.label_b_node = QLabel('Destination Node')
        self.b_node = QLineEdit()
        self.b_node.setText("M")
            
        self.button_reset = QPushButton('Reset', self)
        self.button_reset.resize(self.button_reset.sizeHint())
        self.button_reset.clicked.connect(self.buttonHandler)  
        self.button_map[self.button_reset] = "reset"     
        
        self.button_run = QPushButton('Run Dijkstra', self)
        self.button_run.resize(self.button_run.sizeHint())
        self.button_run.clicked.connect(self.buttonHandler)  
        self.button_map[self.button_run] = "run"
        
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.input, 0, 0, 4, 4)
        self.grid.addWidget(self.label_a_node, 4, 0, 1, 1)
        self.grid.addWidget(self.a_node, 4, 1, 1, 1)
        self.grid.addWidget(self.label_b_node, 4, 2, 1, 1)
        self.grid.addWidget(self.b_node, 4, 3, 1, 1)
        self.grid.addWidget(self.button_reset, 5, 2, 1, 1)
        self.grid.addWidget(self.button_run, 5, 3, 1, 1)
        
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.grid)
           
        #Window
        self.setCentralWidget(self.central_widget)
        self.setGeometry(1200, 300, 500, 500)
        self.setWindowTitle('Draw Dijkstra')
        self.setWindowIcon(QIcon('LisboaAppsIcon.png'))
        
        self.show()
    
    def buttonHandler(self):
        action = self.button_map[self.sender()] 
        if action == "reset":
            self.a_node.setText("F")
            self.b_node.setText("M")
            self.input.setText('''{
    ("A","B"):10,
    ("A","C"):100,
    ("B","D"):100,
    ("C","D"):10,
    ("A","E"):200,
    ("B","F"):200,
    ("C","G"):200,
    ("D","H"):200,
    ("G","H"):10,
    ("F","E"):10,
    ("F","G"):100,
    ("E","H"):100,
    ("A","I"):1000,
    ("B","J"):1000,
    ("I","J"):10,
    ("F","L"):1000,
    ("E","M"):1000,
    ("L","M"):10
}''')
        if action == "run":
            plt.close("all") #closes all matplotlib windows
            a_node = self.a_node.text()
            b_node = self.b_node.text()
            edges = eval(self.input.toPlainText())
            self.fig = draw_shortest_path(a_node, b_node, edges)
            
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()        
            
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_()) 