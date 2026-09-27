#!/usr/bin/env bash
set -euo pipefail

arm_root="$HOME/dev/void-war-college-execution/v8-generation2/generation2/pair-06/baseline"
claims_root="$arm_root/claims-v1"

marker="$claims_root/pair06-v8-combat-priority-coherent-baseline-game-attempt-v1.json"
result="$claims_root/pair06-v8-combat-priority-coherent-baseline-game-result-v1.json"
closeout="$claims_root/pair06-v8-combat-priority-coherent-baseline-game-closeout-v1.json"
runs_root="$arm_root/runs-combat-priority-coherent-v1"

source_wt="$arm_root/frozen-source"
engine_wt="$arm_root/engine"

printf '%s\n' \
  "VOID_PAIR06_COHERENT_CONSUMED_ATTEMPT_OBSERVER_V1" \
  "host_mutation=false" \
  "git_mutation=false" \
  "worktree_removal=false" \
  "gpu_observation=false" \
  "runtime_execution=false" \
  "automatic_retry=false"

printf '\n=== COHERENT EVIDENCE ===\n'
if [ -f "$marker" ]; then
  printf 'coherent_attempt_marker_present=true\n'
  printf 'coherent_attempt_marker_sha256=%s\n' "$(sha256sum "$marker" | awk '{print $1}')"
  printf 'coherent_attempt_marker_bytes=%s\n' "$(wc -c < "$marker" | tr -d ' ')"
else
  printf 'coherent_attempt_marker_present=false\n'
fi

for spec in "result:$result" "closeout:$closeout"; do
  label="${spec%%:*}"
  p="${spec#*:}"
  if [ -f "$p" ]; then
    printf 'coherent_%s_present=true\n' "$label"
    printf 'coherent_%s_sha256=%s\n' "$label" "$(sha256sum "$p" | awk '{print $1}')"
    printf 'coherent_%s_bytes=%s\n' "$label" "$(wc -c < "$p" | tr -d ' ')"
  else
    printf 'coherent_%s_present=false\n' "$label"
  fi
done

printf '\n=== COHERENT RUNS ===\n'
if [ -d "$runs_root" ]; then
  printf 'coherent_runs_root_present=true\n'
  count="$(find "$runs_root" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
  printf 'coherent_run_directory_count=%s\n' "$count"
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    printf 'coherent_run_id=%s\n' "$(basename "$p")"
  done < <(find "$runs_root" -mindepth 1 -maxdepth 1 -type d -print | sort)
else
  printf 'coherent_runs_root_present=false\n'
  printf 'coherent_run_directory_count=0\n'
fi

printf '\n=== STAGING WORKTREES AFTER FAILURE ===\n'
for spec in "source:$source_wt" "engine:$engine_wt"; do
  label="${spec%%:*}"
  p="${spec#*:}"
  if [ -e "$p" ]; then
    printf '%s_staging_present=true\n' "$label"
    if git -C "$p" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      printf '%s_staging_head=%s\n' "$label" "$(git -C "$p" rev-parse HEAD 2>/dev/null || printf ERROR)"
      printf '%s_staging_branch=%s\n' "$label" "$(git -C "$p" symbolic-ref -q --short HEAD 2>/dev/null || printf DETACHED)"
      if [ -z "$(git -C "$p" status --porcelain=v1 --untracked-files=all 2>/dev/null)" ]; then
        printf '%s_staging_clean=true\n' "$label"
      else
        printf '%s_staging_clean=false\n' "$label"
      fi
    else
      printf '%s_staging_git_worktree=false\n' "$label"
    fi
  else
    printf '%s_staging_present=false\n' "$label"
  fi
done

printf '\nobserver_terminal=GREEN\n'
