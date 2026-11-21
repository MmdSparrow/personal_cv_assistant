<h1 align="center">Personal CV Assistant</h1>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.x-blue.svg">
    <img src="https://img.shields.io/badge/Angular-Frontend-red.svg">
    <img src="https://img.shields.io/badge/RAG-Retrieval%20Augmented%20Generation-orange.svg">
    <img src="https://img.shields.io/badge/ChromaDB-Vector%20Database-green.svg">
    <img src="https://img.shields.io/badge/Groq-LLM%20Provider-purple.svg">
    <img src="https://img.shields.io/badge/License-MIT-red.svg">
</p>

An AI-powered **Personal CV Assistant** built with **Python**, **Angular**, and **Retrieval-Augmented Generation (RAG)**. The system allows visitors to interact with my professional background, technical skills, education, and projects through a conversational AI interface.

It processes personal documents, generates semantic embeddings, retrieves relevant information using vector search, and generates context-aware responses using Large Language Models (LLMs).

> **Current Status:** The project supports PDF, JSON, and plain-text document ingestion, semantic embedding generation, document indexing, and LLM integration. Groq is the default LLM provider, with Google Gemini also supported.

## Overview

The system follows the following workflow:

1. **Document Ingestion** – Extract information from PDF, JSON, and plain-text documents.
2. **Embedding Generation** – Convert document chunks into vector representations.
3. **Document Indexing** – Index document embeddings in a vector database for efficient retrieval.
4. **Semantic Retrieval** – Find relevant information based on the user's query.
5. **LLM Integration** – Send retrieved context to an LLM to generate relevant responses.
6. **Interactive Chat** – Allow visitors to explore my professional background through a conversational interface.

## Current Features

### 🔹 Document Ingestion

- PDF document processing.
- JSON document processing.
- Plain-text document processing.
- Modular ingestion architecture.

### 🔹 Embedding Generation

- Semantic text embedding (
  - Default model: `BAAI/bge-small-en-v1.5`
- Configurable embedding model.
- Local embedding generation.

### 🔹 Document Indexing

- Centralized document indexing pipeline.
- Vector-based document representation.
- Semantic retrieval support.

### 🔹 LLM Integration

- Multiple LLM provider support.
- Groq API integration.
  - Default model: `openai/gpt-oss-20b`
- Google Gemini API integration.
  - Default model: `gemini-3.8-flash`
- Modular LLM client architecture.

### 🔹 Interactive Chat Interface

- Angular-based chat interface.
- Conversational interaction with personal documents.
- API-based communication with the backend.
- Responsive user experience.

## Technologies Used

- **Python** – Backend development and RAG pipeline implementation.
- **Angular** – Frontend and interactive chat interface.
- **ChromaDB** – Vector storage and semantic retrieval.
- **Sentence Transformers** – Semantic embedding generation.
- **BAAI/bge-small-en-v1.5** – Default embedding model.
- **Groq** – Default LLM provider.
- **Google Gemini** – Alternative LLM provider.

## Future Improvements

- 🔍 Hybrid search combining semantic search and keyword-based retrieval.
- 🎯 Retrieval reranking for improved relevance.
- 🧠 Context-aware conversational memory.
- 🔄 Query rewriting and optimization.
- 📊 Retrieval evaluation and performance optimization.
- 📂 Advanced document metadata filtering.
- ⚡ Improved indexing and retrieval efficiency.

## Future Vision

The goal of this project is to build an intelligent personal assistant that serves as an interactive representation of my professional background.

By combining modular document processing, semantic retrieval, and multiple LLM providers, the system provides a natural and efficient way for visitors to explore my technical skills, professional experience, education, and projects through conversation.