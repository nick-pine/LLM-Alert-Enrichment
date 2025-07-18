# Rollback Procedures for LLM-Alert-Enrichment

This guide describes how to safely revert your deployment to a previous stable state in case of failure or issues.

---

## 1. Version Control Revert
- Use git to restore the last known good commit or branch.
- Example:
  ```sh
  git checkout main
  git reset --hard <last-known-good-commit>
  git push --force origin main
  ```

## 2. Restore Environment Configuration
- Revert `.env` or config files to their previous versions (keep backups before changes).
- Example:
  ```sh
  cp .env.backup .env
  ```

## 3. Re-deploy Application
- Restart services (FastAPI, Docker containers, etc.) using the previous codebase.
- Example:
  ```sh
  docker-compose down
  docker-compose up -d
  # or
  systemctl restart <your-service>
  ```

## 4. Restore Data (if needed)
- Restore Elasticsearch or database snapshots if data was affected.
- Example:
  ```sh
  # Elasticsearch snapshot restore
  curl -X POST "localhost:9200/_snapshot/my_backup/snapshot_1/_restore"
  ```

## 5. Verify Rollback
- Test the system to ensure it’s functioning as expected.
- Check logs, run test scripts, and confirm dashboard/UI is correct.

## 6. Document Incident
- Record what was rolled back, why, and any lessons learned for future deployments.

---

**Tip:** Always keep backups of critical files and data before making major changes or deployments.
