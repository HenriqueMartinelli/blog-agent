# app/services/llm_service.py
from openai import AsyncOpenAI
from core.settings import settings


from tenacity import retry, wait_random, stop_after_attempt, retry_if_exception_type, before_sleep_log
from openai import APIError, RateLimitError, Timeout
from utils.log_utils import logger

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


    @retry(
        retry=retry_if_exception_type((RateLimitError, Timeout, APIError)),
        wait=wait_random(min=1, max=3),
        stop=stop_after_attempt(3),
        reraise=True
    )
    async def generate_post(self, topic: str) -> dict:
        """
        Generates a blog post using the GPT-3.5 model.
        args:
            topic (str): The topic of the blog post.
        returns:
            dict: The generated blog
            post.
        """
        logger.info("Generating post...")
        prompt = self._build_prompt(topic)
        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Você é um redator experiente."},
                {"role": "user", "content": prompt}
            ]
            )
        raw_text = response.choices[0].message.content
        logger.info("Post gerado com sucesso")

        return self._parse_llm_output(raw_text)


    def _parse_llm_output(self, content: str) -> dict:
        """
        Extrai título e corpo do texto gerado pela IA.

        Args:
            content (str): Texto em Markdown retornado pela IA.

        Returns:
            dict: {"title": ..., "body": ...}
        """
        lines = content.strip().splitlines()

        title = "Título Desconhecido"
        body_lines = list()

        for i, line in enumerate(lines):
            if line.strip().lower().startswith("**título:"):
                title = line.strip().replace("**Título:", "").replace("**", "").strip()
                body_lines = lines[i + 1:]
                break

        body = "\n".join(body_lines).strip()

        return {
            "title": title,
            "body": body
        }
    

    def _build_prompt(self, topic: str) -> str:
        """
        Builds a prompt for the GPT-3.5 model.
        args:
            topic (str): The topic of the blog post.
        returns:
            str: The generated prompt
        """
        logger.info("Building prompt...", extra={"topic": topic})
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
