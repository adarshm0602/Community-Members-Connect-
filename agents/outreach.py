import json
import time
from google import genai


def draft_dms(matches, members, api_key):
    client = genai.Client(api_key=api_key)

    member_map = {m["id"]: m for m in members}
    dms = []

    for match in matches:
        seeker = member_map.get(match.get("seeker_id"), {})
        target = member_map.get(match.get("match_id"), {})
        if not seeker.get("name") or not target.get("name"):
            print(f"  [skip] Skipping match with missing member data (seeker={match.get('seeker_id')}, match={match.get('match_id')})")
            continue
        reason = match.get("reason", "")

        prompt = f"""You are writing a warm intro DM on behalf of GrowthX, a curated community of growth and product leaders in India.

The DM is being sent to {target['name']} ({target['role']} at {target['company']}).
You're introducing them to {seeker['name']} ({seeker['role']} at {seeker['company']}).

Reason for the connection: {reason}

Write a 3-sentence DM that:
1. Opens with a specific, genuine reason why this intro makes sense
2. Mentions what both people bring to the table (two-way value)
3. Ends with a soft ask to connect

Tone: community-first, warm, not salesy. Write like a helpful friend, not a LinkedIn bot.

Return ONLY valid JSON, no markdown, no explanation:
{{"to": "{target['name']}", "dm": "..."}}"""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                text = response.text.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                    text = text.rsplit("```", 1)[0].strip()
                dm = json.loads(text)
                dm["seeker"] = seeker["name"]
                dms.append(dm)
                break
            except Exception as e:
                if "503" in str(e) and attempt < max_retries - 1:
                    wait = (attempt + 1) * 10
                    print(f"  [retry] DM for {match.get('match_id')} hit 503 (server overloaded). Retrying in {wait}s... (attempt {attempt + 2}/{max_retries})")
                    time.sleep(wait)
                else:
                    print(f"  [error] Failed to draft DM for {match.get('match_id')}: {e}")

        time.sleep(2)

    return dms
