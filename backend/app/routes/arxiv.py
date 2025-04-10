import requests
import xml.etree.ElementTree as ET 
from fastapi import APIRouter, Query, HTTPException

router = APIRouter()

@router.get("/api/fetch-papers")
def fetch_arxiv_papers(query: str = Query(..., min_length=2)):
    print("🔍 Fetching papers for:", query)

    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": 5
    }

    response = requests.get(base_url, params=params)

    print("📄 Response content:")
    print(response.text[:1000])  # Show preview of raw XML

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch from arXiv")

    try:
        root = ET.fromstring(response.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        papers = []

        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip()
            summary = entry.find("atom:summary", ns).text.strip()
            authors = [author.find("atom:name", ns).text for author in entry.findall("atom:author", ns)]
            link = entry.find("atom:id", ns).text.strip()

            papers.append({
                "title": title,
                "summary": summary,
                "authors": authors,
                "link": link
            })

        print("✅ Parsed papers:", len(papers))
        return {
            "query": query,
            "results": papers
        }

    except ET.ParseError:
        raise HTTPException(status_code=500, detail="Error parsing XML from arXiv")
