import asyncio
import aiohttp
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import whois
import dns.resolver
from urllib.parse import urljoin

app = Flask(__name__)

NEWS_API_KEY = "28f24e8a6a014e7286ff985797f076c2"

# Helper function to fetch metadata
async def fetch_metadata(session, url, category_description=None):
    """
    Fetches metadata (title, description) for a given URL asynchronously.

    :param session: aiohttp client session
    :param url: The URL to fetch
    :param category_description: Fallback description for the category
    :return: Dictionary containing URL, title, and description
    """
    try:
        async with session.get(url, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            title = soup.title.string.strip() if soup.title else "No Title"
            description_tag = soup.find("meta", attrs={"name": "description"})
            description = description_tag["content"].strip() if description_tag else None
            return {"url": url, "title": title, "description": description if description else category_description}
    except Exception as e:
        return {"url": url, "title": "Error", "description": str(e)}

# Asynchronous scraping function
async def scrape_data(query, site=None, search_type=None, title_prefix="Public Information"):
    """
    Scrapes data asynchronously for a given query and source.

    :param query: Search query
    :param site: Optional site filter (e.g., 'reddit.com')
    :param search_type: Type of search (e.g., 'images', 'videos', 'shopping', etc.)
    :param title_prefix: Prefix to add to the title to describe the result type
    :return: List of metadata dictionaries for search results
    """
    base_url = "https://www.google.com"
    search_url = f"{base_url}/search?q="
    if site:
        search_url += f"site:{site}+"
    search_url += query

    if search_type:
        search_url += f"&tbm={search_type}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(search_url, timeout=10) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                links = [urljoin(base_url, a["href"]) for a in soup.find_all("a", href=True)]
                tasks = [
                    fetch_metadata(
                        session,
                        link,
                        category_description=f"This is {title_prefix} about '{query}'."
                    )
                    for link in links[:10]  # Limit to 10 results
                ]
                results = await asyncio.gather(*tasks)
                for result in results:
                    if title_prefix not in result["title"]:
                        result["title"] = f"{title_prefix}: {result['title']}"
                return results
        except Exception as e:
            return [{"url": search_url, "title": "Error", "description": str(e)}]

# Fetch news articles using News API
async def fetch_news_articles(query):
    """
    Fetches news articles for a given query using the News API.

    :param query: Search query
    :return: List of news article dictionaries
    """
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=popularity&apiKey={NEWS_API_KEY}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                data = await response.json()
                if data.get("status") == "ok":
                    articles = data.get("articles", [])
                    return [
                        {
                            "url": article["url"],
                            "title": article["title"],
                            "description": article.get("description"),
                        }
                        for article in articles
                    ]
                else:
                    return [{"url": url, "title": "Error", "description": data.get("message", "Unknown Error")}]
        except Exception as e:
            return [{"url": url, "title": "Error", "description": str(e)}]

# WHOIS and DNS lookup
def get_whois_data(domain):
    try:
        return whois.whois(domain)
    except Exception as e:
        return str(e)

def dns_lookup(domain):
    try:
        answers = dns.resolver.resolve(domain, "A")
        return [str(rdata) for rdata in answers]
    except Exception as e:
        return str(e)

# Flask routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
async def search():
    query = request.form["query"]
    tasks = {
        "google_search": scrape_data(query, search_type="", title_prefix="Google Search"),
        "news": fetch_news_articles(query),
        "reddit": scrape_data(query, site="reddit.com", title_prefix="Reddit Post"),
        "wikipedia": scrape_data(query, site="wikipedia.org", title_prefix="Wikipedia Article"),
        "linkedin": scrape_data(query, site="linkedin.com", title_prefix="LinkedIn Profile"),
    }

    results = await asyncio.gather(*tasks.values())
    data = {key: result for key, result in zip(tasks.keys(), results)}

    # Filter out empty descriptions
    for key, result in data.items():
        for res in result:
            if not res["description"]:
                del res["description"]

    return render_template("result.html", query=query, data=data)

if __name__ == "__main__":
    app.run(debug=True)
