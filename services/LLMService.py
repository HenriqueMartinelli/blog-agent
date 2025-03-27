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
        # prompt = self._build_prompt(topic)
        # response = await self.client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "Você é um redator experiente."},
        #         {"role": "user", "content": prompt}
        #     ]
        #     )
        # raw_text = response.choices[0].message.content
        # logger.info("Post gerado com sucesso")
        raw_text = """**Título: Tudo o que você precisa saber sobre o eVisa para o Brasil - FAQ e Mega-thread**                                                                                                                                          
blog_api       | 
blog_api       | Se você está planejando uma viagem para o Brasil, saiba que o processo de obtenção do visto eletrônico, também conhecido como eVisa, é um passo fundamental. Com o objetivo de facilitar a entrada de turistas estrangeiros no país, o eVisa é uma alternativa prática e conveniente para quem deseja visitar as belas paisagens e a rica cultura brasileira. Neste artigo, abordaremos as perguntas mais frequentes sobre o eVisa para o Brasil, proporcionando a você um guia completo para planejar sua próxima aventura.
blog_api       | 
blog_api       | **O que é o eVisa?**                                                                                                                               
blog_api       | 
blog_api       | O eVisa é um visto eletrônico que permite que cidadãos de determinados países entrem no Brasil para fins de turismo, negócios, tratamento médico ou participação em atividades culturais e esportivas. Este tipo de visto é emitido pela Polícia Federal do Brasil de forma eletrônica, dispensando a necessidade de comparecer a um consulado ou embaixada.
blog_api       | 
blog_api       | **Quais são os requisitos para solicitar o eVisa para o Brasil?**                                                                                  
blog_api       |                                                                                                                                                    
blog_api       | Os principais requisitos para solicitar o eVisa para o Brasil incluem:                                                                             
blog_api       | - Ter um passaporte válido
blog_api       | - Ter uma foto digital recente                                                                                                                     
blog_api       | - Fornecer informações sobre a sua viagem, como passagem de volta e documentos de reserva de hospedagem                                            
blog_api       | - Pagar a taxa de processamento do visto                                                                                                           
blog_api       | 
blog_api       | Além disso, é importante verificar se o seu país de origem está na lista de nacionalidades elegíveis para o eVisa brasileiro.                      
blog_api       |                                                                                                                                                    
blog_api       | **Qual é o processo de solicitação do eVisa?**                                                                                                     
blog_api       |                                                                                                                                                    
blog_api       | O processo de solicitação do eVisa é simples e pode ser feito completamente online. Basta acessar o site oficial do governo brasileiro dedicado à emissão do visto eletrônico, preencher o formulário de solicitação com suas informações pessoais e de viagem, carregar os documentos solicitados e pagar a taxa de processamento. Em seguida, aguarde a aprovação do seu eVisa, que geralmente é enviada por e-mail em poucos dias.
blog_api       | 
blog_api       | **Quais são as condições de validade do eVisa?**
blog_api       |                                                                                                                                                    
blog_api       | O eVisa para o Brasil é válido por até 2 anos a partir da data de emissão e permite múltiplas entradas no país, com estadias de até 90 dias por visita. É importante respeitar o período de validade do visto e as condições de permanência estabelecidas pelas autoridades brasileiras para evitar problemas durante a sua viagem.
blog_api       | 
blog_api       | **Como proceder em caso de dúvidas ou problemas durante a solicitação do eVisa?**                                                                  
blog_api       |                                                                                                                                                    
blog_api       | Caso você tenha alguma dúvida ou encontre algum problema durante o processo de solicitação do eVisa para o Brasil, recomenda-se entrar em contato com o suporte ao cliente do site oficial do governo brasileiro. Eles estão disponíveis para ajudar e esclarecer qualquer questão relacionada ao visto eletrônico.    
blog_api       | 
blog_api       | **Conclusão:**                                                                                                                                     
blog_api       | O eVisa para o Brasil é uma alternativa prática e ágil para facilitar a entrada de turistas estrangeiros no país. Com requisitos simples e um processo de solicitação online, o eVisa torna mais acessível a experiência de conhecer as maravilhas do Brasil. Portanto, se você está planejando uma viagem para este destino incrível, não deixe de se informar sobre o eVisa e realizar sua solicitação com antecedência.
blog_api       | 
blog_api       | Aproveite tudo o que o Brasil tem a oferecer e faça o seu eVisa agora mesmo!                                                                       
blog_api       |                                                                                                                                                    
blog_api       | Esperamos que este guia tenha esclarecido as suas dúvidas e ajudado a planejar a sua viagem. Boa viagem e divirta-se explorando as belezas do Brasil!                                                                                                                                                                  
blog_api       | 
blog_api       | *Artigo produzido por [Seu Nome] - redator experiente*
blog_api       |                                                                                                                                                    
blog_api       | **CTA:**                                                                                                                                           
blog_api       | Para mais informações ou para solicitar o seu eVisa para o Brasil, acesse o site oficial do governo brasileiro e inicie o seu processo de solicitação agora mesmo. Viaje com tranquilidade e aproveite ao máximo sua estadia no Brasil!             """

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
