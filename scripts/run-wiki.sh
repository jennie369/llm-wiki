#!/bin/bash
# LLM Wiki — Auto Run Script
# Called by system scheduler (Task Scheduler / cron)
# Edit WIKI_ROOT below to match your installation path

WIKI_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_FILE="$WIKI_ROOT/outputs/auto-run.log"

# Set MAT_THAN_SYNC=true to auto-sync wiki entities → Mắt Thần KG after each run
MAT_THAN_SYNC="${MAT_THAN_SYNC:-false}"

mkdir -p "$WIKI_ROOT/outputs"
echo "$(date '+%Y-%m-%d %H:%M:%S') — Starting /llm-wiki run" >> "$LOG_FILE"

cd "$WIKI_ROOT" || exit 1

claude --print --dangerously-skip-permissions "/llm-wiki run" 2>>"$LOG_FILE" | tail -20 >> "$LOG_FILE"

echo "$(date '+%Y-%m-%d %H:%M:%S') — Completed /llm-wiki run" >> "$LOG_FILE"

# Optional: sync wiki entities → Mắt Thần KG
# Enable by setting MAT_THAN_SYNC=true environment variable
# or by setting mat_than.auto_sync_on_ingest: true in config.yaml
if [ "$MAT_THAN_SYNC" = "true" ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') — Starting /llm-wiki mat_than_sync" >> "$LOG_FILE"
  claude --print --dangerously-skip-permissions "/llm-wiki mat_than_sync" 2>>"$LOG_FILE" | tail -10 >> "$LOG_FILE"
  echo "$(date '+%Y-%m-%d %H:%M:%S') — Completed mat_than_sync" >> "$LOG_FILE"
fi

echo "---" >> "$LOG_FILE"
