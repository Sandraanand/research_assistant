"""
Simple PubMed Search Utility
"""
import requests
from typing import List, Dict
from config import config


def search_pubmed(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search PubMed for papers
    
    Args:
        query: Search query
        max_results: Maximum number of results
        
    Returns:
        List of paper dictionaries
    """
    try:
        # Search for IDs
        search_url = f"{config.PUBMED_BASE_URL}esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "email": config.PUBMED_EMAIL
        }
        
        response = requests.get(search_url, params=search_params)
        response.raise_for_status()
        search_data = response.json()
        
        ids = search_data.get("esearchresult", {}).get("idlist", [])
        
        if not ids:
            return []
        
        # Fetch details
        fetch_url = f"{config.PUBMED_BASE_URL}esummary.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "json",
            "email": config.PUBMED_EMAIL
        }
        
        response = requests.get(fetch_url, params=fetch_params)
        response.raise_for_status()
        fetch_data = response.json()
        
        papers = []
        for paper_id in ids:
            try:
                paper_data = fetch_data["result"][paper_id]
                
                # Extract authors
                authors = []
                for author in paper_data.get("authors", [])[:3]:  # First 3 authors
                    if "name" in author:
                        authors.append(author["name"])
                
                paper = {
                    "pmid": paper_id,
                    "title": paper_data.get("title", ""),
                    "authors": authors,
                    "journal": paper_data.get("fulljournalname", ""),
                    "pubdate": paper_data.get("pubdate", ""),
                    "link": f"https://pubmed.ncbi.nlm.nih.gov/{paper_id}/",
                    "doi": paper_data.get("elocationid", "").replace("doi: ", "")
                }
                papers.append(paper)
            except Exception as e:
                print(f"Error processing paper {paper_id}: {e}")
                continue
        
        return papers
    
    except Exception as e:
        print(f"PubMed search error: {e}")
        return []


# Add to config if not present
if not hasattr(config, 'PUBMED_BASE_URL'):
    config.PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
