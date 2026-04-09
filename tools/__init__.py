from tools.conversation_coach import CONVERSATION_COACH_TOOLS, handle_conversation_coach
from tools.profile_optimizer import PROFILE_OPTIMIZER_TOOLS, handle_profile_optimizer
from tools.safety_companion import SAFETY_COMPANION_TOOLS, handle_safety_companion
from tools.vibe_check import VIBE_CHECK_TOOLS, handle_vibe_check

ALL_TOOLS = (
    CONVERSATION_COACH_TOOLS
    + PROFILE_OPTIMIZER_TOOLS
    + SAFETY_COMPANION_TOOLS
    + VIBE_CHECK_TOOLS
)

TOOL_HANDLERS = {
    # Conversation Coach
    "generate_opener": handle_conversation_coach,
    "suggest_response": handle_conversation_coach,
    "escalate_conversation": handle_conversation_coach,
    "recover_conversation": handle_conversation_coach,
    # Profile Optimizer
    "optimize_profile": handle_profile_optimizer,
    "review_photos": handle_profile_optimizer,
    "platform_tips": handle_profile_optimizer,
    # Safety Companion
    "analyze_red_flags": handle_safety_companion,
    "catfish_risk_score": handle_safety_companion,
    "meetup_safety_checklist": handle_safety_companion,
    "detect_sextortion": handle_safety_companion,
    "exit_strategy": handle_safety_companion,
    # Vibe Check
    "decode_message": handle_vibe_check,
    "compatibility_check": handle_vibe_check,
    "ghosting_probability": handle_vibe_check,
    "is_he_interested": handle_vibe_check,
}
