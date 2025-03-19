class Model(str):
    available_models = [
        "gemini/gemini-pro",
        "anthropic/claude-3-5-sonnet-20241022",
        "anthropic/claude-3-7-sonnet-20250219",
        "openai/gpt-4o-mini",
        "deepseek/deepseek-chat",
        "deepseek/deepseek-reasoner",
    ]

    def __new__(cls, model: str, validate: bool = True, api_key: str = None):
        instance = super().__new__(cls, model)
        if validate and model not in cls.available_models:
            raise ValueError("Invalid model name")

        # We can't set attributes in __new__, need to return the instance first
        return instance

    def __init__(self, model: str, validate: bool = True, api_key: str = None):
        # This will be called after __new__ creates the instance
        # Here we can set the api_key as an attribute
        self._api_key = api_key

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @classmethod
    def from_local(cls, model: str):
        """Create a Model instance without validating against available_models"""
        return cls(model, validate=False)

    def is_local(self):
        return self.startswith("ollama")

    def is_openai(self):
        return self.startswith("openai")

    def is_anthropic(self):
        return self.startswith("anthropic")

    def is_deepseek(self):
        return self.startswith("deepseek")

    @property
    def models(self):
        return self.available_models

    @classmethod
    def deepseek_chat(cls, api_key: str):
        return cls("deepseek/deepseek-chat", api_key=api_key)

    @classmethod
    def deepseek_reasoner(cls, api_key: str):
        return cls("deepseek/deepseek-reasoner", api_key=api_key)

    @classmethod
    def claude_3_5_sonnet(cls, api_key: str):
        return cls("anthropic/claude-3-5-sonnet-20241022", api_key=api_key)

    @classmethod
    def claude_3_7_sonnet(cls, api_key: str):
        return cls("anthropic/claude-3-7-sonnet-20250219", api_key=api_key)

    @classmethod
    def gpt_4o_mini(cls, api_key: str):
        return cls("openai/gpt-4o-mini", api_key=api_key)
