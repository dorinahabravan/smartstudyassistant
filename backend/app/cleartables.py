from backend.app.database import SessionLocal
from backend.app.models.init import Topics, TopicDependency

db = SessionLocal()
db.query(TopicDependency).delete()
db.query(Topics).delete()
db.commit()
db.close()
print("✅ Topics and dependencies cleared.")
