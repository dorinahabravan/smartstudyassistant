import requests
import re
from sqlalchemy.orm import Session
from keybert import KeyBERT
from backend.app.models.init import Topics, TopicDependency
from backend.app.database import SessionLocal
from backend.app.topic_graph import TopicGraph



# 🔍 Extract subtopics from summary using basic keyword extraction
 
 
kw_model = KeyBERT()

def extract_subtopics_from_summary(summary: str) -> list:
    keywords = kw_model.extract_keywords(
        summary,
        keyphrase_ngram_range=(1, 3),
        stop_words='english',
        top_n=6
    )
    return [kw[0] for kw in keywords]
def fetch_wikipedia_summary(topic: str) -> str:
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "format": "json",
        "titles": topic
    }

    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        pages = response.json().get("query", {}).get("pages", {})
        if pages:
            page = next(iter(pages.values()))
            return page.get("extract", "No content found.")
    return "No summary available."


def resolve_wikipedia_title(user_input: str) -> str:
    search_url = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=true&format=json&titles"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": user_input,
        "format": "json"
    }

    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        results = response.json()["query"]["search"]
        if results:
            return results[0]["title"]  # 🧠 Best match Wikipedia article title
    return user_input  # fallback to original if nothing found
   

def fetch_and_add_topic(main_topic: str):
    db: Session = SessionLocal()

    # Check if topic already exists
    existing = db.query(Topics).filter(Topics.title.ilike(main_topic)).first()
    if existing:
        print(f"✅ '{main_topic}' already exists in the database.")
        db.close()
        return

    print(f"🔍 '{main_topic}' not found. Fetching from Wikipedia...")
    wiki_title = resolve_wikipedia_title(main_topic)
    main_summary = fetch_wikipedia_summary(wiki_title)

    # Insert main topic
    main_topic_entry = Topics(title=main_topic, content=main_summary, source="Wikipedia")
    db.add(main_topic_entry)
    db.commit()
    db.refresh(main_topic_entry)

    # Dynamically extract subtopics from the summary
    subtopics = extract_subtopics_from_summary(main_summary)
    print("🔍 Extracted subtopics:", subtopics)

    topic_objects = [main_topic_entry]

    for sub in subtopics:
        content = fetch_wikipedia_summary(sub)
        t = Topics(title=sub, content=content, source="Wikipedia")
        db.add(t)
        topic_objects.append(t)

    db.commit()

    for t in topic_objects:
        db.refresh(t)

    # Create simple linear dependencies for now
    for i in range(1, len(topic_objects)):
        db.add(TopicDependency(
            topic_id=topic_objects[i].id, 
            prerequisite_id=topic_objects[i - 1].id
        ))

    db.commit()
    db.close()

    print("✅ Topic and dynamic subtopics added. Reloading graph...")
    graph = TopicGraph()
    # ✅ Build study path only for the new topic and its subtopics
    new_topic_titles = [main_topic] + subtopics

    filtered_study_order = [
    title for title in graph.topological_sort()
    if title in new_topic_titles
    ]

    print("📘 Study Order (new topics only):", filtered_study_order)

if __name__ == "__main__":
     topic = input("🔎 Enter a topic you'd like to learn: ")
     fetch_and_add_topic(topic)