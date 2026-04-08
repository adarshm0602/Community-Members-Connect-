# GrowthX Member Connect Agent

A multi-agent CLI tool that automatically identifies high-value connection opportunities between GrowthX community members and drafts personalized intro DMs. It scans community feed posts, detects signals (what members are seeking and offering), matches them with the best-fit member who can help, and writes warm, community-first introductions — all powered by Google Gemini.

## Architecture

The system uses a 3-agent pipeline:

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   WATCHER   │ ───> │   MATCHER   │ ───> │  OUTREACH   │
│             │      │             │      │             │
│ Scans feed  │      │ Finds best  │      │ Drafts warm │
│ posts and   │      │ member-to-  │      │ intro DMs   │
│ extracts    │      │ member      │      │ with context │
│ signals     │      │ connections │      │ and reason   │
└─────────────┘      └─────────────┘      └─────────────┘
   feed.json            signals              matches
   members.json         + members            + members
```

- **Watcher Agent** — Reads community feed posts, uses Gemini to extract what each member is *seeking* and *offering*
- **Matcher Agent** — Takes signals and finds the single best connection for each member based on expertise and goals
- **Outreach Agent** — Drafts a 3-sentence intro DM in GrowthX's community-first voice

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key to .env
# (already created — just verify the key is correct)
echo "GEMINI_API_KEY=your_key_here" > .env

# Run the agent
python main.py
```

## Sample Output

```
--- GrowthX Member Connect Agent ---

[watcher] Scanning community feed for signals...

  [signal found] @Priya Iyer: seeking "how to improve D2C retention beyond 18% repeat rate" | offering "D2C brand building experience, shipping 10K boxes/month"
  [signal found] @Arjun Kapoor: seeking "PLG conversion strategy for free-to-paid" | offering "auth infrastructure learnings and developer tool expertise"
  [signal found] @Ananya Sharma: seeking "community engagement and sharing insights" | offering "gamification and reward mechanics expertise from CRED"
  [signal found] @Sneha Reddy: seeking "advice on transitioning from corporate PM to founder" | offering "4 years of experimentation and logistics-tech expertise at Swiggy"
  [signal found] @Rohit Mehra: seeking "understanding B2B SaaS growth frameworks" | offering "consumer retention and quick commerce growth expertise"

  Found 10 signals from 7 members.

[matcher] Finding best connections...

  [match found] @Priya Iyer ↔ @Rohit Mehra — Rohit scaled retention at Zepto by 3x, directly relevant to Priya's D2C retention challenge
  [match found] @Arjun Kapoor ↔ @Karthik Nair — Karthik runs PLG and pricing experiments at Freshworks, exactly what Arjun needs for free-to-paid conversion
  [match found] @Sneha Reddy ↔ @Arjun Kapoor — Arjun recently made the corporate-to-founder leap with StackAuth, can advise Sneha on the transition
  [match found] @Rohit Mehra ↔ @Vikram Desai — Vikram leads B2B SaaS marketing at Razorpay, perfect for Rohit's B2B curiosity

  Generated 7 unique matches.

[outreach] Drafting intro DMs...

  [DM drafted] To @Rohit Mehra (intro with @Priya Iyer):
  "Hey Rohit — Priya from NutriBox is stuck at 18% repeat rate and your 3x retention work at Zepto is exactly the playbook she needs. She's got deep D2C brand-building chops that could be interesting for your consumer insights too. Would you be up for a quick chat with her this week?"

  [DM drafted] To @Karthik Nair (intro with @Arjun Kapoor):
  "Hey Karthik — Arjun is building StackAuth (YC W24) and has 50 devs on free tier but zero paid conversions. Your pricing experiments at Freshworks across 6 geos could be a game-changer for him, and his dev-tools PLG learnings might give you fresh angles too. Think a 20-min call would be worth it?"

--- Done! ---
```

## Why This Matters for GrowthX

The hardest part of any professional community isn't getting members — it's making sure they find each other at the right time. Most valuable connections never happen because people don't know who else is in the room. This agent turns passive feed activity into active, high-context introductions — making the community feel smaller, warmer, and more useful. It's the difference between "a Slack group I'm in" and "the community that changed my career."
