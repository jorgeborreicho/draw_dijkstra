# draw_dijkstra
A little app I made that can be used to run Dijkstra’s algorithm and draw a graphical representation of the computed shortest path.

This app takes a list of edges (the connections between the nodes of a graph) and their corresponding weights or distance values as the input. It also requires that user indicates the origin and destination nodes. It then runs the Dijkstra’s algorithm to determine the shortest path.
 
The first version just displayed the list of nodes corresponding to the shortest path but then I thought it could be nicer to visualize the path. I decided to use networkx together with matplotlib to draw the computed shortest path. 
 
You can try changing the way the nodes connect to each other by editing the graph definition in the text box. I think the required format is self-explanatory but if you mess it up just click on the reset button to start over.

I found out later that networkx also comes with a Dijkstra’s algorithm implementation... but that would have been too easy. 

Cheers!
