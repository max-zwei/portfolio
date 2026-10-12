# Research about Large Language Models

## Research questions

- How is text represented inside an LLM?
- What is the structure of an LLM?
- How are LLMs trained?

### How is text represented inside an LLM?

Text
↓
Tokens
↓
Token IDs
↓
Embeddings

#### Tokens

Broken down text, for example:

"fine-tuning"
↓
["fine", "-", "tuning"]

"Generative"
↓
["Gener", "ative"]

#### Token IDs

Converting the word segements to a number.

#### Embeddings

Conerting the numerical Token IDs to vectors which contain learned representations that allow the neural network to work with language mathematically.

#### Source

https://medium.com/@kashafabdullah01/inside-an-llm-how-text-becomes-numbers-fdd8ea071ba4

## What is the structure of an LLM?

- transformer architecture
- attention mechanism which processes relationships between all elements in a sequence simultaneously

### Source

https://en.wikipedia.org/wiki/Large_language_model

## How are LLMs trained?

Pre-Training

- Self-supervised learning
- Tokenization -> Training -> Language Understanding -> General-purpose model

↓

Fine-tuning

- Domain-specific training

Supervised fine-tuning

- Training with I/O samples

Domain-specific fine-tuning

- Trained on domain data

Full-parameter fine-tuning

- All weights updated to new domain

↓

Low-rank adaptation

- adding trainable layers to reduce trainings costs

↓

LLM post-training and alignment

- Aligning with human preferences, safety and application-specific limits

### Source

https://www.ibm.com/think/topics/llm-training
