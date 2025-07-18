# Ollama Setup Instructions

This guide explains how to set up Ollama as a local LLM provider for the enrichment pipeline.

## 1. Install Ollama
See https://ollama.com/download for platform-specific instructions.

## 2. Start Ollama
Run `ollama serve` to start the local server.

## 3. Configure Provider
Set the provider in your `.env` or config to `ollama`.

## 4. Test Connection
Use the test script or API endpoint to verify enrichment works with Ollama.
