from collections import defaultdict, deque
from backend.app.database import SessionLocal
from backend.app.models.init import Topics, TopicDependency


class TopicGraph:
    def __init__(self):
        self.graph = defaultdict(list)  # key: topic_id, value: list of dependent topic_ids
        self.reverse_graph = defaultdict(list)# key: topic_id, value: list of prerequisite topic_ids
        self.topic_titles = {} # Maps topic_id to title for readable output
        self.load_graph()

    def load_graph(self):
        """Fetch topics and dependencies from the database and build graph structure."""
        db = SessionLocal()
        topics = db.query(Topics).all()
        dependencies = db.query(TopicDependency).all()

       #Save topic titles
        for topic in topics:
         self.topic_titles[topic.id] = topic.title

       #Build the graph
        for dep in dependencies:
         self.graph[dep.prerequisite_id].append(dep.topic_id)
         self.reverse_graph[dep.topic_id].append(dep.prerequisite_id)

        db.close()


    def topological_sort(self):
        """Return a list of topic IDs in a valid study order using Kahn's algorithm."""
        in_degree = {node: 0 for node in self.topic_titles}
        for node in self.reverse_graph:
            in_degree[node] = len(self.reverse_graph[node])

        queue = deque([node for node in self.topic_titles if in_degree[node] == 0])
        ordered = []


        while queue:
            current = queue.popleft()
            ordered.append(current)   
            for neighbor in self.graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor) 
        return [self.topic_titles[tid] for tid in ordered]  # return titles for readability        
        
    def breadthfirst_from(self, start_title):
       """Breadth-First Search from a topic title: show what comes after it."""
       start_id = self.get_topic_id_by_title(start_title)
       if not start_id:
           return []
      
       visited = set()
       queue = deque([start_id])
       result = []

       while queue:
         current = queue.popleft()
         for neighbor in self.graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                result.append(self.topic_titles[neighbor])

       return result

    def depthfirst_from(self, start_title):
        """Depth-First Search from a topic title: explore paths deeper."""
        start_id = self.get_topic_id_by_title(start_title)
        if not start_id:
            return []

        visited = set()
        result = []

        def depthfirst(node):
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                   visited.add(neighbor)
                   result.append(self.topic_titles[neighbor])   
                   depthfirst(neighbor)    
        
        depthfirst(start_id)
        return result

      
    def get_topic_id_by_title(self, title):
        """Helper to get topic ID from title."""
        for tid, t_title in self.topic_titles.items():
            if t_title and t_title.lower() == title.lower():
               return tid
        return None