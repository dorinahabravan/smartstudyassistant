from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.init import Topics, TopicDependency

# Dictionary of slugs → list of topics in order
ALL_ROADMAPS = {
    "Python Developer": [
        "Python Basics",
        "Variables and Data Types",
        "Control Flow (if/else, loops)",
        "Functions",
        "Lists and Dictionaries",
        "File I/O",
        "Error Handling (try/except)",
        "Object-Oriented Programming",
        "Modules and Packages",
        "Python for Data Analysis (Pandas)",
        "Working with APIs (requests)",
        "Data Structures and Algorithms",
        "Web Development with Flask"
    ],
    "Java Developer": [
        "Java Basics",
        "OOP in Java",
        "Exception Handling",
        "Java Collections",
        "Multithreading",
        "JDBC and File I/O",
        "Spring Boot Basics",
        "Building REST APIs"
    ],
    "Frontend Developer": [
        "HTML & CSS",
        "JavaScript Basics",
        "DOM Manipulation",
        "ES6+ Features",
        "React Basics",
        "React State Management",
        "React Router",
        "Next.js Basics"
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
    "AI Engineer": [
        "Math for AI (Linear Algebra, Probability)",
        "Python for AI",
        "Supervised Learning",
        "Unsupervised Learning",
        "Neural Networks",
        "Model Evaluation",
        "Deep Learning",
        "NLP Basics"
    ],
    "Cyber Security Specialist": [
        "Basics of Networking",
        "Operating Systems Security",
        "Cryptography Fundamentals",
        "Web Security (XSS, CSRF)",
        "Penetration Testing",
        "Vulnerability Scanning",
        "SIEM & Threat Monitoring"
    ],
    "React Developer": [
        "JSX and Components",
        "React State and Props",
        "useEffect and Lifecycle",
        "Routing with React Router",
        "Hooks and Custom Hooks",
        "Context API and Redux",
        "React Query or SWR"
    ]
}

def seed_all_roadmaps():
    db: Session = SessionLocal()

    for path_name, topics in ALL_ROADMAPS.items():
        print(f"🌱 Seeding roadmap: {path_name}")
        root = Topics(title=path_name, content="", source="manual")
        db.add(root)
        db.commit()
        db.refresh(root)

        previous = root
        for t_title in topics:
            topic = Topics(title=t_title, content="", source="manual")
            db.add(topic)
            db.commit()
            db.refresh(topic)

            dep = TopicDependency(topic_id=topic.id, prerequisite_id=previous.id)
            db.add(dep)
            previous = topic

        db.commit()
        print(f"✅ {path_name} added!")

    db.close()
    print("\n🎓 All roadmaps seeded.")

if __name__ == "__main__":
    seed_all_roadmaps()
