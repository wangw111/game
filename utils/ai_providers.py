from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json
from utils.logger import setup_logger

class AIProvider(ABC):
    """AI提供商基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(f"{name}_provider")
    
    @abstractmethod
    def send_request(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """发送请求到AI提供商"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查AI提供商是否可用"""
        pass

class OpenAIProvider(AIProvider):
    """OpenAI提供商"""
    
    def __init__(self, api_key: str, base_url: str = None):
        super().__init__("openai")
        self.api_key = api_key
        self.base_url = base_url or "https://api.openai.com/v1"
        self.client = None
        
    def _get_client(self):
        """获取OpenAI客户端"""
        if self.client is None:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
            except ImportError:
                self.logger.error("OpenAI库未安装")
                return None
        return self.client
    
    def send_request(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """发送请求到OpenAI"""
        try:
            client = self._get_client()
            if not client:
                return {'success': False, 'error': 'OpenAI客户端初始化失败'}
            
            model = kwargs.get('model', 'gpt-3.5-turbo')
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', 1000)
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                'success': True,
                'response': response.choices[0].message.content,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            }
        except Exception as e:
            self.logger.error(f"OpenAI请求失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def is_available(self) -> bool:
        """检查OpenAI是否可用"""
        return self.api_key is not None and len(self.api_key) > 0

class AnthropicProvider(AIProvider):
    """Anthropic提供商"""
    
    def __init__(self, api_key: str):
        super().__init__("anthropic")
        self.api_key = api_key
        self.client = None
        
    def _get_client(self):
        """获取Anthropic客户端"""
        if self.client is None:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                self.logger.error("Anthropic库未安装")
                return None
        return self.client
    
    def send_request(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """发送请求到Anthropic"""
        try:
            client = self._get_client()
            if not client:
                return {'success': False, 'error': 'Anthropic客户端初始化失败'}
            
            model = kwargs.get('model', 'claude-3-sonnet-20240229')
            max_tokens = kwargs.get('max_tokens', 1000)
            
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                'success': True,
                'response': response.content[0].text,
                'usage': {
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens,
                    'total_tokens': response.usage.input_tokens + response.usage.output_tokens
                }
            }
        except Exception as e:
            self.logger.error(f"Anthropic请求失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def is_available(self) -> bool:
        """检查Anthropic是否可用"""
        return self.api_key is not None and len(self.api_key) > 0

class QwenProvider(AIProvider):
    """Qwen提供商"""
    
    def __init__(self, api_key: str):
        super().__init__("qwen")
        self.api_key = api_key
        self.client = None
        
    def _get_client(self):
        """获取Qwen客户端"""
        if self.client is None:
            try:
                import dashscope
                dashscope.api_key = self.api_key
                self.client = dashscope
            except ImportError:
                self.logger.error("Dashscope库未安装")
                return None
        return self.client
    
    def send_request(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """发送请求到Qwen"""
        try:
            client = self._get_client()
            if not client:
                return {'success': False, 'error': 'Qwen客户端初始化失败'}
            
            model = kwargs.get('model', 'qwen-turbo')
            
            response = client.Generation.call(
                model=model,
                prompt=prompt
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'response': response.output.text,
                    'usage': {
                        'input_tokens': response.usage.input_tokens,
                        'output_tokens': response.usage.output_tokens,
                        'total_tokens': response.usage.total_tokens
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f"Qwen API错误: {response.code} - {response.message}"
                }
        except Exception as e:
            self.logger.error(f"Qwen请求失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def is_available(self) -> bool:
        """检查Qwen是否可用"""
        return self.api_key is not None and len(self.api_key) > 0