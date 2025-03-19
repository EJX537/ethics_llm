# Ethics by LLM

A tool for evaluating and analyzing ethical considerations in AI responses across different LLM providers.

⚠️⚠️ Website was written swiftly and untested ⚠️⚠️
Hosting on Github does not support subpage routing correctly, IF I ever work on this again, I will host it on Cloudflare.

## Overview

Ethics by LLM allows you to compare responses from various large language models (LLMs) on ethically complex questions. This tool helps researchers, developers, and ethicists understand how different models approach challenging ethical scenarios.

## Collected Data
Turso read-only
```
TURSO_DATABASE_URL="libsql://llm-responses-ejx537.turso.io"
TURSO_AUTH_TOKEN="eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicm8iLCJpYXQiOjE3NDI0MDk5MTgsImlkIjoiZTFiNDBhYzQtZjBkOS00N2U4LTgyOWUtYzEyYjYwZjlkZmNmIn0.VdEi0HFjh4dnrbBV3ubbBbCgSZiegCijZNwxXDgD3zlH_OwjKrBRMGUSLYWSc2z42dielNV6-c2HCwldkgqSCw"
```

## Features

- Query multiple LLM providers simultaneously (Anthropic, OpenAI, DeepSeek)
- Compare responses side-by-side
- Store historical queries and responses for analysis
- Visualize trends in ethical reasoning across models

## Configuration

Create a `.env` file in the root directory with your API keys:

```
TURSO_DATABASE_URL="your_turso_database_url"
TURSO_AUTH_TOKEN="your_turso_auth_token"
ANTHROPIC_API_KEY="your_anthropic_api_key" 
OPENAI_API_KEY="your_openai_api_key"
DEEPSEEK_API_KEY="your_deepseek_api_key"
```

⚠️ **Important:** Never commit your `.env` file to version control. Make sure it's included in your `.gitignore`.

## Setting Up Your API Keys

### Anthropic (Claude)
1. Create an account at [anthropic.com](https://www.anthropic.com/)
2. Navigate to the API section and generate a new API key
3. Copy the key starting with `sk-ant-api...`

### OpenAI
1. Create an account at [openai.com](https://www.openai.com/)
2. Go to API settings and create a new API key
3. Copy the key starting with `sk-...`

### DeepSeek
1. Register at [deepseek.ai](https://www.deepseek.ai/)
2. Navigate to your account settings to create an API key
3. Copy the key starting with `sk-...`

### Turso Database
1. Create an account at [turso.tech](https://turso.tech/)
2. Create a new database and get your URL and auth token
3. Copy both values to your `.env` file

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all the LLM providers for their APIs
- Contributors and researchers in the field of AI ethics
