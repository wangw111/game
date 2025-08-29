from typing import Dict, Any, Optional, List
from config.settings import Config
from utils.ai_providers import OpenAIProvider, AnthropicProvider, QwenProvider
from utils.logger import setup_logger

class AIProviderManager:
    """AI提供商管理器"""
    
    def __init__(self):
        self.logger = setup_logger("ai_provider_manager")
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """初始化AI提供商"""
        # 初始化OpenAI提供商
        if Config.OPENAI_API_KEY:
            self.providers['openai'] = OpenAIProvider(
                Config.OPENAI_API_KEY, 
                Config.OPENAI_BASE_URL
            )
            self.logger.info("OpenAI提供商已初始化")
        
        # 初始化Anthropic提供商
        if Config.ANTHROPIC_API_KEY:
            self.providers['anthropic'] = AnthropicProvider(Config.ANTHROPIC_API_KEY)
            self.logger.info("Anthropic提供商已初始化")
        
        # 初始化Qwen提供商
        if Config.QWEN_API_KEY:
            self.providers['qwen'] = QwenProvider(Config.QWEN_API_KEY)
            self.logger.info("Qwen提供商已初始化")
    
    def get_available_providers(self) -> List[str]:
        """获取可用的AI提供商列表"""
        return [name for name, provider in self.providers.items() if provider.is_available()]
    
    def send_request(self, provider_name: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """发送请求到指定的AI提供商"""
        if provider_name not in self.providers:
            return {'success': False, 'error': f'未找到提供商: {provider_name}'}
        
        provider = self.providers[provider_name]
        if not provider.is_available():
            return {'success': False, 'error': f'提供商不可用: {provider_name}'}
        
        return provider.send_request(prompt, **kwargs)
    
    def send_request_to_best_provider(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """发送请求到最佳可用的AI提供商"""
        available_providers = self.get_available_providers()
        
        if not available_providers:
            return {'success': False, 'error': '没有可用的AI提供商'}
        
        # 按优先级选择提供商
        priority_order = ['openai', 'anthropic', 'qwen']
        
        for provider_name in priority_order:
            if provider_name in available_providers:
                self.logger.info(f"使用AI提供商: {provider_name}")
                return self.send_request(provider_name, prompt, **kwargs)
        
        # 如果优先级提供商都不可用，使用第一个可用的
        fallback_provider = available_providers[0]
        self.logger.info(f"使用备用AI提供商: {fallback_provider}")
        return self.send_request(fallback_provider, prompt, **kwargs)
    
    def get_provider_status(self) -> Dict[str, bool]:
        """获取所有提供商的状态"""
        return {
            name: provider.is_available() 
            for name, provider in self.providers.items()
        }