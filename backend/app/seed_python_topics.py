from sqlalchemy.orm import Session
from backend.app.models.init import Topics, TopicDependency
from backend.app.database import SessionLocal

# Predefined Python learning path
topics_data = [
    "Python Basics",
    "Variables and Data Types",
    "Control Flow (if/else, loops)",
    "Functions",
    "Lists and Dictionaries",
    "File I/O",
    "Error Handling (try/except)",
    "Object-Oriented Programming",
    "Modules and Packages",
    "Working with APIs (requests)",
    "Data Structures and Algorithms",
    "Python for Data Analysis (Pandas)",
    "Web Development with Flask"
]

# Define dependencies using index (0-based)
# (dependent_topic_index, prerequisite_topic_index)
dependencies = [
    (1, 0),   # Variables -> Basics
    (2, 1),   # Control Flow -> Variables
    (3, 2),   # Functions -> Control Flow
    (4, 2),   # Lists/Dictionaries -> Control Flow
    (5, 3),   # File I/O -> Functions
    (6, 3),   # Error Handling -> Functions
    (7, 3),   # OOP -> Functions
    (8, 4),   # Modules -> Lists
    (9, 5),   # APIs -> File I/O
    (10, 7),  # DS & Algos -> OOP
    (11, 4),  # Pandas -> Lists
    (12, 8)   # Flask -> Modules
]

def seed_topics_and_dependencies():
    db: Session = SessionLocal()

    topic_objects = []
    for title in topics_data:
        topic = Topics(title=title, content="Placeholder content", source="seed")
        db.add(topic)
        topic_objects.append(topic)

    db.commit()

    # refresh to get IDs
    for topic in topic_objects:
        db.refresh(topic)

        # create dependencies
    for dep_index, prereq_index in dependencies:
        dep = TopicDependency(
            topic_id=topic_objects[dep_index].id,
            prerequisite_id=topic_objects[prereq_index].id
        )
        db.add(dep)

    db.commit()
    db.close()
    print("✅ Topics and dependencies seeded successfully.")

if __name__ == "__main__":
    seed_topics_and_dependencies()