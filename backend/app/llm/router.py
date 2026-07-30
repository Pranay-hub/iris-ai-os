import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class IRISRouter:
    def __init__(self):
        if not OPENROUTER_API_KEY:
            raise RuntimeError("OPENROUTER_API_KEY is missing. Check backend/.env")

        self.headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        self.models = {
            "planner": "deepseek/deepseek-r1-0528",
            "chat": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
            "fast": "meta-llama/llama-3.1-8b-instruct:free",
        }

    def run(self, user_input: str, mode: str = "auto"):
        model = self.select_model(user_input, mode)

        payload = {
    "model": model,
    "messages": [
        {"role": "system", "content": self.get_system_prompt(mode)},
        {"role": "user", "content": user_input},
    ],
    "max_tokens": 1024,
}

        response = requests.post(
            OPENROUTER_URL,
            headers=self.headers,
            json=payload,
            timeout=60,
        )

        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        result = response.json()

        if response.status_code != 200:
            return f"OpenRouter error {response.status_code}: {result}"

        if "choices" not in result:
            return f"Unexpected OpenRouter response: {result}"

        return result["choices"][0]["message"]["content"]

    def select_model(self, user_input: str, mode: str):
        if mode in self.models:
            return self.models[mode]

        if any(word in user_input.lower() for word in [
            "build", "plan", "design", "workflow", "step by step"
        ]):
            return self.models["planner"]

        if len(user_input) < 50:
            return self.models["fast"]

        return self.models["chat"]

    def get_system_prompt(self, mode: str):
        if mode == "planner":
            return (
                "You are IRIS Planner Brain. Break tasks into clear steps. "
                "Prefer structured JSON when planning tools or workflows."
            )

        if mode == "chat":
            return "You are IRIS. Be helpful, concise, and natural."

        return "You are IRIS."