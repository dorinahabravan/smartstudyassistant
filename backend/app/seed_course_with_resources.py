import json
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.init import Topics, TopicDependency
from backend.app.utils.google_search import fetch_resources_google

COURSES = {
    "Python Developer": [
        "Python Basics",
        "Variables and Data Types",
        
        "Control Flow (if/else, loops)",
        "Functions",
        "Modules and Packages",
        "Object-Oriented Programming",
        "Working with APIs (requests)"
    ],
    "Java Developer": [
        "Java Basics",
        "OOP in Java",
        "Exception Handling",
        "Java Collections",
        "Multithreading",
        "JDBC and File I/O",
        "Spring Boot Basics"
    ],
    "Backend Developer": [
        "Server, HTTP, REST APIs",
        "Node.js or Java Backend",
        "Express or Spring Boot",
        "Databases (SQL & NoSQL)",
        "Authentication & Authorization",
        "API Security",
        "Unit Testing"
    ],
    "React Developer": [
        "JSX and Components",
        "React State and Props",
        "useEffect and Lifecycle",
        "Routing with React Router",
        "Hooks and Custom Hooks",
        "Context API and Redux",
        "React Query or SWR"
    ],
    "AI Engineer": [
        "Math for AI (Linear Algebra, Probability)",
        "Python for AI",
        "Supervised Learning",
        "Unsupervised Learning",
        "Neural Networks",
        "Model Evaluation",
        "Deep Learning"
    ],
    "Frontend Developer": [
        "HTML & CSS",
        "JavaScript Basics",
        "DOM Manipulation",
        "ES6+ Features",
        "React Basics",
        "React State Management",
        "React Router"
    ],
    "Cyber Security Specialist": [
        "Basics of Networking",
        "Operating Systems Security",
        "Cryptography Fundamentals",
        "Web Security (XSS, CSRF)",
        "Penetration Testing",
        "Vulnerability Scanning",
        "SIEM & Threat Monitoring"
    ]
}

def reset_and_seed_courses():
    db: Session = SessionLocal()

    db.query(TopicDependency).delete()
    db.query(Topics).delete()
    db.commit()
    print("🧹 Cleared topics and dependencies.")

    for course, subtopics in COURSES.items():
        print(f"\n📚 Seeding course: {course}")

        
        course_topic = Topics(title=course, content=f"{course} learning path", source="manual")
        db.add(course_topic)
        db.commit()
        db.refresh(course_topic)

        prev_topic_id = course_topic.id

        for title in subtopics:
            topic = Topics(title=title, content=f"{title} content", source="manual")
            db.add(topic)
            db.commit()
            db.refresh(topic)

            dependency = TopicDependency(topic_id=topic.id, prerequisite_id=prev_topic_id)
            db.add(dependency)
            prev_topic_id = topic.id

            resources = fetch_resources_google(title)
            if resources:
                topic.resources = json.dumps(resources)
                db.commit()
                print(f"✅ Subtopic: {title} + resources")
            else:
                print(f"⚠️ Subtopic: {title} (no resources)")

    db.close()
    print("\n🎉 All courses seeded and resources fetched.")


if __name__ == "__main__":
    reset_and_seed_courses()
