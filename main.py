import os
import json
from dotenv import load_dotenv
from agents.watcher import load_data, extract_signals
from agents.matcher import find_matches
from agents.outreach import draft_dms


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[error] GEMINI_API_KEY not found in .env file.")
        return

    print("\n--- GrowthX Member Connect Agent ---\n")

    # Load data
    feed, members = load_data()
    member_map = {m["id"]: m for m in members}

    # Step 1: Watcher Agent
    print("[watcher] Scanning community feed for signals...\n")
    signals = extract_signals(feed, members, api_key)

    for s in signals:
        author = member_map.get(s["author_id"], {})
        print(f'  [signal found] @{author.get("name", "Unknown")}: '
              f'seeking "{s["seeking"]}" | offering "{s["offering"]}"')

    print(f"\n  Found {len(signals)} signals from {len(set(s['author_id'] for s in signals))} members.\n")

    # Step 2: Matcher Agent
    print("[matcher] Finding best connections...\n")
    matches = find_matches(signals, members, api_key)

    for m in matches:
        seeker = member_map.get(m["seeker_id"], {})
        match = member_map.get(m["match_id"], {})
        print(f'  [match found] @{seeker.get("name", "?")} \u2194 @{match.get("name", "?")} \u2014 {m["reason"]}')

    print(f"\n  Generated {len(matches)} unique matches.\n")

    # Step 3: Outreach Agent
    print("[outreach] Drafting intro DMs...\n")
    dms = draft_dms(matches, members, api_key)

    for dm in dms:
        print(f'  [DM drafted] To @{dm["to"]} (intro with @{dm["seeker"]}):')
        print(f'  "{dm["dm"]}"\n')

    print("--- Done! ---\n")


if __name__ == "__main__":
    main()
