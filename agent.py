import os
from pathlib import Path
from typing import List, Dict

import requests
import feedparser
from bs4 import BeautifulSoup
from twilio.rest import Client
from transformers import pipeline

SEEN_FILE = Path("seen_urls.txt")

# Example RSS feeds from IT strategy consulting firms or related sources
SOURCES: List[Dict[str, str]] = [
    {
        "name": "Accenture Blog",
        "rss": "https://www.accenture.com/us-en/blogs/blogs-index-rss"
    },
    {
        "name": "McKinsey Insights",
        "rss": "https://www.mckinsey.com/insights/rss"
    },
    {
        "name": "BCG Publications",
        "rss": "https://www.bcg.com/feeds/publications"
    },
]


def load_seen() -> set:
    if SEEN_FILE.exists():
        return set(SEEN_FILE.read_text().splitlines())
    return set()


def save_seen(seen: set) -> None:
    SEEN_FILE.write_text("\n".join(sorted(seen)))


def fetch_article_content(url: str) -> str:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # Get text from paragraphs
    paragraphs = [p.get_text(separator=" ", strip=True) for p in soup.find_all("p")]
    return "\n".join(paragraphs)


def summarize(text: str) -> str:
    summarizer = pipeline("summarization")
    # Hugging Face models typically limit input length; truncate long text
    max_len = 1000
    if len(text) > max_len:
        text = text[:max_len]
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]["summary_text"]


def send_whatsapp_message(body: str) -> None:
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    whatsapp_from = os.environ["TWILIO_WHATSAPP_FROM"]
    whatsapp_to = os.environ["WHATSAPP_TO"]

    client = Client(account_sid, auth_token)
    client.messages.create(from_=whatsapp_from, body=body, to=whatsapp_to)


def process_sources() -> None:
    seen = load_seen()
    new_seen = set(seen)

    for source in SOURCES:
        feed = feedparser.parse(source["rss"])
        for entry in feed.entries:
            url = entry.link
            if url in seen:
                continue
            try:
                content = fetch_article_content(url)
                summary = summarize(content)
                message = f"{source['name']}\n{entry.title}\n{summary}\n{url}"
                send_whatsapp_message(message)
                new_seen.add(url)
            except Exception as exc:
                print(f"Failed to process {url}: {exc}")

    save_seen(new_seen)


def main() -> None:
    process_sources()


if __name__ == "__main__":
    main()
