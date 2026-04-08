import json
import time
from google import genai


def find_matches(signals, members, api_key):
    client = genai.Client(api_key=api_key)

    member_map = {m["id"]: m for m in members}
    matches = []
    seen_seekers = set()

    for signal in signals:
        seeker_id = signal["author_id"]
        if seeker_id in seen_seekers:
            continue

        seeker = member_map.get(seeker_id, {})
        other_members = [m for m in members if m["id"] != seeker_id]

        members_desc = "\n".join(
            f"- {m['name']} (id: {m['id']}), {m['role']} at {m['company']}. "
            f"Expertise: {', '.join(m['expertise'])}. Goals: {', '.join(m['goals'])}. Bio: {m['bio']}"
            for m in other_members
        )

        prompt = f"""You are a community matchmaker for GrowthX, a professional community of growth and product leaders.

Member A: {seeker['name']} ({seeker['role']} at {seeker['company']})
- Is seeking: {signal['seeking']}
- Is offering: {signal['offering']}

Here are the other community members:
{members_desc}

Who is the SINGLE best person to connect Member A with, and why? Consider whose expertise directly addresses what Member A is seeking, and where there's potential for a two-way value exchange.

Return ONLY valid JSON, no markdown, no explanation:
{{"seeker_id": "{seeker_id}", "match_id": "...", "reason": "..."}}"""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                text = response.text.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                    text = text.rsplit("```", 1)[0].strip()
                match = json.loads(text)
                matches.append(match)
                seen_seekers.add(seeker_id)
                break
            except Exception as e:
                if "503" in str(e) and attempt < max_retries - 1:
                    wait = (attempt + 1) * 10
                    print(f"  [retry] Match for {seeker_id} hit 503 (server overloaded). Retrying in {wait}s... (attempt {attempt + 2}/{max_retries})")
                    time.sleep(wait)
                else:
                    print(f"  [error] Failed to match for {seeker_id}: {e}")

        time.sleep(2)

    return matches
