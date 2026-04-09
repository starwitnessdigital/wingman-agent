"""
Safety Companion — red flag detection, catfish scoring, sextortion warnings,
meetup safety checklists, exit strategies.

Privacy note: No conversation data is stored. Analysis happens in-memory only.
"""

import anthropic

client = anthropic.Anthropic()

SAFETY_COMPANION_TOOLS = [
    {
        "name": "analyze_red_flags",
        "description": (
            "Analyze a conversation or profile for manipulation patterns, red flags, "
            "and concerning behaviors. Returns specific flags with explanations."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The conversation history or profile text to analyze",
                },
                "content_type": {
                    "type": "string",
                    "enum": ["conversation", "profile", "both"],
                },
                "context": {
                    "type": "string",
                    "description": "Optional: any additional context about the situation",
                },
            },
            "required": ["content", "content_type"],
        },
    },
    {
        "name": "catfish_risk_score",
        "description": (
            "Assess the likelihood that someone is not who they claim to be. "
            "Analyzes conversation patterns, profile consistency, and behavioral signals."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "conversation": {
                    "type": "string",
                    "description": "The conversation history",
                },
                "profile_description": {
                    "type": "string",
                    "description": "Description of their profile (photos, bio, info)",
                },
                "behaviors_observed": {
                    "type": "string",
                    "description": "Any specific behaviors that raised suspicion",
                },
            },
            "required": ["conversation"],
        },
    },
    {
        "name": "meetup_safety_checklist",
        "description": (
            "Generate a personalized meetup safety checklist based on the situation. "
            "Covers location sharing, check-in schedules, exit signals, and practical tips."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "meetup_type": {
                    "type": "string",
                    "enum": ["first_meet_public", "first_meet_private", "hookup_theirs", "hookup_yours", "date"],
                    "description": "Type of meetup",
                },
                "known_about_them": {
                    "type": "string",
                    "description": "What the user knows about this person (name, verified info, how long chatting, etc.)",
                },
                "comfort_level": {
                    "type": "string",
                    "enum": ["very_comfortable", "mostly_comfortable", "somewhat_nervous", "nervous"],
                    "description": "How comfortable the user feels about this meetup",
                },
            },
            "required": ["meetup_type"],
        },
    },
    {
        "name": "detect_sextortion",
        "description": (
            "Analyze a conversation for sextortion warning signs — early pressure for explicit "
            "content, refusal to video verify, escalating requests, blackmail setup patterns."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "conversation": {
                    "type": "string",
                    "description": "The conversation to analyze",
                },
                "specific_concern": {
                    "type": "string",
                    "description": "What specifically concerned the user",
                },
            },
            "required": ["conversation"],
        },
    },
    {
        "name": "exit_strategy",
        "description": (
            "Get specific strategies and exact messages to exit an uncomfortable situation — "
            "whether that's a conversation, a date, or a hookup that's gone wrong."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "situation": {
                    "type": "string",
                    "description": "Describe the situation that needs an exit",
                },
                "urgency": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "immediate"],
                    "description": "How urgently an exit is needed",
                },
                "relationship_type": {
                    "type": "string",
                    "enum": ["online_chat", "date", "hookup", "ongoing_connection"],
                },
            },
            "required": ["situation", "urgency"],
        },
    },
]


def handle_safety_companion(tool_name: str, tool_input: dict) -> str:
    """Route safety companion tool calls."""

    prompts = {
        "analyze_red_flags": _red_flags_prompt,
        "catfish_risk_score": _catfish_prompt,
        "meetup_safety_checklist": _meetup_checklist_prompt,
        "detect_sextortion": _sextortion_prompt,
        "exit_strategy": _exit_prompt,
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
            "You are a safety advisor who specializes in online dating safety for gay men. "
            "You are direct, non-alarmist, and practical. You don't catastrophize but you don't downplay real risks. "
            "You give specific, actionable guidance. You understand that people are going to take risks regardless, "
            "so your job is to help them take smarter ones. You never shame or lecture."
        ),
    )
    return response.content[0].text


def _red_flags_prompt(inp: dict) -> str:
    content = inp["content"]
    content_type = inp["content_type"]
    context = inp.get("context", "")

    return f"""Analyze this {content_type} for red flags and concerning patterns.

Content:
{content}

{f'Additional context: {context}' if context else ''}

Identify:
1. **Red flags found** — list each one with a brief explanation of why it's concerning
2. **Severity level** — overall: Low / Medium / High / Serious
3. **Specific patterns** — name any manipulation tactics if present (love bombing, isolation, pressure tactics, etc.)
4. **What to watch for** — next warning signs to look out for
5. **Recommended action** — what the user should do

Be honest. If there are no real red flags, say so — don't manufacture concern. If it's serious, be clear about that too.
Don't be preachy. State the facts and let the person decide."""


