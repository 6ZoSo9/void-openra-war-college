#!/usr/bin/env bash
set -euo pipefail

repo="$HOME/dev/openra-rl-war-college"
engine_repo="$repo/OpenRA"
arm_root="$HOME/dev/void-war-college-execution/v8-generation2/generation2/pair-06/baseline"
source_wt="$arm_root/frozen-source"
engine_wt="$arm_root/engine"

expected_source_commit="973802ef0a614e5afa782ff20e231e18966ae3e5"
expected_engine_commit="1607a7a6501d42a47638393ecef8b22831064932"

old_marker="$arm_root/claims-v1/pair06-v8-combat-priority-baseline-game-attempt-v1.json"
old_marker_sha="90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"

new_marker="$arm_root/claims-v1/pair06-v8-combat-priority-coherent-baseline-game-attempt-v1.json"
new_result="$arm_root/claims-v1/pair06-v8-combat-priority-coherent-baseline-game-result-v1.json"
new_closeout="$arm_root/claims-v1/pair06-v8-combat-priority-coherent-baseline-game-closeout-v1.json"
new_runs="$arm_root/runs-combat-priority-coherent-v1"

printf '%s\n' \
  "VOID_PAIR06_COHERENT_STALE_WORKTREE_OBSERVER_V1" \
  "host_mutation=false" \
  "git_mutation=false" \
  "worktree_removal=false" \
  "gpu_observation=false" \
  "attempt_marker_creation=false" \
  "runtime_execution=false" \
  "automatic_retry=false"

test -d "$repo/.git" || { echo "HOLD: source repo missing"; exit 1; }
test -d "$engine_repo/.git" || { echo "HOLD: engine repo missing"; exit 1; }

registered() {
  local root="$1" target="$2"
  if git -C "$root" worktree list --porcelain |
      awk -v p="$target" '$1=="worktree" && $2==p {found=1} END{exit !found}'; then
    printf true
  else
    printf false
  fi
}

observe_target() {
  local label="$1" root="$2" target="$3" expected="$4"
  local present=false reg=false head="ABSENT" tree="ABSENT" branch="ABSENT" clean="UNKNOWN" exact=false
  [ -e "$target" ] && present=true
  reg="$(registered "$root" "$target")"

  if [ "$present" = true ]; then
    if git -C "$target" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      head="$(git -C "$target" rev-parse HEAD 2>/dev/null || printf ERROR)"
      tree="$(git -C "$target" rev-parse 'HEAD^{tree}' 2>/dev/null || printf ERROR)"
      branch="$(git -C "$target" symbolic-ref -q --short HEAD 2>/dev/null || printf DETACHED)"
      if [ -z "$(git -C "$target" status --porcelain=v1 --untracked-files=all 2>/dev/null)" ]; then
        clean=true
      else
        clean=false
      fi
      if [ "$reg" = true ] && [ "$head" = "$expected" ] && [ "$branch" = DETACHED ] && [ "$clean" = true ]; then
        exact=true
      fi
    else
      head="NOT_A_GIT_WORKTREE"
      tree="NOT_A_GIT_WORKTREE"
      branch="NOT_A_GIT_WORKTREE"
      clean=false
    fi
  fi

  printf '%s_%s=%s\n' "$label" "path" "$target"
  printf '%s_%s=%s\n' "$label" "present" "$present"
  printf '%s_%s=%s\n' "$label" "registered" "$reg"
  printf '%s_%s=%s\n' "$label" "head" "$head"
  printf '%s_%s=%s\n' "$label" "expected_head" "$expected"
  printf '%s_%s=%s\n' "$label" "tree" "$tree"
  printf '%s_%s=%s\n' "$label" "branch" "$branch"
  printf '%s_%s=%s\n' "$label" "clean" "$clean"
  printf '%s_%s=%s\n' "$label" "exact_clean_detached_registered" "$exact"
}

printf '\n=== SOURCE WORKTREE ===\n'
observe_target source "$repo" "$source_wt" "$expected_source_commit"

printf '\n=== ENGINE WORKTREE ===\n'
observe_target engine "$engine_repo" "$engine_wt" "$expected_engine_commit"

printf '\n=== SOURCE REGISTRY ===\n'
git -C "$repo" worktree list --porcelain

printf '\n=== ENGINE REGISTRY ===\n'
git -C "$engine_repo" worktree list --porcelain

printf '\n=== ATTEMPT EVIDENCE ===\n'
if [ -f "$old_marker" ]; then
  actual_old="$(sha256sum "$old_marker" | awk '{print $1}')"
  printf 'prior_consumed_marker_present=true\n'
  printf 'prior_consumed_marker_sha256=%s\n' "$actual_old"
  [ "$actual_old" = "$old_marker_sha" ] &&
    printf 'prior_consumed_marker_exact=true\n' ||
    printf 'prior_consumed_marker_exact=false\n'
else
  printf 'prior_consumed_marker_present=false\n'
  printf 'prior_consumed_marker_exact=false\n'
fi

for spec in "coherent_marker:$new_marker" "coherent_result:$new_result" "coherent_closeout:$new_closeout"; do
  label="${spec%%:*}"
  p="${spec#*:}"
  if [ -e "$p" ]; then
    printf '%s_present=true\n' "$label"
    [ -f "$p" ] && printf '%s_sha256=%s\n' "$label" "$(sha256sum "$p" | awk '{print $1}')"
  else
    printf '%s_present=false\n' "$label"
  fi
done

if [ -e "$new_runs" ]; then
  printf 'coherent_runs_root_present=true\n'
  printf 'coherent_runs_entry_count=%s\n' "$(find "$new_runs" -mindepth 1 -maxdepth 1 -printf '.' 2>/dev/null | wc -c)"
else
  printf 'coherent_runs_root_present=false\n'
  printf 'coherent_runs_entry_count=0\n'
fi

printf '\nobserver_terminal=GREEN\n'
