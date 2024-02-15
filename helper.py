from langchain_community.document_loaders import PyPDFLoader
import os


def split_and_format_data(path):
    title = os.path.basename(path).split(".")[0]  # Extracting the filename without extension as the title
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    documents =[]
    for page in pages:
        format={
            "meta": {"title":title},
            "content": page.page_content
        }
        documents.append(format)

    return documents
