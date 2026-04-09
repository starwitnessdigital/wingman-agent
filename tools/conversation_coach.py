"""
Conversation Coach — openers, response suggestions, escalation, recovery.
"""

import anthropic

client = anthropic.Anthropic()

CONVERSATION_COACH_TOOLS = [
    {
        "name": "generate_opener",
        "description": (
            "Generate effective opening messages for a specific profile or situation. "
            "Produces 3 openers at different tones (playful, direct, conversational). "
            "Never outputs generic 'hey' messages."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "profile_details": {
                    "type": "string",
                    "description": "What's in his profile — bio, interests, photos described, any prompts answered",
                },
                "intent": {
                    "type": "string",
                    "enum": ["hookup", "dating", "friendship", "unclear"],
                    "description": "What the user is looking for",
                },
                "platform": {
                    "type": "string",
                    "enum": ["grindr", "scruff", "hinge", "tinder", "feeld", "other"],
                    "description": "Which app this is on",
                },
                "user_vibe": {
                    "type": "string",
                    "description": "Optional: how the user wants to come across (e.g. 'funny', 'confident', 'chill')",
                },
            },
            "required": ["profile_details", "intent", "platform"],
        },
    },
    {
        "name": "suggest_response",
        "description": (
            "Suggest what to say next in a conversation given the recent message history. "
            "Context-aware — reads the tone and adjusts accordingly."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "conversation_history": {
                    "type": "string",
                    "description": "Recent messages in the conversation (format: 'Him: ... / Me: ...')",
                },
                "goal": {
                    "type": "string",
                    "description": "What the user wants to achieve next (e.g., 'move to meetup', 'keep it going', 'find out if he's interested')",
                },
                "tone": {
                    "type": "string",
                    "enum": ["flirty", "casual", "direct", "funny", "warm"],
                    "description": "Desired tone for the response",
                },
            },
            "required": ["conversation_history", "goal"],
        },
    },
    {
        "name": "escalate_conversation",
        "description": (
            "Help naturally escalate a conversation toward a meetup, date, or more intimate territory. "
            "Provides specific lines to move things forward without being pushy or awkward."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "conversation_history": {
                    "type": "string",
                    "description": "The conversation so far",
                },
                "current_stage": {
                    "type": "string",
                    "enum": ["just_matched", "small_talk", "flirting", "pre_meetup"],
                    "description": "Where the conversation currently is",
                },
                "desired_outcome": {
                    "type": "string",
                    "enum": ["coffee_date", "dinner_date", "hookup", "phone_number", "video_call"],
                    "description": "What the user wants to move toward",
                },
            },
            "required": ["conversation_history", "current_stage", "desired_outcome"],
        },
    },
    {
        "name": "recover_conversation",
        "description": (
            "Help rescue a dying or awkward conversation. Analyzes what went wrong "
            "and provides specific messages to get things back on track."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "conversation_history": {
                    "type": "string",
                    "description": "The full conversation including the point where it died or got weird",
                },
                "what_happened": {
                    "type": "string",
                    "description": "User's description of what went wrong or why it's dying",
                },
            },
            "required": ["conversation_history"],
        },
    },
]


def handle_conversation_coach(tool_name: str, tool_input: dict) -> str:
    """Route conversation coach tool calls to the appropriate handler."""

    prompts = {
        "generate_opener": _opener_prompt,
        "suggest_response": _response_prompt,
        "escalate_conversation": _escalate_prompt,
        "recover_conversation": _recover_prompt,
    }

    prompt_fn = prompts.get(tool_name)
    if not prompt_fn:
        return f"Unknown tool: {tool_name}"

    prompt = prompt_fn(tool_input)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        system=(
            "You are a gay dating coach who gives direct, practical advice. "
            "No fluff. No disclaimers. Just what actually works."
        ),
    )
    return response.content[0].text


def _opener_prompt(inp: dict) -> str:
    platform = inp.get("platform", "the app")
    intent = inp.get("intent", "unclear")
    profile = inp["profile_details"]
    vibe = inp.get("user_vibe", "")

    return f"""Write 3 opening messages for this {platform} profile. Intent: {intent}. {f'User wants to come across as: {vibe}.' if vibe else ''}

Profile details: {profile}

Rules:
- No "hey" openers. Ever.
- Each opener should be distinct (playful, direct, conversational)
- Reference something specific from his profile
- Keep them short (1-3 sentences max)
- Sound human, not like a template
- For hookup intent: be more direct but not vulgar unless his profile is explicitly sexual
- For dating intent: show genuine curiosity

Format:
**Opener 1 (playful):** [message]
**Opener 2 (direct):** [message]
**Opener 3 (conversational):** [message]
**Why these work:** [1-2 sentences]"""


def _response_prompt(inp: dict) -> str:
    history = inp["conversation_history"]
    goal = inp["goal"]
    tone = inp.get("tone", "casual")

    return f"""Based on this conversation, suggest 2-3 response options.

Conversation:
{history}

Goal: {goal}
Desired tone: {tone}

Give specific message options, not generic advice. After each option, one sentence on why it works.
Format:
**Option 1:** [message] — [why]
**Option 2:** [message] — [why]
**Option 3 (optional):** [message] — [why]"""


def _escalate_prompt(inp: dict) -> str:
    history = inp["conversation_history"]
    stage = inp["current_stage"]
    outcome = inp["desired_outcome"]

    return f"""Help escalate this conversation from {stage} to suggesting {outcome}.

Conversation so far:
{history}

Desired outcome: {outcome}

Provide 2-3 specific lines to naturally move things forward. The escalation should feel organic, not forced.
Read the energy of the conversation and match it.

Format:
**Move 1 (softer):** [message]
**Move 2 (direct):** [message]
**Move 3 (if he's giving signals):** [message]
**Reading the room:** [1-2 sentences on what the conversation signals]"""


def _recover_prompt(inp: dict) -> str:
    history = inp["conversation_history"]
    what_happened = inp.get("what_happened", "")

    return f"""This conversation needs rescuing. Analyze what happened and give specific recovery messages.

Conversation:
{history}

{f'What the user thinks went wrong: {what_happened}' if what_happened else ''}

Diagnose the problem honestly. Then give 2-3 specific messages to get things back on track.
If it's unsalvageable, say so directly (don't waste his time).

Format:
**What happened:** [honest diagnosis]
**Recovery option 1:** [message]
**Recovery option 2:** [message]
**Verdict:** [is this worth recovering or move on?]"""
