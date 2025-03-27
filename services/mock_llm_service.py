from utils.log_utils import logger

class MockLLMService:
    async def generate_post(self, topic: str) -> dict:
        logger.info("Generating mock post...")
        return {
            "title": f"[Mock] Artigo sobre: {topic}",
            "body": (
                f"# Introdução\n"
                f"Este é um conteúdo fictício gerado para testes com o tópico '{topic}'.\n\n"
                f"## Desenvolvimento\n"
                f"Conteúdo mockado para ilustrar como a estrutura do texto poderia ficar.\n\n"
                f"## Conclusão\n"
                f"Esse artigo foi gerado de forma simulada.\n\n"
                f"**CTA:** Compartilhe com seus amigos!"
            )
        }
