"""
Wingman Agent — main agentic loop.

Privacy: No conversation data is stored. Sessions are ephemeral.
All processing happens via the Anthropic API. Zero logs of user content.
"""

import os
import json
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from tools import ALL_TOOLS, TOOL_HANDLERS

load_dotenv()


def load_system_prompt() -> str:
    prompt_path = Path(__file__).parent / "prompts" / "system_prompt.txt"
    return prompt_path.read_text(encoding="utf-8")


def run_wingman(user_message: str, conversation_history: list | None = None) -> tuple[str, list]:
    """
    Run a single turn of the Wingman agent loop.

    Args:
        user_message: The user's input
        conversation_history: Prior messages in this session (NOT stored anywhere)

    Returns:
        Tuple of (assistant_response_text, updated_conversation_history)

    Privacy guarantee: conversation_history is an in-memory list only.
    It is never written to disk, database, or any external service.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    system_prompt = load_system_prompt()

    if conversation_history is None:
        conversation_history = []

    messages = conversation_history + [{"role": "user", "content": user_message}]

    # Agent loop — continues until Claude stops calling tools
    while True:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            system=system_prompt,
            tools=ALL_TOOLS,
            messages=messages,
        )

        # Collect all content blocks
        assistant_content = response.content

        # Add assistant turn to history
        messages.append({"role": "assistant", "content": assistant_content})

        # If Claude is done, return
        if response.stop_reason == "end_turn":
            # Extract text from final response
            text_parts = [
                block.text for block in assistant_content if block.type == "text"
            ]
            final_text = "\n\n".join(text_parts)
            return final_text, messages

        # Handle tool use
        if response.stop_reason == "tool_use":
            tool_results = []

            for block in assistant_content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_use_id = block.id

                    handler = TOOL_HANDLERS.get(tool_name)
                    if handler:
                        try:
                            result = handler(tool_name, tool_input)
                        except Exception as e:
                            result = f"Tool error: {str(e)}"
                    else:
                        result = f"Unknown tool: {tool_name}"

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": result,
                    })

            # Add tool results as user message
            messages.append({"role": "user", "content": tool_results})

        else:
            # Unexpected stop reason
            text_parts = [
                block.text for block in assistant_content if block.type == "text"
            ]
            return "\n\n".join(text_parts) or "Something went wrong. Try again.", messages


def run_cli():
    """Run the interactive CLI interface."""
    print("\n" + "="*60)
    print("  WINGMAN — Your Gay Dating Coach & Safety Companion")
    print("="*60)
    print("  Privacy: Zero data stored. Session ends when you exit.")
    print("  Type 'quit' or 'exit' to end the session.")
    print("="*60 + "\n")

    conversation_history = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nSession ended. Take care out there.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "bye"):
            print("\nWingman: Take care out there. 🏳️‍🌈")
            break

        print("\nWingman: ", end="", flush=True)

        try:
            response, conversation_history = run_wingman(user_input, conversation_history)
            print(response)
        except anthropic.AuthenticationError:
            print("API key issue. Check your .env file.")
            break
        except Exception as e:
            print(f"Something went wrong: {e}")

        print()


if __name__ == "__main__":
    run_cli()
