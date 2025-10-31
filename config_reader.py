from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    test_token: SecretStr
    bot_token: SecretStr
    admin_id: SecretStr
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    def get_token(self, mode: str = '') -> str:
        if mode == 'test':
            return self.test_token.get_secret_value()
        else:
            return self.bot_token.get_secret_value()

    def get_admin_id(self) -> int:
        return int(self.admin_id.get_secret_value())


config = Settings()