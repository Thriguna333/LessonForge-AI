"""Research engine: websites, books and YouTube videos for ANY lesson topic.

Same return format as before, so app.py keeps working:
  {"websites": [...], "books": [...], "youtube": [...]}

Key changes vs the old version:
- Queries are built from the lesson title + learning objective (nothing hardcoded to HTTP).
- YouTube uses ddgs videos() (more reliable) with a YouTube-page fallback, and every video
  is VERIFIED through YouTube's oEmbed endpoint before it is accepted.
- Books come from Google Books (has descriptions), falling back to Open Library.
- Each step is isolated: one failing source never wipes out the others.
"""
import re
import time
from urllib.parse import quote_plus, urlparse

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

HEADERS = {"User-Agent": "Mozilla/5.0 (LessonForge research bot)"}

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "between", "about", "your", "their",
    "explain", "understand", "learn", "describe", "distinguish", "identify", "using", "how", "what",
    "are", "can", "will", "be", "of", "to", "in", "on", "a", "an", "is", "or", "by", "as", "it",
}

# Simple source-reliability hint used by the QC layer / UI.
HIGH_RELIABILITY = (
    "developer.mozilla.org", "rfc-editor.org", "ietf.org", "w3.org", "whatwg.org", "docs.python.org",
    "python.org", "wikipedia.org", "ibm.com", "cloudflare.com", "aws.amazon.com", "learn.microsoft.com",
    "oracle.com", "kernel.org", "git-scm.com", "nist.gov",
)


# ----------------------------------------------------------------- helpers
def extract_keywords(*texts, limit=8):
    """Meaningful words from title/objective, used for relevance filtering."""
    words = re.findall(r"[A-Za-z0-9+#.]{2,}", " ".join(t or "" for t in texts).lower())
    seen, out = set(), []
    for w in words:
        w = w.strip(".")
        if w and w not in STOPWORDS and w not in seen:
            seen.add(w)
            out.append(w)
    return out[:limit]


def reliability(url):
    host = urlparse(url).netloc.lower()
    if host.endswith(".edu") or host.endswith(".gov") or any(host.endswith(d) for d in HIGH_RELIABILITY):
        return "high"
    return "medium"


def _ddgs(method, query, max_results, attempts=2):
    """Call a ddgs method with a retry; return [] instead of raising ('No results found' etc.)."""
    for i in range(attempts):
        try:
            return list(getattr(DDGS(), method)(query, max_results=max_results)) or []
        except Exception as error:
            print(f"ddgs {method} error for '{query}': {error}")
            time.sleep(1.5 * (i + 1))
    return []


# ----------------------------------------------------------------- websites
def search_web(query: str, max_results: int = 6):
    results, seen = [], set()
    for item in _ddgs("text", query, max_results * 2):
        url = item.get("href", "")
        if not url.startswith(("http://", "https://")) or url in seen:
            continue
        if "youtube.com" in url or "youtu.be" in url:
            continue
        seen.add(url)
        snippet = item.get("body", "")
        entry = {
            "title": item.get("title") or "Title unavailable",
            "url": url,
            "snippet": snippet,
            "content": snippet,
            "reachable": False,
            "reliability": reliability(url),
        }
        try:
            r = requests.get(url, timeout=10, headers=HEADERS)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()
            text = soup.get_text(separator=" ", strip=True)[:5000]
            if len(text) > 200:
                entry["content"] = text
            entry["reachable"] = True
        except requests.RequestException:
            pass
        results.append(entry)
        if len(results) >= max_results:
            break
    # reachable and high-reliability sources first
    results.sort(key=lambda x: (not x["reachable"], x["reliability"] != "high"))
    return results


# ----------------------------------------------------------------- books
def _relevant(text, keywords):
    text = text.lower()
    return sum(1 for k in keywords if k in text) >= 1


