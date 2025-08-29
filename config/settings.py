import os
from typing import Optional

class Config:
    """应用配置类"""
    
    # AI提供商配置
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL: Optional[str] = os.getenv("OPENAI_BASE_URL")
    
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    QWEN_API_KEY: Optional[str] = os.getenv("QWEN_API_KEY")
    
    # 应用配置
    APP_NAME: str = "游戏开发智能体"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Streamlit配置
    STREAMLIT_PORT: int = int(os.getenv("STREAMLIT_PORT", "8501"))
    STREAMLIT_HOST: str = os.getenv("STREAMLIT_HOST", "0.0.0.0")
    
    # 游戏配置
    DEFAULT_DIFFICULTY: str = "medium"
    MAX_PLAYERS: int = 4
    GAME_TIMEOUT: int = 300  # 5分钟
    
    @classmethod
    def validate_config(cls) -> bool:
        """验证配置是否有效"""
        # 至少需要一个AI提供商的API密钥
        if not any([cls.OPENAI_API_KEY, cls.ANTHROPIC_API_KEY, cls.QWEN_API_KEY]):
            return False
        return True