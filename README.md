
# LEGADO

Nossa plataforma é um ambiene de jogo empolgante e competitivo projetado para desafiar os jogadores a analisarem documentos e identificarem indicadores sociais presentes neles. O objetivo é que os jogadores avaliem e identifiquem os indicadores sociais em um documento, e então comparem suas respostas com aquelas de uma Inteligência Artificial. Com base na precisão das respostas, os jogadores recebem uma pontuação correspondente.

# Tecnologias Utilizadas

## Conversão de Documentos

♻️ **Converter PDF para Imagens (jpg):** Utilizamos a biblioteca pdf2img para transformar cada página de um documento PDF em uma imagem jpg separada.

📸 **Extração de Texto de Imagens:** Empregamos o framework Tesseract, em conjunto com Python, para reconhecer o texto contido nas imagens.

## Inteligência Artificial e Processamento de Linguagem Natural (NLP)

🤖 **IA e Processamento de Linguagem Natural:** Utilizamos a inteligência artificial LLama, da Meta, em conjunto com a biblioteca da OpenAI, para gerar indicadores sociais e identificar trechos nos textos que os descrevem.

## API

🌐 **Desenvolvimento da API:** Para construir a API do projeto, utilizamos o framework FastAPI. Essa API disponibiliza os documentos, imagens e textos necessários para o frontend da aplicação.
