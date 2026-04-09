# Wingman Privacy Policy

**Last updated: April 8, 2026**

This is a human-readable privacy policy. No legal maze. Just the facts.

---

## The short version

Wingman doesn't store your conversations. It doesn't know who you are. It doesn't track you. It can't out you because it doesn't hold anything that would.

---

## What data touches the server

### What we DO process (temporarily):
- The message you send in a given session
- The conversation history for the current session (held in RAM)
- Your IP address (standard web server logs — see below)

### What we DON'T store:
- Conversation content — never written to disk, database, or any log
- User accounts, profiles, or identities
- Device fingerprints or persistent identifiers
- Behavioral analytics
- Location data
- Any information that could identify you as a gay, bi, queer, or questioning person

---

## Sessions

Sessions are ephemeral memory only. When your session expires (default: 30 minutes of inactivity) or the server restarts, the conversation is gone permanently. There is no recovery mechanism because there is no storage.

You can also explicitly delete your session via the `/session/{id}` DELETE endpoint, which immediately clears it from memory.

**No session IDs are linked to any persistent identity.** A session ID is a random UUID generated at the start of a conversation. It exists only to maintain context within that session. It is not stored after the session expires.

---

## The AI provider

Wingman uses the Anthropic API to generate responses. Your messages are sent to Anthropic's servers to generate a response. Anthropic's data handling is governed by their own privacy policy.

**What this means in practice:** Anthropic does not train on API user data by default (as of their current policy). Your messages are processed to generate a response and not retained for model training. Check Anthropic's current privacy policy for the authoritative statement.

We do not use any other AI provider. We do not share your conversation with any third party beyond Anthropic.

---

## Web server logs

Standard web server access logs may record:
- IP address
- Timestamp
- HTTP method and path (e.g., `POST /chat`)
- Response status code
- Browser user agent

These logs do **not** contain conversation content. They are used for debugging and security monitoring. They are retained for a maximum of 30 days and then deleted.

---

## No analytics

We do not use Google Analytics, Mixpanel, Amplitude, or any third-party analytics service. No tracking pixels. No session recording tools.

---

## No advertising

We don't sell, rent, or share any data with advertisers. We don't have an advertising model. The business model is subscriptions.

---

## Our commitment to the community

Wingman was built by a gay man who understands what's at stake when someone's sexual orientation or dating life is exposed without consent.

**We will never:**
- Sell data that could reveal someone's sexual orientation
- Share conversation data with any third party
- Comply with data requests without a valid legal order
- Notify anyone that a specific person used this service (absent a legal obligation)

**We will always:**
- Tell you clearly what data we do hold (answer: almost nothing)
- Give you a way to clear your session immediately
- Maintain this policy in plain language

---

## If you're in a country with data protection rights

**EU/UK (GDPR/UK GDPR):** Given that we process your IP address in server logs, you have rights including access, rectification, erasure, and objection. Since we don't store conversation data, there's typically nothing to access or erase beyond standard log entries. Contact us at the address below if you want to exercise these rights.

**California (CCPA):** We don't sell personal information. We don't share personal information for cross-context behavioral advertising.

---

## Changes to this policy

If we make material changes to this policy, we'll update the date at the top and note what changed. The policy lives in the open-source repository so the full history is visible.

---

## Contact

Questions about privacy: open an issue at [github.com/starwitnessdigital/wingman-agent](https://github.com/starwitnessdigital/wingman-agent)

---

*Wingman is not a mental health service, crisis service, or professional counselor. If you are in danger, contact emergency services. If you are struggling, the Trevor Project is available at 1-866-488-7386 or TheTrevorProject.org.*
