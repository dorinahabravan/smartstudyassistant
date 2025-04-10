import requests
import re
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.init import Topics, TopicDependency
from backend.app.topic_graph import TopicGraph

ROADMAP_TOPICS = {
    "frontend": "Frontend Developer",
    "backend": "Backend Developer",
    "ai": "AI Engineer",
    "cyber-security": "Cyber Security Specialist",
    "python": "Python Developer",
    "react": "React Developer",
    "devops": "DevOps Engineer",
    "java": "Java Developer",
}


def get_build_id_from_homepage():
    print("🔍 Fetching build ID from homepage...")
    resp = requests.get("https://www.roadmap.sh")
    if resp.status_code != 200:
        raise Exception("❌ Failed to load roadmap.sh homepage")

    match = re.search(r"_next/data/([a-zA-Z0-9]+)/", resp.text)
    if match:
        return match.group(1)
    else:
        raise Exception("❌ Could not extract build ID from homepage")


def fetch_roadmap_json(slug: str, build_id: str):
    url = f"https://www.roadmap.sh/_next/data/{build_id}/{slug}.json"
    print(f"📡 Fetching roadmap JSON: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"❌ Failed to fetch roadmap JSON (status {response.status_code})")
    return response.json()


def seed_to_db(roadmap_data):
    roadmap = roadmap_data["pageProps"]["roadmap"]
    db: Session = SessionLocal()

    root = Topics(title=roadmap["title"], content="Auto-fetched from roadmap.sh", source="roadmap.sh")
    db.add(root)
    db.commit()
    db.refresh(root)

    node_map = {}
    for node in roadmap["nodes"]:
        t = Topics(title=node["title"], content="", source="roadmap.sh")
        db.add(t)
        db.commit()
        db.refresh(t)
        node_map[node["id"]] = t

    for node in roadmap["nodes"]:
        if node.get("parent"):
            parent = node_map.get(node["parent"])
            child = node_map.get(node["id"])
            if parent and child:
                dep = TopicDependency(topic_id=child.id, prerequisite_id=parent.id)
                db.add(dep)

    db.commit()
    db.close()
    print("✅ Roadmap topics seeded!")

    graph = TopicGraph()
    print("📘 Study Order:", graph.topological_sort())


# 🧪 CLI Entry Point
if __name__ == "__main__":
    print("🔎 Available roadmaps:")
    print(", ".join(ROADMAP_TOPICS.keys()))
    slug = input("💬 Enter roadmap slug: ").strip().lower()

    if slug not in ROADMAP_TOPICS:
        print("❌ Invalid slug.")
    else:
        try:
            build_id = get_build_id_from_homepage()
            data = fetch_roadmap_json(slug, build_id)
            seed_to_db(data)
        except Exception as e:
            print("🚨 Error:", e)
