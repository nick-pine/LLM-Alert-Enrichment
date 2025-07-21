# Docker Setup Guide for LLM Enrichment API

## 0. Install Docker & Docker Compose

**On Ubuntu/Debian:**
```sh
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl enable --now docker
```

**Add your user to the docker group (optional, recommended):**
```sh
sudo usermod -aG docker $USER
# Log out and log back in for group changes to take effect
```

**Check Docker and Compose:**
```sh
docker --version
docker compose version  # or docker-compose --version
```

> **Note:**  
> If `docker compose` (with a space) does not work, use `docker-compose` (with a hyphen) instead.

---

## 1. Build the Docker Image
```sh
docker compose build
```

## 2. Start the API Service
```sh
docker compose up -d
```

## 3. View Running Containers
```sh
docker ps
```

## 4. Check API Logs
```sh
docker logs llm_enrichment_api
```

## 5. Restart the API Service (After Config/Code Changes)
```sh
docker compose restart llm-enrichment-api
```

## 6. Stop the API Service
```sh
docker compose down
```

## 7. Update Environment/Configuration
- Edit your `.env` file with valid API keys and connection info.
- After editing, restart the container:
  ```sh
  docker compose restart llm-enrichment-api
  ```

## 8. Test API Endpoint
- Open Swagger UI: `http://<VM-IP>:8000/docs`
- Or use `curl`:
  ```sh
  curl -X POST "http://<VM-IP>:8000/v1/enrich" -H "Content-Type: application/json" -d '{"alert": {"id": "123", "timestamp": "2025-07-17T12:00:00Z"}}'
  ```

---
Replace `<VM-IP>` with your VM’s actual IP address.
