# Supported providers and models
The list of models has the baseline assumption that they support multimodal image inputs.

By default, the OpenAI LangChain package is installed but you can add provider-specific packages by doing `pip install langchain-{provider}`, substituting  `{provider}` with your desired one.

Here's the full list of providers as supported by LangChain: https://python.langchain.com/docs/integrations/chat/

## Table of Contents
* [Only proprietary models](#only-proprietary-models)
  * [OpenAI](#openai)
  * [Anthropic](#anthropic)
  * [Google Generative AI](#google-generative-ai)
* [Allows custom models](#allows-custom-models)
  * [AWS Bedrock](#aws-bedrock)
  * [Google Vertex AI](#google-vertex-ai)
  * [Together AI](#together-ai)
  * [HuggingFace](#huggingface)
  * [Ollama](#ollama)

## Only proprietary models

### OpenAI
* Provider info: https://platform.openai.com/docs/models
* Supported models
  * GPT-4o
  * GPT-4o mini
* LangChain package to install: `langchain-openai`
* LangChain documentation: https://python.langchain.com/docs/integrations/chat/openai/

### Anthropic
* Provider info: https://docs.anthropic.com/en/docs/about-claude/models
* Supported models
  * Claude 3.5 Sonnet
  * Claude 3 Opus
  * Claude 3 Sonnet
  * Claude 3 Haiku
* LangChain package to install: `langchain-anthropic`
* LangChain documentation: https://python.langchain.com/docs/integrations/chat/anthropic/

### Google Generative AI
* Provider info: https://ai.google.dev/gemini-api/docs/models/gemini
* Supported models
  * Gemini 1.5 Flash
  * Gemini 1.5 Flash-8B
  * Gemini 1.5 Pro
* LangChain package to install: `langchain-google-genai`
* LangChain documentation: https://python.langchain.com/docs/integrations/chat/google_generative_ai/

## Allows custom models

### AWS Bedrock
* Provider info: https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html
* Supported models:
  * Full list: https://docs.aws.amazon.com/bedrock/latest/userguide/models-features.html
* LangChain package to install: `langchain-aws`
* LangChain documentation: https://python.langchain.com/docs/integrations/chat/bedrock/

### Google Vertex AI
* Provider info: https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/overview
* Supported models:
  * Gemini 1.5 Flash
  * Gemini 1.5 Flash-8B
  * Gemini 1.5 Pro
  * More in "Model Garden": https://console.cloud.google.com/vertex-ai/model-garden
* LangChain package to install: `langchain-google-vertexai`
* LangChain documentation: https://python.langchain.com/docs/integrations/chat/google_vertex_ai_palm/

### Together AI
* Provider info: https://docs.together.ai/docs/vision-overview
* Supported models:
  * Llama 3.2 Vision 11B
  * Llama 3.2 Vision 90B
  * "Serverless" list: https://docs.together.ai/docs/serverless-models
  * "Dedicated" list: https://docs.together.ai/docs/dedicated-models
* LangChain package to install: `langchain-together`
* LangChain documentation: https://python.langchain.com/docs/integrations/chat/together/

### HuggingFace
* Provider info: https://huggingface.co/models
* Supported models:
  * Llama 3.2 Vision 11B
  * Llama 3.2 Vision 90B
  * Full list: https://huggingface.co/models
* LangChain package to install: `langchain-huggingface`
* LangChain documentation: https://python.langchain.com/docs/integrations/chat/huggingface/

### Ollama
* Provider info: https://github.com/ollama/ollama
* Supported models:
  * Llama 3.2 Vision 11B
  * Llama 3.2 Vision 90B
  * Full list: https://github.com/ollama/ollama#model-library
* LangChain package to install: `langchain-ollama`
* LangChain documentation: https://python.langchain.com/docs/integrations/chat/ollama/
