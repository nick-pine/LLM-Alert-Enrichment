# Ollama Setup Guide

This guide helps you install Ollama and pull recommended models for local LLM inference.

## 1. Install Ollama
- Visit [https://ollama.com/download](https://ollama.com/download) and download the installer for your operating system.
- Follow the installation instructions for your platform (Windows, macOS, Linux).

## 2. Start Ollama
- After installation, start the Ollama service:
  - On Windows: Launch Ollama from the Start Menu.
  - On macOS/Linux: Run `ollama serve` in your terminal.

## 3. Pull Recommended Models
Open a terminal and run the following commands:

```sh
ollama pull phi3-medium
ollama pull phi3-mini
ollama pull llama3:8b
ollama pull mixtral:8x7b
ollama pull command-r-plus
```

## 4. Test Model Availability
To verify the models are available, run:

```sh
ollama list
```

You should see `phi3-medium`, `phi3-mini`, `llama3:8b`, `mixtral:8x7b`, and `command-r-plus` listed.

## 5. Troubleshooting
- If you encounter issues, visit the [Ollama documentation](https://ollama.com/docs) or check your system requirements.
- Ensure the Ollama service is running before using the LLM enrichment project.

---

**Note:** Ollama must be running for the enrichment project to use local models.
