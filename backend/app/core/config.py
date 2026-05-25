from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Xiaomi MiMo
    mimo_base_url: str = "https://token-plan-sgp.xiaomimimo.com/v1"
    mimo_api_key: str
    mimo_model: str = "mimo-v2.5-pro"
    
    # Database
    database_url: str
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Agent Configuration
    max_parallel_agents: int = 12
    agent_timeout_seconds: int = 300
    max_retries: int = 3
    
    # Token Limits
    max_tokens_per_request: int = 100000
    daily_token_limit: int = 100000000
    
    # Report Generation
    report_output_dir: str = "/tmp/solaudit/reports"
    exploit_output_dir: str = "/tmp/solaudit/exploits"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