def _catfish_prompt(inp: dict) -> str:
    conversation = inp["conversation"]
    profile = inp.get("profile_description", "")
    behaviors = inp.get("behaviors_observed", "")

    return f"""Assess the catfish risk for this person.

Conversation:
{conversation}

{f'Profile description: {profile}' if profile else ''}
{f'Suspicious behaviors noted: {behaviors}' if behaviors else ''}

Give:
1. **Risk score**: Low (10-30%) / Medium (30-60%) / High (60-80%) / Very High (80%+)
2. **Key signals** — specific things in this conversation/profile that support this score
3. **Authenticity indicators** — things that suggest they might be real
4. **Verification suggestions** — specific, practical ways to verify (video call, reverse image search tips, etc.)
5. **Bottom line** — direct assessment

Common catfish tells: stock photos, inconsistent details, won't video call, "travels a lot," profiles with too-good-to-be-true photos, profiles that feel generic.
Common sextortion catfish tells: quick escalation to explicit requests, refusal to video, very attractive photos, often overseas or military."""


def _meetup_checklist_prompt(inp: dict) -> str:
    meetup_type = inp["meetup_type"]
    known = inp.get("known_about_them", "not much")
    comfort = inp.get("comfort_level", "mostly_comfortable")

    type_descriptions = {
        "first_meet_public": "first meeting in a public place",
        "first_meet_private": "first meeting at a private location",
        "hookup_theirs": "hookup at their place",
        "hookup_yours": "hookup at your place",
        "date": "a date",
    }
    type_desc = type_descriptions.get(meetup_type, meetup_type)

    return f"""Generate a practical safety checklist for a {type_desc}.

What they know about him: {known}
Comfort level: {comfort}

Create a specific, practical checklist. Not overwhelming — prioritized by importance.

Format:
**Before you go:**
- [specific action]

**Share this info with a friend:**
- [specific info to share]

**Check-in plan:**
- [specific check-in schedule]

**Exit signals:**
- [specific safe words or signals to set up with a friend]

**When you're there:**
- [specific safety tips relevant to this type of meetup]

**If something feels off:**
- [specific actions to take]

Keep it practical and un-preachy. These are adults who know what they're doing — just give them the tools."""


def _sextortion_prompt(inp: dict) -> str:
    conversation = inp["conversation"]
    concern = inp.get("specific_concern", "")

    return f"""Analyze this conversation for sextortion warning signs.

Conversation:
{conversation}

{f'Specific concern: {concern}' if concern else ''}

Sextortion setup patterns to check for:
- Early escalation to explicit content requests (within first few messages)
- Refusing to video verify / making excuses not to video call
- Pressure combined with flattery to send explicit photos/videos
- Asking for increasingly explicit content over time
- "Screenshots" or recording implications
- Profile that seems too attractive / stock photo vibes
- Overseas location / military claims
- Quick emotional attachment (to lower guard)

Give:
1. **Sextortion risk**: None / Low / Medium / High / Active threat
2. **Specific warning signs** found (quote exact patterns if present)
3. **What's likely happening** — honest assessment
4. **Immediate recommendations** — exactly what to do right now

If this is an active sextortion attempt already in progress, give clear guidance on:
- Do NOT pay — it escalates demands
- Block and report
- Who to contact if needed (FBI IC3 at ic3.gov, NCMEC at cybertipline.org)

Be direct. This can be a serious situation."""


def _exit_prompt(inp: dict) -> str:
    situation = inp["situation"]
    urgency = inp["urgency"]
    rel_type = inp.get("relationship_type", "online_chat")

    urgency_context = {
        "low": "This is a low-pressure situation — a graceful exit is fine.",
        "medium": "They want out but there's no immediate danger.",
        "high": "This needs to happen soon — clear exit strategy needed.",
        "immediate": "IMMEDIATE EXIT NEEDED. Prioritize safety above politeness.",
    }

    return f"""Provide an exit strategy for this situation.

Situation: {situation}
Urgency: {urgency} — {urgency_context.get(urgency, '')}
Context: {rel_type}

Give:
1. **Immediate action** — exactly what to do right now
2. **Exit message options** (2-3 options ranging from polite to blunt) — ready to copy-paste
3. **If they push back** — how to handle resistance
4. **After the exit** — any follow-up steps (block, report, etc.)

{'''
SAFETY FIRST: For immediate exits — getting out safely is more important than being polite.
Real exit excuses that work in person: sudden illness, emergency call from family, someone you know just arrived.
If you feel unsafe in person: text a friend "Code X" (or whatever signal you set up), call yourself and fake an emergency, go to a public area.
''' if urgency == 'immediate' else ''}

Don't make them feel bad for wanting to exit a situation that's not working. Everyone deserves to leave."""
