"""
Profile Optimizer — bio rewrites, photo advice, platform-specific tips.
"""

import anthropic

client = anthropic.Anthropic()

PLATFORM_GUIDES = {
    "grindr": "Short, punchy, often omits full sentences. Stats/position often listed. Can be blunt.",
    "scruff": "More detailed acceptable. Bears/masculine-coded culture. Tribe tags matter.",
    "hinge": "Prompt-based. Story-driven. Showing personality > listing traits. Dating-oriented.",
    "tinder": "Brief bio + photos do the heavy lifting. 1-3 sentences max.",
    "feeld": "Kink-friendly, ENM-friendly. More explicit allowed. Orientation + relationship style important.",
    "other": "General dating app conventions apply.",
}

PROFILE_OPTIMIZER_TOOLS = [
    {
        "name": "optimize_profile",
        "description": (
            "Review and rewrite a dating app bio. Gives specific rewrites, not generic feedback. "
            "Platform-aware — a Grindr bio is very different from a Hinge prompt."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "current_bio": {
                    "type": "string",
                    "description": "The current bio text (or 'none' if starting fresh)",
                },
                "platform": {
                    "type": "string",
                    "enum": ["grindr", "scruff", "hinge", "tinder", "feeld", "other"],
                },
                "goal": {
                    "type": "string",
                    "enum": ["hookups", "dating", "both", "friends"],
                    "description": "What the user is looking for",
                },
                "about_user": {
                    "type": "string",
                    "description": "Key facts about the user to incorporate (age, interests, personality, etc.)",
                },
                "what_to_avoid": {
                    "type": "string",
                    "description": "Optional: things they don't want in the bio or types they want to filter out",
                },
            },
            "required": ["platform", "goal", "about_user"],
        },
    },
    {
        "name": "review_photos",
        "description": (
            "Give honest feedback on photo selection and ordering for a dating profile. "
            "Covers which photos to use first, what order works, and what to cut."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "photos_description": {
                    "type": "string",
                    "description": "Description of each photo: what it shows, setting, expression, quality, clothing",
                },
                "platform": {
                    "type": "string",
                    "enum": ["grindr", "scruff", "hinge", "tinder", "feeld", "other"],
                },
                "goal": {
                    "type": "string",
                    "enum": ["hookups", "dating", "both"],
                },
            },
            "required": ["photos_description", "platform"],
        },
    },
    {
        "name": "platform_tips",
        "description": (
            "Get platform-specific strategy tips — what works on this app, "
            "what to avoid, how to stand out, unwritten rules."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["grindr", "scruff", "hinge", "tinder", "feeld", "other"],
                },
                "specific_question": {
                    "type": "string",
                    "description": "Optional: specific aspect they want tips on",
                },
            },
            "required": ["platform"],
        },
    },
]


def handle_profile_optimizer(tool_name: str, tool_input: dict) -> str:
    """Route profile optimizer tool calls."""

    prompts = {
        "optimize_profile": _optimize_prompt,
        "review_photos": _photos_prompt,
        "platform_tips": _tips_prompt,
    }

    prompt_fn = prompts.get(tool_name)
    if not prompt_fn:
        return f"Unknown tool: {tool_name}"

    prompt = prompt_fn(tool_input)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
        system=(
            "You are a gay dating profile expert who has seen thousands of profiles. "
            "You give direct, specific feedback that actually improves results. "
            "You understand the culture and unwritten rules of each platform. "
            "No generic advice. No 'just be yourself' platitudes. Specific, actionable rewrites."
        ),
    )
    return response.content[0].text


def _optimize_prompt(inp: dict) -> str:
    platform = inp["platform"]
    goal = inp["goal"]
    about = inp["about_user"]
    current = inp.get("current_bio", "none")
    avoid = inp.get("what_to_avoid", "")
    platform_context = PLATFORM_GUIDES.get(platform, PLATFORM_GUIDES["other"])

    return f"""Optimize this {platform} profile bio.

Platform context: {platform_context}
Goal: {goal}
About the user: {about}
{f'Current bio: {current}' if current and current != 'none' else 'No current bio — write fresh.'}
{f'Things to filter/avoid: {avoid}' if avoid else ''}

Give:
1. **What's wrong** with the current bio (if any) — be direct
2. **Rewritten bio** — ready to copy-paste
3. **Why it works** — specific reasoning, not generic praise
4. **Optional add-ons** — stats/info to include separately if the platform supports it

The rewrite must match {platform} conventions. For Grindr: short and punchy.
For Hinge: conversational and story-driven. For Scruff: can be more detailed.
Don't make it sound like a resume or a list of adjectives."""


def _photos_prompt(inp: dict) -> str:
    photos = inp["photos_description"]
    platform = inp.get("platform", "the app")
    goal = inp.get("goal", "both")

    return f"""Give honest photo advice for a {platform} profile. Goal: {goal}.

Photos described:
{photos}

Tell me:
1. **Lead photo** — which should be first and why
2. **Cut these** — any photos to remove and why (be direct)
3. **Order** — recommended sequence
4. **What's missing** — types of photos that would strengthen the profile
5. **Specific notes** — anything about individual photos (lighting, crop, vibe)

Rules: Face in lead photo unless it's Grindr/explicit profile. Body pics okay but where they land in the sequence matters.
For dating-oriented apps, lifestyle and personality photos carry more weight than just body shots."""


def _tips_prompt(inp: dict) -> str:
    platform = inp["platform"]
    specific = inp.get("specific_question", "")
    platform_context = PLATFORM_GUIDES.get(platform, PLATFORM_GUIDES["other"])

    return f"""Give the real insider guide to {platform} for a gay man.

Platform culture: {platform_context}
{f'Specific question: {specific}' if specific else ''}

Cover:
1. **What actually gets responses** on this platform
2. **The unwritten rules** most people don't know
3. **Common mistakes** that hurt your results
4. **How to stand out** from the typical profile
5. **Settings/features** worth using

Be specific to {platform}'s culture and demographics. Not generic dating advice."""
