import requests
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.init import Topics, TopicDependency
from backend.app.topic_graph import TopicGraph

# Available roadmap slugs you can query
ROADMAP_SLUGS = {
    "frontend": "Frontend Developer",
    "backend": "Backend Developer",
    "ai": "AI Engineer",
    "cyber-security": "Cyber Security Specialist",
    "python": "Python Developer",
    "react": "React Developer",
    "devops": "DevOps Engineer",
    "java": "Java Developer",
}

GRAPHQL_ENDPOINT = "https://api.roadmap.sh/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "Origin": "https://roadmap.sh",
    "Referer": "https://roadmap.sh/",
    "User-Agent": "SmartStudyAssistant/1.0"
}


def fetch_roadmap_topics(slug: str):
    query = """
    query Roadmap($slug: String!) {
      roadmap(slug: $slug) {
        id
        title
        nodes {
          id
          title
          parent
        }
      }
    }
    """

    response = requests.post(
        GRAPHQL_ENDPOINT,
        headers=HEADERS,
        json={"query": query, "variables": {"slug": slug}}
    )

    if response.status_code != 200:
        raise Exception(f"❌ GraphQL request failed with status {response.status_code}")

    data = response.json()
    roadmap = data.get("data", {}).get("roadmap")
    if not roadmap:
        raise Exception("❌ Invalid response or roadmap not found")

    print(f"✅ Fetched roadmap: {roadmap['title']}")
    return roadmap


def seed_roadmap_to_db(roadmap):
    db: Session = SessionLocal()

    root_topic = Topics(
        title=roadmap["title"],
        content=f"Auto-fetched roadmap from roadmap.sh",
        source="roadmap.sh"
    )
    db.add(root_topic)
    db.commit()
    db.refresh(root_topic)

    node_map = {}
    for node in roadmap["nodes"]:
        topic = Topics(
            title=node["title"].strip(),
            content="",
            source="roadmap.sh"
        )
        db.add(topic)
        db.commit()
        db.refresh(topic)
        node_map[node["id"]] = topic

    # Build dependencies
    for node in roadmap["nodes"]:
        if node["parent"]:
            child = node_map.get(node["id"])
            parent = node_map.get(node["parent"])
            if child and parent:
                dep = TopicDependency(
                    topic_id=child.id,
                    prerequisite_id=parent.id
                )
                db.add(dep)

    db.commit()
    db.close()

    print("✅ Topics seeded from roadmap.sh")
    graph = TopicGraph()
    print("📘 Study Order:", graph.topological_sort())


# 🧪 CLI Test
if __name__ == "__main__":
    print("🔎 Available roadmaps:\n" + ", ".join(ROADMAP_SLUGS.keys()))
    slug = input("💬 Enter a roadmap slug: ").strip().lower()

    if slug not in ROADMAP_SLUGS:
        print("❌ Invalid slug.")
    else:
        try:
            roadmap = fetch_roadmap_topics(slug)
            seed_roadmap_to_db(roadmap)
        except Exception as e:
            print(f"🚨 Error: {e}")
