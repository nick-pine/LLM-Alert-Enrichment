# Performance Tuning Instructions

## Enrichment Pipeline
- Tune batch size if enriching in batches for best throughput vs. latency.
- Profile enrichment time per alert and adjust concurrency as needed.

## Benchmarking Enrichment Latency

Use this command to measure average enrichment time:
```sh
time python test_enrichment.py
```

## Profiling API Performance

Use FastAPI's built-in docs at `/docs` and tools like [Locust](https://locust.io/) or [wrk](https://github.com/wg/wrk) for load testing.

## Elasticsearch/OpenSearch
- Use bulk indexing for high-throughput scenarios.
- Monitor index refresh intervals and shard counts for optimal write performance.

### Elasticsearch Bulk Indexing Example
```python
from elasticsearch.helpers import bulk
bulk(es, actions)
```

## LLM Response Times
- Log and monitor LLM API latency.
- Consider using a faster model (e.g., Gemini Flash, Claude Haiku) for high-volume use.

## Resource Allocation
- Allocate sufficient CPU/RAM to Docker containers or VMs running the enrichment API.
- Monitor and scale resources as needed.

## Caching
- Optionally cache enrichment results for repeated/duplicate alerts to reduce LLM/API calls.

## Troubleshooting Slow Enrichment
- Check for network latency or LLM API throttling.
- Profile code with `cProfile` or similar tools.
- Monitor Docker/container stats with `docker stats`.

## Scaling
- For higher throughput, consider running multiple enrichment workers in parallel.
- Explore Docker Swarm or Kubernetes for horizontal scaling.

---

Refer