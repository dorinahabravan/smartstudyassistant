from fastapi import APIRouter, HTTPException, Query
from backend.app.utils.slug_matcher import match_goal_to_slug
from backend.app.roadmap_loader import fetch_and_add_from_github_roadmap
from backend.app.topic_graph import TopicGraph

router = APIRouter()

@router.get("/api/learn")
def learn_path(goal: str = Query(..., min_length=2)):
    slug = match_goal_to_slug(goal)
    if not slug:
        raise HTTPException(status_code=404, detail="Roadmap not supported")

    title = goal.title()
    url = f"https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/career-paths/{slug}.json"
    
    try:
        fetch_and_add_from_github_roadmap(slug=str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading roadmap: {str(e)}")

    # Reload graph
    graph = TopicGraph()
    full_path = graph.topological_sort()
    
    # Return only the relevant section
    study_path = [t for t in full_path if goal.lower() in t.lower() or title.lower() in t.lower()]
    
    return {
        "goal": goal,
        "study_path": study_path
    }
