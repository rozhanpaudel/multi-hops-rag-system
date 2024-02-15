import requests
from bs4 import BeautifulSoup
import re
import urllib
import os


# PubMed URL for the "microbe" topic
pubmed_url = "https://pubmed.ncbi.nlm.nih.gov/"
query = "microbe"
num_papers_to_fetch = 1 


def fetch_papers(query, num_papers):
    papers = []
    page = 1

    while len(papers) < num_papers:
        search_url = f"{pubmed_url}?term={query}&page={page}"
        response = requests.get(search_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paper_links = soup.find_all("a", {"class": "docsum-title"})

            for link in paper_links:
                title = link.text.strip()
                paper_url = f"{pubmed_url}{link['href']}"
                content = fetch_paper_content(paper_url)
                if content:
                    papers.append({"title": title, "content": content})

                if len(papers) == num_papers:
                    break

            page += 1
        else:
            print(f"Failed to fetch papers. Status code: {response.status_code}")
            break

    return papers


def fetch_paper_content(paper_url):
    response = requests.get(paper_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        full_view_identifiers = soup.find("ul", {"id": "full-view-identifiers"})
        doi = soup.find("span", {"class": "identifier doi"})
        id_link = soup.find("a", {"class": "id-link"})

        content = {
            "full_view_identifiers": full_view_identifiers.text.strip() if full_view_identifiers else None,
            "doi": doi.text.strip() if doi else None,
            "id_link": id_link.text.strip() if id_link else None
        }

        if content["doi"]:
            baseUrl = "https://onlinelibrary.wiley.com/doi/epdf/"
            
            content_url = baseUrl + extract_doi(content["doi"])
            download_url = convert_url_format(original_url=content_url)
              

    print(f"Failed to fetch paper content. Status code: {response.status_code}")
    return None

def convert_url_format(original_url):
    if "https://onlinelibrary.wiley.com/doi/epdf/" not in original_url:
        raise ValueError("Invalid URL format. Please provide a valid Wiley ePDF URL.")
    
    doi = original_url.split("/")
    print(doi)
    prefix = doi[5]
    doi = doi[6]

    new_url = f"https://onlinelibrary.wiley.com/doi/pdfdirect/{prefix}/{doi}?download=true"
    return new_url

def extract_doi(input_string):
    doi_pattern = re.compile(r'\b10\.\d+/\S+\b')
    match = doi_pattern.search(input_string)
    
    if match:
        return match.group()
    else:
        return None
    
# Fetch papers
papers_to_fetch = fetch_papers(query, num_papers_to_fetch)

