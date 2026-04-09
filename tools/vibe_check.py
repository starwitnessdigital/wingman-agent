"""
Vibe Check — message decoder, compatibility analysis, ghosting probability,
interest assessment.
"""

import anthropic

client = anthropic.Anthropic()

VIBE_CHECK_TOOLS = [
    {
        "name": "decode_message",
        "description": (
            "Decode what a specific message or behavior actually means in context. "
            "'He said X, what does that mean?' Gets a real, honest answer."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "message_or_behavior": {
                    "type": "string",
                    "description": "The specific message or behavior to decode",
                },
                "conversation_context": {
                    "type": "string",
                    "description": "Optional: surrounding conversation context",
                },
                "platform": {
                    "type": "string",
                    "description": "Which app or context this is from",
                },
            },
            "required": ["message_or_behavior"],
        },
    },
    {
        "name": "compatibility_check",
        "description": (
            "Assess compatibility based on conversation patterns, stated preferences, "
            "and behavioral signals. Honest assessment of long-term fit."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "conversation": {
                    "type": "string",
                    "description": "The conversation to analyze",
                },
                "user_wants": {
                    "type": "string",
                    "description": "What the user is looking for",
                },
                "his_apparent_wants": {
                    "type": "string",
                    "description": "What he seems to be looking for",
                },
            },
            "required": ["conversation"],
        },
    },
    {
        "name": "ghosting_probability",
        "description": (
            "Assess the probability of being ghosted based on engagement signals. "
            "Honest assessment with specific reasoning."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "conversation": {
                    "type": "string",
                    "description": "The full conversation",
                },
                "recent_pattern": {
                    "type": "string",
                    "description": "Description of recent engagement patterns (response times, length of replies, etc.)",
                },
                "stage": {
                    "type": "string",
                    "enum": ["just_matched", "early_chat", "established_chat", "post_meetup", "dating"],
                    "description": "Stage of the connection",
                },
            },
            "required": ["conversation"],
        },
    },
    {
        "name": "is_he_interested",
        "description": (
            "Honest assessment: is he actually interested or just passing time? "
            "Analyzes engagement signals and gives a direct answer."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "conversation": {
                    "type": "string",
                    "description": "The conversation to analyze",
                },
                "behaviors": {
                    "type": "string",
                    "description": "Any behaviors outside the conversation (viewed profile, unmatched/rematched, etc.)",
                },
                "what_user_wants": {
                    "type": "string",
                    "enum": ["hookup", "dating", "relationship", "unclear"],
                },
            },
            "required": ["conversation"],
        },
    },
]


def handle_vibe_check(tool_name: str, tool_input: dict) -> str:
    """Route vibe check tool calls."""

    prompts = {
        "decode_message": _decode_prompt,
        "compatibility_check": _compatibility_prompt,
        "ghosting_probability": _ghosting_prompt,
        "is_he_interested": _interested_prompt,
    }

    prompt_fn = prompts.get(tool_name)
    if not prompt_fn:
        return f"Unknown tool: {tool_name}"

    prompt = prompt_fn(tool_input)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=900,
        messages=[{"role": "user", "content": prompt}],
        system=(
            "You are a blunt but kind friend who gives honest assessments of dating situations. "
            "No sugarcoating, no false hope, no doom and gloom — just the truth. "
            "You understand gay dating culture deeply. "
            "You read between the lines accurately. "
            "You don't project emotions onto people who haven't shown them."
        ),
    )
    return response.content[0].text


def _decode_prompt(inp: dict) -> str:
    message = inp["message_or_behavior"]
    context = inp.get("conversation_context", "")
    platform = inp.get("platform", "")

    return f"""Decode what this actually means.

{"Platform: " + platform if platform else ""}
Message/behavior: "{message}"
{f'Context: {context}' if context else ''}

Give:
1. **Most likely meaning** — the most probable interpretation
2. **Alternative readings** — other possible interpretations (if relevant)
3. **What it signals** about his interest/intentions
4. **Recommended response** — what to do with this information

Be direct. If "let's hang sometime" with no follow-up means he's not interested, say that.
If "I've been busy" after days of silence means he's pulling back, say that.
Don't manufacture hope. Don't catastrophize either."""


def _compatibility_prompt(inp: dict) -> str:
    conversation = inp["conversation"]
    user_wants = inp.get("user_wants", "unclear")
    his_wants = inp.get("his_apparent_wants", "unclear")

    return f"""Assess compatibility based on this conversation.

Conversation:
{conversation}

What the user wants: {user_wants}
What he seems to want: {his_wants}

Analyze:
1. **Alignment score**: High / Medium / Low / Misaligned
2. **What aligns** — specific things they seem to have in common
3. **Tension points** — where they seem to want different things
4. **Reading between the lines** — what the conversation reveals about him beyond what's explicit
5. **Honest take** — is this worth pursuing for the user's stated goal?

Don't tell people what they want to hear. If the wants are fundamentally misaligned, say so clearly.
If there's genuine compatibility, show the evidence."""


def _ghosting_prompt(inp: dict) -> str:
    conversation = inp["conversation"]
    pattern = inp.get("recent_pattern", "")
    stage = inp.get("stage", "early_chat")

    return f"""Assess ghosting probability based on this conversation.

Stage of connection: {stage}
{f'Recent engagement pattern: {pattern}' if pattern else ''}

Conversation:
{conversation}

Give:
1. **Ghosting probability**: Very Low / Low / Medium / High / Very High
2. **Key signals** driving this assessment (quote specific patterns)
3. **What's actually happening** — honest read on his engagement level
4. **What would change the assessment** — signals that would move it up or down
5. **Recommended move** — what to do (reach out, wait, move on, etc.)

Ghosting signals to look for: decreasing message length, longer response gaps, vague answers,
dropped threads, no reciprocal questions, "sounds good" type responses, avoiding plans.

Engagement signals: quick responses, asks questions back, references previous things said,
initiates, makes specific plans."""


def _interested_prompt(inp: dict) -> str:
    conversation = inp["conversation"]
    behaviors = inp.get("behaviors", "")
    wants = inp.get("what_user_wants", "unclear")

    return f"""Honest assessment: is he actually interested?

What the user is looking for: {wants}
{f'Behaviors outside conversation: {behaviors}' if behaviors else ''}

Conversation:
{conversation}

Give a direct answer:
1. **Verdict**: Yes / Probably / Mixed signals / Probably not / No
2. **Evidence for interest** — specific things he's said/done
3. **Evidence against** — specific things that suggest he's not
4. **What kind of interested** — hookup interested vs. actually wants more (if relevant)
5. **The honest take** — what's actually going on here

Don't spare their feelings if the evidence points to "he's just bored" or "he's keeping options open."
But also don't dismiss genuine interest signals. Read what's actually there."""
