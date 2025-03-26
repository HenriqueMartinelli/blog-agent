# services/llm_service.py

import openai
from core.settings import settings


class LLMService:
    def __init__(self) -> None:
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL

    async def generate_post(self, topic: str) -> dict:
        prompt = self._build_prompt(topic)

        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[
                {"role": "system", "content": "Você é um redator experiente em blogs."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )

        content = response.choices[0].message["content"]
        return {
            "title": f"Artigo sobre: {topic}",
            "body": content.strip()
        }

    def _build_prompt(self, topic: str) -> str:
        return (
            f"Escreva um artigo de blog com pelo menos 800 palavras sobre o seguinte tema:\n"
            f"\"{topic}\"\n\n"
            f"O artigo deve:\n"
            f"- Ter um título chamativo\n"
            f"- Conter subtítulos bem distribuídos\n"
            f"- Usar uma linguagem clara e objetiva\n"
            f"- Terminar com uma chamada para ação (CTA)\n\n"
            f"Retorne o conteúdo completo em formato de blog."
        )