def search_books(query: str, max_results: int = 4, keywords=None):
    keywords = keywords or extract_keywords(query)
    results = []

    # 1) Google Books (no key needed for light use) - has descriptions
    try:
        r = requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={"q": query, "maxResults": 15, "printType": "books", "langRestrict": "en"},
            timeout=15,
        )
        r.raise_for_status()
        for it in r.json().get("items", []):
            v = it.get("volumeInfo", {})
            title = v.get("title", "")
            desc = v.get("description", "")
            if not title or not _relevant(title + " " + desc, keywords):
                continue
            results.append({
                "title": title + (f": {v['subtitle']}" if v.get("subtitle") else ""),
                "authors": v.get("authors", []),
                "description": desc[:300],
                "url": v.get("infoLink") or it.get("selfLink", ""),
            })
            if len(results) >= max_results:
                return results
    except Exception as error:
        print(f"Google Books error: {error}")

    # 2) Open Library fallback
    try:
        r = requests.get(
            "https://openlibrary.org/search.json",
            params={"q": query, "limit": 20},
            timeout=15,
        )
        r.raise_for_status()
        for item in r.json().get("docs", []):
            title = item.get("title", "")
            subjects = " ".join(item.get("subject", [])[:10])
            if not title or not _relevant(title + " " + subjects, keywords):
                continue
            if any(title.lower() == x["title"].lower() for x in results):
                continue
            results.append({
                "title": title,
                "authors": item.get("author_name", []),
                "description": "",
                "url": "https://openlibrary.org" + item.get("key", ""),
            })
            if len(results) >= max_results:
                break
    except Exception as error:
        print(f"Open Library error: {error}")
    return results


# ----------------------------------------------------------------- YouTube
YT_ID = re.compile(r"(?:youtube\.com/(?:watch\?[^\s\"']*?v=|embed/|shorts/)|youtu\.be/)([A-Za-z0-9_-]{11})")


def verify_youtube(video_id):
    """A video is accepted only if YouTube's oEmbed endpoint confirms it exists."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        r = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": url, "format": "json"},
            headers=HEADERS,
            timeout=10,
        )
        if r.status_code == 200:
            d = r.json()
            return {"title": d.get("title", ""), "url": url, "channel": d.get("author_name", "")}
    except Exception:
        pass
    return None


def _youtube_page_fallback(query, limit=8):
    """Scrape video ids from the YouTube results page if ddgs finds nothing."""
    try:
        r = requests.get(
            f"https://www.youtube.com/results?search_query={quote_plus(query)}",
            headers={**HEADERS, "Accept-Language": "en-US,en;q=0.9"},
            timeout=15,
        )
        ids = list(dict.fromkeys(re.findall(r'"videoId":"([A-Za-z0-9_-]{11})"', r.text)))
        return ids[:limit]
    except Exception as error:
        print(f"YouTube page fallback error: {error}")
        return []


def search_youtube(query: str, max_results: int = 4, queries=None, keywords=None):
    keywords = keywords or extract_keywords(query)
    queries = queries or [f"{query} tutorial", f"{query} explained"]
    candidates = {}  # video_id -> {"duration": ..}

    for q in queries:
        for item in _ddgs("videos", q, 10):
            url = item.get("content") or item.get("href") or item.get("embed_url") or ""
            m = YT_ID.search(url)
            if not m:
                continue
            text = f"{item.get('title', '')} {item.get('description', '')}"
            vid = m.group(1)
            candidates.setdefault(vid, {"duration": item.get("duration", ""), "relevant": _relevant(text, keywords)})
        if len(candidates) >= max_results * 3:
            break

    if not candidates:  # ddgs gave nothing -> try YouTube directly
        for q in queries:
            for vid in _youtube_page_fallback(q):
                candidates.setdefault(vid, {"duration": "", "relevant": True})
            if candidates:
                break

    # relevant first, then verify each one exists
    ordered = sorted(candidates.items(), key=lambda kv: not kv[1]["relevant"])
    videos = []
    for vid, meta in ordered:
        v = verify_youtube(vid)
        if v:
            v["duration"] = meta["duration"]
            videos.append(v)
        if len(videos) >= max_results:
            break
    if not videos:
        print("YouTube research error: no verifiable videos found.")
    return videos


# ----------------------------------------------------------------- entry point
def conduct_research(query: str, objective: str = ""):
    """query = lesson title. Pass the learning objective too for better results."""
    if not query or not query.strip():
        raise ValueError("Research query cannot be empty.")

    keywords = extract_keywords(query, objective)
    focus = " ".join(keywords[:6])  # compact topic string from title + objective

    websites = search_web(f"{query} {focus}".strip()) or search_web(query)
    books = search_books(query, keywords=keywords)
    youtube = search_youtube(
        query,
        queries=[f"{query} tutorial", f"{query} explained", f"{focus} tutorial"],
        keywords=keywords,
    )

    if not websites:
        raise RuntimeError("No web sources could be found (search or network problem). Please retry.")

    return {"websites": websites, "books": books, "youtube": youtube}