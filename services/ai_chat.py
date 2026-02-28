"""AI Chat service with GPT integration."""
import os
import httpx


class AIChat:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("AI_MODEL", "gpt-4o-mini")
        self.system_prompt = (
            "You are a helpful assistant for NeuroForge AI agency. "
            "We offer: AI digital avatars, smart contract audits, web development, and automation bots. "
            "Be professional, concise, and helpful. If asked about pricing, say starting from $300."
        )

    def chat(self, message: str) -> str:
        if not self.api_key:
            return self._fallback_response(message)

        try:
            response = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": message},
                    ],
                    "max_tokens": 500,
                },
                timeout=30,
            )
            return response.json()["choices"][0]["message"]["content"]
        except Exception:
            return self._fallback_response(message)

    def _fallback_response(self, message: str) -> str:
        msg = message.lower()
        if any(w in msg for w in ["price", "cost", "how much"]):
            return "Our services start from $300. Contact us for a detailed quote!"
        if any(w in msg for w in ["avatar", "video"]):
            return "We create AI digital avatars for marketing! Starting from $500."
        if any(w in msg for w in ["audit", "smart contract", "security"]):
            return "Smart contract audits start from $1000. We check for 15+ vulnerability types."
        return "Thanks for your message! Our team will get back to you shortly. Use /faq for quick answers."
