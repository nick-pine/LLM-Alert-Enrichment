# Elasticsearch Self-Signed Certificate Setup for Development

This guide will help you generate a self-signed certificate for your local Elasticsearch instance and configure your Python enrichment script to trust it.

---

## 1. Generate a Self-Signed Certificate (on your Elasticsearch server)

Run these commands on the server where Elasticsearch is running:

```sh
# Create a directory for certs
sudo mkdir -p /etc/elasticsearch/certs
cd /etc/elasticsearch/certs

# Generate a CA (Certificate Authority)
sudo openssl genrsa -out elastic-stack-ca.key 4096
sudo openssl req -x509 -new -nodes -key elastic-stack-ca.key -sha256 -days 3650 -out elastic-stack-ca.crt -subj "/CN=Elastic-Stack-CA"

# Generate a certificate for Elasticsearch
sudo openssl genrsa -out elasticsearch.key 4096
sudo openssl req -new -key elasticsearch.key -out elasticsearch.csr -subj "/CN=localhost"
sudo openssl x509 -req -in elasticsearch.csr -CA elastic-stack-ca.crt -CAkey elastic-stack-ca.key -CAcreateserial -out elasticsearch.crt -days 3650 -sha256

# Set permissions
sudo chown elasticsearch:elasticsearch *.key *.crt
sudo chmod 600 *.key
sudo chmod 644 *.crt
```

---

## 2. Configure Elasticsearch to Use the Certificate

Edit `/etc/elasticsearch/elasticsearch.yml` and add:

```
xpack.security.enabled: true
xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.key: /etc/elasticsearch/certs/elasticsearch.key
xpack.security.http.ssl.certificate: /etc/elasticsearch/certs/elasticsearch.crt
xpack.security.http.ssl.certificate_authorities: [ "/etc/elasticsearch/certs/elastic-stack-ca.crt" ]
```

Restart Elasticsearch:
```sh
sudo systemctl restart elasticsearch
```

---

## 3. Copy the CA Certificate to Your Development Machine

On your dev machine:
```sh
scp user@elasticsearch-server:/etc/elasticsearch/certs/elastic-stack-ca.crt ./ca.crt
```

---

## 4. Update Your .env File

Add this line (or update if present):
```
ELASTIC_CA_BUNDLE=/path/to/ca.crt
```

---

## 5. Update Your Python Code to Use the CA Bundle

In your Elasticsearch client code (e.g., in `llm_enrichment.py`):

```python
from elasticsearch import Elasticsearch
import os

ca_bundle = os.getenv("ELASTIC_CA_BUNDLE")
es = Elasticsearch(
    os.getenv("ELASTICSEARCH_URL"),
    http_auth=(os.getenv("ELASTIC_USER"), os.getenv("ELASTIC_PASS")),
    ca_certs=ca_bundle  # Enables certificate verification
)
```

---

## 6. Test the Connection

Run your script as usual. The InsecureRequestWarning should be gone, and your connection will be secure.

---

## Notes
- For production, use a certificate from a trusted CA.
- Never share your private keys.
- If you use Docker, mount the CA cert into the container and set the path in `.env` accordingly.
