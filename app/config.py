from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str
    database_url: str = "sqlite:///./recruitment.db"
    app_env: str = "development"

    weight_required_skills: float = 0.40
    weight_experience: float = 0.25
    weight_projects: float = 0.20
    weight_education: float = 0.10
    weight_additional_skills: float = 0.05
    max_resume_file_size_mb: int = 5

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings() 