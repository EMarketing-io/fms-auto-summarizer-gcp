import requests
from bs4 import BeautifulSoup


# 🌐 Extracts clean, readable text content from a web page (URL)
def extract_text_from_url(url):
    # 🔗 Send an HTTP GET request to the target URL
    response = requests.get(url)

    # 🧽 Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # 🚫 Remove unwanted script and style elements to avoid clutter
    for script in soup(["script", "style"]):
        script.decompose()

    # 📃 Extract visible text from the page with newlines separating blocks
    text = soup.get_text(separator="\n")

    # 🧹 Strip whitespace from each line and remove empty lines
    lines = [line.strip() for line in text.splitlines()]
    cleaned_text = "\n".join(line for line in lines if line)

    # 🧾 Return the fully cleaned body text
    return cleaned_text
