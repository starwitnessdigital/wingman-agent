"""
Wingman Demo — showcases each feature with sample conversations.

Run: python demo.py
Run specific: python demo.py --feature opener
"""

import argparse
import time
from main import run_wingman


DEMOS = {
    "opener": {
        "title": "Conversation Coach — Opener Generation",
        "prompt": (
            "I matched with a guy on Hinge. His profile says he's a chef, "
            "loves hiking, has a photo with his dog (Golden Retriever), "
            "and answered the prompt 'My most controversial opinion' with "
            "'brunch is overrated and you all know it.' "
            "I want to date this guy, not just hook up. What do I open with?"
        ),
    },
    "escalate": {
        "title": "Conversation Coach — Escalation",
        "prompt": (
            "We've been chatting on Scruff for a week. Conversation: "
            "'Him: hey / Me: hey! cool profile / Him: thanks yours too, where you from? / "
            "Me: Brooklyn, you? / Him: Upper West Side / Me: nice, you out much? / "
            "Him: not as much as I'd like lol work is crazy / Me: what do you do? / "
            "Him: finance, boring I know haha. you? / Me: graphic designer / "
            "Him: nice that's actually cool / Me: thanks :) / Him: so what are you into? / "
            "Me: [crickets because I froze]'. "
            "How do I respond to 'what are you into' and move toward actually meeting?"
        ),
    },
    "profile": {
        "title": "Profile Optimizer — Grindr Bio Rewrite",
        "prompt": (
            "Can you rewrite my Grindr bio? Current bio: 'Just a normal guy looking to "
            "meet cool people. I work in tech, like to travel. Looking for fun and maybe more.' "
            "I'm 28, masc presenting, vers, into outdoor stuff, music festivals, cooking. "
            "Looking for hookups mostly but open to something more. "
            "Don't want couples or people WAY older than me."
        ),
    },
    "safety": {
        "title": "Safety Companion — Red Flag Analysis",
        "prompt": (
            "Can you check this conversation for red flags? "
            "Him (first message on Grindr): 'hey gorgeous, you are exactly my type' "
            "Me: 'thanks, what's up?' "
            "Him: 'been thinking about you all day, you have such an amazing energy' "
            "Me: 'we just matched lol' "
            "Him: 'i know but I have a feeling about you. I'm actually in the military right now in Germany' "
            "Me: 'oh ok' "
            "Him: 'I'd love to see more of you, you seem very sexy. can you send me some pics?' "
            "Me: 'maybe, are you going to send any?' "
            "Him: 'I can't right now, security reasons. but I will when I'm back. I'd really love to see you' "
            "Does this seem off to you?"
        ),
    },
    "sextortion": {
        "title": "Safety Companion — Sextortion Detection",
        "prompt": (
            "This guy matched with me on Instagram (not even a dating app), "
            "said he found me through a mutual friend. He's been really flirty and escalated fast. "
            "After maybe 30 minutes of chatting he asked me to send explicit photos "
            "and said 'I'll send mine after.' When I asked for a video call to verify he's real "
            "he said his camera is broken and he's 'shy on camera anyway.' "
            "He keeps pushing for the photos and says 'I just want to see the real you.' "
            "Is this sextortion?"
        ),
    },
    "vibe": {
        "title": "Vibe Check — Is He Interested?",
        "prompt": (
            "Been talking to this guy on Hinge for 2 weeks. He responds every day, "
            "conversation flows well, he laughs at my jokes, asks me questions. "
            "But every time I hint at meeting up he says something like "
            "'yeah we should do that sometime!' and doesn't follow through with actual plans. "
            "This has happened 3 times. Is he interested or is he just being friendly?"
        ),
    },
    "decode": {
        "title": "Vibe Check — Message Decoder",
        "prompt": (
            "He texted me 'hey stranger' after not responding to my last message for 8 days. "
            "What does that mean and should I respond?"
        ),
    },
    "meetup": {
        "title": "Safety Companion — Meetup Checklist",
        "prompt": (
            "I'm meeting a guy from Grindr at his place tomorrow night. "
            "We've only been talking for 4 days. I've seen his face on video call briefly "
            "but he made it quick. I'm a little nervous but he seems okay. "
            "What should I do to stay safe?"
        ),
    },
}


def run_demo(feature: str, show_title: bool = True):
    demo = DEMOS[feature]
    if show_title:
        print(f"\n{'='*65}")
        print(f"  DEMO: {demo['title']}")
        print(f"{'='*65}")

    print(f"\n📱 User: {demo['prompt']}\n")
    print("🤝 Wingman: ", end="", flush=True)

    response, _ = run_wingman(demo["prompt"])
    print(response)


def run_all_demos():
    print("\n" + "="*65)
    print("  WINGMAN DEMO — Showing all features")
    print("="*65)
    print("  Privacy: All demo conversations are ephemeral. Nothing stored.")
    print("="*65)

    for i, (feature, demo) in enumerate(DEMOS.items()):
        run_demo(feature, show_title=True)
        if i < len(DEMOS) - 1:
            print("\n" + "-"*65)
            input("\n  Press Enter for next demo...")


def main():
    parser = argparse.ArgumentParser(description="Wingman feature demos")
    parser.add_argument(
        "--feature",
        choices=list(DEMOS.keys()) + ["all"],
        default="all",
        help="Which feature to demo",
    )
    args = parser.parse_args()

    if args.feature == "all":
        run_all_demos()
    else:
        run_demo(args.feature)

    print("\n\n" + "="*65)
    print("  Demo complete.")
    print("  Privacy reminder: No conversation data was stored.")
    print("="*65 + "\n")


if __name__ == "__main__":
    main()
