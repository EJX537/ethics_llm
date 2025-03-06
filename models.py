class Model(str):
    available_models = [
        "google/gemini-2.0-flash-001",
        "anthropic/claude-3.5-sonnet",
        "deepseek/deepseek-r1:free",
        "openai/o1-mini",
        "openai/gpt-4o-mini",
        "google/gemma-2-9b-it",
        "google/gemma-2-27b-it",
        "qwen/qwen-2.5-72b-instruct",
        "deepseek/deepseek-r1-distill-qwen-32b",
        "x-ai/grok-2-1212",
    ]

    def __new__(cls, model: str, validate: bool = True):
        instance = super().__new__(cls, model)
        if validate and model not in cls.available_models:
            raise ValueError("Invalid model name")
        return instance

    @classmethod
    def from_local(cls, model: str):
        """Create a Model instance without validating against available_models"""
        return cls(model, validate=False)

    def is_local(self):
        return self.startswith("ollama")

    @property
    def models(self):
        return self.available_models

    @classmethod
    def deepseek_r1(cls):
        return cls("deepseek/deepseek-r1")

    @classmethod
    def deepseek_r1_distill_qwen(cls):
        return cls("deepseek/deepseek-r1-distill-qwen-32b")

    @classmethod
    def gemini_2_0_flash_001(cls):
        return cls("google/gemini-2.0-flash-001")

    @classmethod
    def gemma_2_9b_it(cls):
        return cls("google/gemma-2-9b-it")

    @classmethod
    def gemma_2_27b_it(cls):
        return cls("google/gemma-2-27b-it")

    @classmethod
    def claude_3_5_sonnet(cls):
        return cls("anthropic/claude-3.5-sonnet")

    @classmethod
    def o1_mini(cls):
        return cls("openai/o1-mini")

    @classmethod
    def gpt_4o_mini(cls):
        return cls("openai/gpt-4o-mini")

    @classmethod
    def qwen_2_5_72b_instruct(cls):
        return cls("qwen/qwen-2.5-72b-instruct")

    @classmethod
    def meta_llama_3_1_70b_instruct(cls):
        return cls("meta-llama/llama-3.1-70b-instruct")

    @classmethod
    def grok_2_1212(cls):
        return cls("x-ai/grok-2-1212")
