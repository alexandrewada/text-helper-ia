"""
IA client for OpenAI integration
"""
from typing import Dict, Optional, Any
from openai import OpenAI
from .config import Config
from .logger import Logger


class AIClient:
    """OpenAI client wrapper with error handling and retry logic"""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        self.client = None
        self._setup_clients()
    
    def _setup_clients(self) -> None:
        """Setup OpenAI clients"""
        openai_config = self.config.get_openai_config()
        api_key = openai_config['api_key']
        
        if not api_key:
            self.logger.warning("OpenAI API key not configured")
            return
        
        try:
            self.client = OpenAI(api_key=api_key, timeout=openai_config['timeout'])
            self.logger.info("OpenAI client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
    
    def is_configured(self) -> bool:
        """Check if client is properly configured"""
        return self.client is not None
    
    def get_system_prompts(self) -> Dict[str, str]:
        """Get system prompts for different operations"""
        return {
            'shorten': "Você é um assistente útil que encurta textos preservando o significado principal e as informações-chave. Torne o texto mais conciso e claro. SEMPRE responda em português brasileiro.",
            'improve': "Você é um assistente útil que melhora textos tornando-os mais claros, bem estruturados e profissionais. Mantenha o significado original mas torne o texto mais fluido e bem escrito. SEMPRE responda em português brasileiro.",
            'informal': "Você é um assistente útil que transforma textos formais em linguagem informal e descontraída, mantendo o significado original. Use linguagem coloquial, contrações e um tom mais casual. SEMPRE responda em português brasileiro.",
            'formal': "Você é um assistente útil que transforma textos informais em linguagem formal e profissional, mantendo o significado original. Use linguagem culta, estruturas mais elaboradas e um tom respeitoso. SEMPRE responda em português brasileiro.",
            'spellcheck': "Você é um assistente útil que corrige erros ortográficos e gramaticais em textos em português brasileiro. Corrija apenas os erros, mantendo o estilo e tom original. SEMPRE responda em português brasileiro.",
            'summarize': "Você é um assistente útil que cria resumos concisos de textos longos, destacando os pontos principais e informações mais importantes. SEMPRE responda em português brasileiro.",
            'expand': "Você é um assistente útil que expande textos curtos adicionando detalhes relevantes, exemplos e explicações, mantendo a coerência e o tom original. SEMPRE responda em português brasileiro.",
            'translate_en': "Você é um assistente útil que traduz textos do português para o inglês de forma natural e fluida, mantendo o significado e tom original. SEMPRE responda em inglês.",
            'translate_pt': "Você é um assistente útil que traduz textos do inglês para o português brasileiro de forma natural e fluida, mantendo o significado e tom original. SEMPRE responda em português brasileiro.",
            'creative': "Você é um assistente criativo que reescreve textos de forma mais interessante, envolvente e criativa, mantendo o significado original mas tornando-o mais atrativo e dinâmico. SEMPRE responda em português brasileiro.",
            'technical': "Você é um assistente técnico que reescreve textos de forma mais técnica e precisa, usando terminologia adequada e estruturas mais formais, mantendo a clareza. SEMPRE responda em português brasileiro.",
            'emojify': "Você é um assistente divertido que adiciona emojis relevantes ao texto para torná-lo mais expressivo e visualmente atrativo, sem exagerar. SEMPRE responda em português brasileiro.",
            'analyze': "Você é um assistente analítico que analisa textos fornecendo insights sobre tom, estrutura, clareza e sugestões de melhoria. SEMPRE responda em português brasileiro.",
            'rewrite': "Você é um assistente que reescreve textos mantendo o significado original mas com uma abordagem diferente, mais envolvente e clara. SEMPRE responda em português brasileiro."
        }
    
    def get_user_prompts(self) -> Dict[str, str]:
        """Get user prompts for different operations"""
        return {
            'shorten': "Por favor, encurte este texto mantendo as informações essenciais. Responda em português brasileiro:\n\n{text}",
            'improve': "Por favor, melhore este texto tornando-o mais claro e bem estruturado. Responda em português brasileiro:\n\n{text}",
            'informal': "Por favor, transforme este texto em linguagem informal e descontraída. Responda em português brasileiro:\n\n{text}",
            'formal': "Por favor, transforme este texto em linguagem formal e profissional. Responda em português brasileiro:\n\n{text}",
            'spellcheck': "Por favor, corrija os erros ortográficos e gramaticais deste texto. Responda em português brasileiro:\n\n{text}",
            'summarize': "Por favor, crie um resumo conciso deste texto destacando os pontos principais. Responda em português brasileiro:\n\n{text}",
            'expand': "Por favor, expanda este texto adicionando detalhes relevantes e exemplos. Responda em português brasileiro:\n\n{text}",
            'translate_en': "Por favor, traduza este texto para o inglês de forma natural. Responda em inglês:\n\n{text}",
            'translate_pt': "Please translate this text to Brazilian Portuguese in a natural way. Responda em português brasileiro:\n\n{text}",
            'creative': "Por favor, reescreva este texto de forma mais criativa e envolvente. Responda em português brasileiro:\n\n{text}",
            'technical': "Por favor, reescreva este texto de forma mais técnica e precisa. Responda em português brasileiro:\n\n{text}",
            'emojify': "Por favor, adicione emojis relevantes a este texto para torná-lo mais expressivo. Responda em português brasileiro:\n\n{text}",
            'analyze': "Por favor, analise este texto fornecendo insights sobre tom, estrutura e clareza. Responda em português brasileiro:\n\n{text}",
            'rewrite': "Por favor, reescreva este texto de forma mais envolvente e clara. Responda em português brasileiro:\n\n{text}"
        }
    
    def process_text(self, text: str, operation_type: str) -> str:
        """Process text using OpenAI API with timeout protection"""
        if not self.is_configured():
            raise Exception("OpenAI client not configured. Please set up your API key.")
        
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            openai_config = self.config.get_openai_config()
            system_prompts = self.get_system_prompts()
            user_prompts = self.get_user_prompts()
            
            if operation_type not in system_prompts:
                raise ValueError(f"Unknown operation type: {operation_type}")
            
            self.logger.info(f"Processing text with operation: {operation_type}")
            
            # Create request with timeout
            response = self.client.chat.completions.create(
                model=openai_config['model'],
                messages=[
                    {
                        "role": "system",
                        "content": system_prompts[operation_type]
                    },
                    {
                        "role": "user",
                        "content": user_prompts[operation_type].format(text=text)
                    }
                ],
                max_tokens=openai_config['max_tokens'],
                temperature=openai_config['temperature'],
                timeout=openai_config['timeout']  # Ensure timeout is applied
            )
            
            if not response.choices or not response.choices[0].message.content:
                raise Exception("Empty response from OpenAI API")
            
            result = response.choices[0].message.content.strip()
            self.logger.info(f"Text processed successfully: {operation_type}")
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                self.logger.error(f"OpenAI API timeout: {e}")
                raise Exception("Timeout ao processar texto. Tente novamente.")
            elif "rate limit" in error_msg.lower():
                self.logger.error(f"OpenAI API rate limit: {e}")
                raise Exception("Limite de requisições excedido. Aguarde um momento e tente novamente.")
            elif "authentication" in error_msg.lower() or "unauthorized" in error_msg.lower():
                self.logger.error(f"OpenAI API authentication error: {e}")
                raise Exception("Erro de autenticação. Verifique sua chave de API.")
            else:
                self.logger.error(f"Error processing text with OpenAI: {e}")
                raise Exception(f"Falha ao processar texto: {error_msg}")
    
