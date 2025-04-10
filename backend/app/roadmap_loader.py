import json
import os
from sqlalchemy.orm import Session
from backend.app.models.init import Topics, TopicDependency
from backend.app.database import SessionLocal
from backend.app.topic_graph import TopicGraph

def fetch_and_add_from_github_roadmap(slug: str):
    print(f"\n📡 Fetching roadmap: {slug}")
    
    backup_path = f"app/roadmap_backups/{slug}.json"
    if not os.path.exists(backup_path):
        print(f"❌ No local roadmap found for slug '{slug}'")
        return
    
    with open(backup_path, "r", encoding="utf-8") as f:
        roadmap_data = json.load(f)

    db: Session = SessionLocal()

    main_topic = roadmap_data.get("name", slug).strip()
    print(f"\n📘 Main topic: {main_topic}")

    # Check if already exists
    existing = db.query(Topics).filter(Topics.title.ilike(main_topic)).first()
    if existing:
        print(f"⚠️ '{main_topic}' already exists. Deleting it to reload...")
        db.query(TopicDependency).filter(
            (TopicDependency.topic_id == existing.id) | 
            (TopicDependency.prerequisite_id == existing.id)
        ).delete()
        db.delete(existing)
        db.commit()

    main_topic_obj = Topics(title=main_topic, content="", source="roadmap.sh")
    db.add(main_topic_obj)
    db.commit()
    db.refresh(main_topic_obj)

    topic_map = {}
    topic_list = roadmap_data.get("topics", [])
    for t in topic_list:
        t_obj = Topics(title=t["title"], content="", source="roadmap.sh")
        db.add(t_obj)
        db.commit()
        db.refresh(t_obj)
        topic_map[t["id"]] = t_obj

    # Add dependencies
    for t in topic_list:
        for dep in t.get("dependencies", []):
            if dep in topic_map:
                db.add(TopicDependency(
                    topic_id=topic_map[t["id"]].id,
                    prerequisite_id=topic_map[dep].id
                ))

    db.commit()

    # Connect main topic to the first topic in the roadmap
    if topic_list:
        db.add(TopicDependency(
            topic_id=topic_map[topic_list[0]["id"]].id,
            prerequisite_id=main_topic_obj.id
        ))
        db.commit()

    db.close()
    print("✅ Roadmap imported. Reloading graph...")
    graph = TopicGraph()
    print("📘 Study Order:", graph.topological_sort())
