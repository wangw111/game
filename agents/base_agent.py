from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json
from utils.logger import setup_logger

class BaseAgent(ABC):
    """基础智能体类"""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.logger = setup_logger(f"{agent_type}_agent")
        self.memory = []
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        pass
    
    @abstractmethod
    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """处理请求"""
        pass
    
    def add_to_memory(self, interaction: Dict[str, Any]):
        """添加交互记录到内存"""
        self.memory.append(interaction)
        # 限制内存大小
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]
    
    def get_memory_context(self) -> str:
        """获取内存上下文"""
        if not self.memory:
            return ""
        
        recent_memory = self.memory[-10:]  # 最近10条记录
        memory_text = "\n".join([
            f"用户: {item.get('user_input', '')}\n助手: {item.get('assistant_response', '')}"
            for item in recent_memory
        ])
        return f"最近的交互记录:\n{memory_text}"