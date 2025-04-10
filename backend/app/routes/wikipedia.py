import requests 
from fastapi import APIRouter, Query, HTTPException


router = APIRouter()

@router.get("/api/fetch-topic")
def fetch_wikipedia_summary(query: str = Query(..., min_length=3)):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"

    response = requests.get(url)


    if response.status_code == 200:
        data = response.json()
        return{
         
         "title": data.get("title"),
         "summary": data.get("extract"),
         "sorce_url": data.get("content_urls", {}).get("desktop", {}).get("page")}

    elif response.status.code == 404:
        raise HTTPException(status_code=404, detail="Topic not found on Wikipedia.")
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch Wikipedia data")


        
        