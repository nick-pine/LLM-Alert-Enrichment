# Cost Monitoring Recommendations

## LLM/API Usage
- Enable usage and billing dashboards for your LLM provider (OpenAI, Gemini, Claude, etc.).
- Set up API usage alerts or limits in your provider’s console.
- Log each enrichment request’s token count and cost (if available in the API response).
- Periodically export and review usage/cost data.

## Example: Logging LLM API Usage

Add this to your enrichment code to log token usage and estimated cost:
```python
# After each enrichment call
usage = response.get("usage", {})
cost = estimate_cost(usage)
log_to_file({"timestamp": now(), "tokens": usage, "cost": cost})
```

## Provider Billing Dashboards

- [OpenAI Usage](https://platform.openai.com/usage)
- [Google Cloud Billing](https://console.cloud.google.com/billing)
- [Anthropic Console](https://console.anthropic.com/)

## Infrastructure Costs
- Use your cloud provider’s billing dashboard (AWS, Azure, GCP) if running in the cloud.
- Monitor resource usage (CPU, RAM, disk, network) for Docker containers or VMs.
- Set up alerts for unexpected cost or resource spikes.

## Automated Reporting
- Add a scheduled script to summarize LLM/API usage and estimated costs (daily/weekly).
- Optionally, push cost summaries to Slack, email, or a webhook for visibility.

## Tips for Optimizing Usage
- Batch alerts where possible to reduce per-request overhead.
- Use cheaper or faster models for low-priority enrichment.
- Regularly review and adjust enrichment frequency and scope.

---

Refer to this file for ongoing cost management and monitoring best practices.