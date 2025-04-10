from backend.app.topic_graph import TopicGraph

graph = TopicGraph()


print("\n Study Order (Topological Sort):")
print(graph.topological_sort())

print("\n Topics after 'Functions' (BFS):")
print(graph.breadthfirst_from("Functions"))

print("\n Deep path from 'Functions' (DFS):")
print(graph.depthfirst_from("Functions")) 