import json
import time
from google import genai


def load_data():
    with open("data/feed.json", "r") as f:
        feed = json.load(f)
    with open("data/members.json", "r") as f:
        members = json.load(f)
    return feed, members


def extract_signals(feed, members, api_key):
    client = genai.Client(api_key=api_key)

    member_map = {m["id"]: m for m in members}
    signals = []

    for post in feed:
        author = member_map.get(post["author_id"], {})
        prompt = f"""You are analyzing a community feed post from a professional network.

Post by {author.get('name', 'Unknown')} ({author.get('role', '')} at {author.get('company', '')}):
\"{post['content']}\"

Extract what this member is "seeking" (a challenge, question, need, or ask) and what they are "offering" (expertise, experience, a win, or insight they're sharing).

Return ONLY valid JSON, no markdown, no explanation:
{{"author_id": "{post['author_id']}", "seeking": "...", "offering": "..."}}"""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                text = response.text.strip()
                # Clean markdown code fences if present
                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                    text = text.rsplit("```", 1)[0].strip()
                signal = json.loads(text)
                signal["post_id"] = post["post_id"]
                signals.append(signal)
                break
            except Exception as e:
                if "503" in str(e) and attempt < max_retries - 1:
                    wait = (attempt + 1) * 10
                    print(f"  [retry] Post {post['post_id']} hit 503 (server overloaded). Retrying in {wait}s... (attempt {attempt + 2}/{max_retries})")
                    time.sleep(wait)
                else:
                    print(f"  [error] Failed to process post {post['post_id']}: {e}")

        time.sleep(2)

    return signals
