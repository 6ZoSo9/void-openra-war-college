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
  "VOID_PAIR06_COHERENT_STALE_WORKTREE_OBSERVER_V2" \
  "host_mutation=false" \
  "git_mutation=false" \
  "worktree_removal=false" \
  "submodule_update=false" \
  "gpu_observation=false" \
  "attempt_marker_creation=false" \
  "runtime_execution=false" \
  "automatic_retry=false"

test -d "$repo" || { echo "HOLD: source repo path missing"; exit 1; }
test "$(git -C "$repo" rev-parse --show-toplevel 2>/dev/null)" = "$repo" ||
  { echo "HOLD: source repo identity invalid"; exit 1; }

printf '\n=== ENGINE SUBMODULE CHECK ===\n'
if [ -e "$engine_repo" ]; then
  printf 'engine_path_present=true\n'
else
  printf 'engine_path_present=false\n'
fi

if engine_top="$(git -C "$engine_repo" rev-parse --show-toplevel 2>/dev/null)"; then
  printf 'engine_git_repository=true\n'
  printf 'engine_toplevel=%s\n' "$engine_top"
  engine_repo_valid=true
else
  printf 'engine_git_repository=false\n'
  printf 'engine_toplevel=UNAVAILABLE\n'
  engine_repo_valid=false
fi

printf 'submodule_git_marker_type='
if [ -d "$engine_repo/.git" ]; then
  printf 'directory\n'
elif [ -f "$engine_repo/.git" ]; then
  printf 'gitfile\n'
elif [ -e "$engine_repo/.git" ]; then
  printf 'other\n'
else
  printf 'absent\n'
fi

printf 'submodule_status='
git -C "$repo" submodule status -- OpenRA 2>/dev/null || printf 'UNAVAILABLE\n'

printf 'submodule_gitlink='
git -C "$repo" ls-tree HEAD OpenRA 2>/dev/null || printf 'UNAVAILABLE\n'

registered() {
  local root="$1" target="$2"
  if git -C "$root" worktree list --porcelain 2>/dev/null |
      awk -v p="$target" '$1=="worktree" && $2==p {found=1} END{exit !found}'; then
    printf true
  else
    printf false
  fi
}

observe_target() {
  local label="$1" root="$2" target="$3" expected="$4"
  local present=false reg=false head="ABSENT" tree="ABSENT"
  local branch="ABSENT" clean="UNKNOWN" exact=false git_worktree=false

  [ -e "$target" ] && present=true

  if git -C "$root" rev-parse --show-toplevel >/dev/null 2>&1; then
    reg="$(registered "$root" "$target")"
  else
    reg="ROOT_NOT_GIT"
  fi

  if [ "$present" = true ]; then
    if git -C "$target" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      git_worktree=true
      head="$(git -C "$target" rev-parse HEAD 2>/dev/null || printf ERROR)"
      tree="$(git -C "$target" rev-parse 'HEAD^{tree}' 2>/dev/null || printf ERROR)"
      branch="$(git -C "$target" symbolic-ref -q --short HEAD 2>/dev/null || printf DETACHED)"
      if [ -z "$(git -C "$target" status --porcelain=v1 --untracked-files=all 2>/dev/null)" ]; then
        clean=true
      else
        clean=false
      fi
      if [ "$reg" = true ] && [ "$head" = "$expected" ] &&
         [ "$branch" = DETACHED ] && [ "$clean" = true ]; then
        exact=true
      fi
    else
      head="NOT_A_GIT_WORKTREE"
      tree="NOT_A_GIT_WORKTREE"
      branch="NOT_A_GIT_WORKTREE"
      clean=false
    fi
  fi

  printf '%s_path=%s\n' "$label" "$target"
  printf '%s_present=%s\n' "$label" "$present"
  printf '%s_git_worktree=%s\n' "$label" "$git_worktree"
  printf '%s_registered=%s\n' "$label" "$reg"
  printf '%s_head=%s\n' "$label" "$head"
  printf '%s_expected_head=%s\n' "$label" "$expected"
  printf '%s_tree=%s\n' "$label" "$tree"
  printf '%s_branch=%s\n' "$label" "$branch"
  printf '%s_clean=%s\n' "$label" "$clean"
  printf '%s_exact_clean_detached_registered=%s\n' "$label" "$exact"
}

printf '\n=== SOURCE STAGING WORKTREE ===\n'
observe_target source "$repo" "$source_wt" "$expected_source_commit"

printf '\n=== ENGINE STAGING WORKTREE ===\n'
if [ "$engine_repo_valid" = true ]; then
  observe_target engine "$engine_repo" "$engine_wt" "$expected_engine_commit"
else
  printf 'engine_staging_observation=BLOCKED_CANONICAL_ENGINE_NOT_GIT\n'
  if [ -e "$engine_wt" ]; then
    printf 'engine_staging_path_present=true\n'
    if git -C "$engine_wt" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      printf 'engine_staging_git_worktree=true\n'
      printf 'engine_staging_head=%s\n' "$(git -C "$engine_wt" rev-parse HEAD 2>/dev/null || printf ERROR)"
      printf 'engine_staging_branch=%s\n' "$(git -C "$engine_wt" symbolic-ref -q --short HEAD 2>/dev/null || printf DETACHED)"
      if [ -z "$(git -C "$engine_wt" status --porcelain=v1 --untracked-files=all 2>/dev/null)" ]; then
        printf 'engine_staging_clean=true\n'
      else
        printf 'engine_staging_clean=false\n'
      fi
    else
      printf 'engine_staging_git_worktree=false\n'
    fi
  else
    printf 'engine_staging_path_present=false\n'
  fi
fi

printf '\n=== SOURCE WORKTREE REGISTRY ===\n'
git -C "$repo" worktree list --porcelain

printf '\n=== ENGINE WORKTREE REGISTRY ===\n'
if [ "$engine_repo_valid" = true ]; then
  git -C "$engine_repo" worktree list --porcelain
else
  printf 'UNAVAILABLE\n'
fi

printf '\n=== ATTEMPT EVIDENCE ===\n'
if [ -f "$old_marker" ]; then
  actual_old="$(sha256sum "$old_marker" | awk '{print $1}')"
  printf 'prior_consumed_marker_present=true\n'
  printf 'prior_consumed_marker_sha256=%s\n' "$actual_old"
  if [ "$actual_old" = "$old_marker_sha" ]; then
    printf 'prior_consumed_marker_exact=true\n'
  else
    printf 'prior_consumed_marker_exact=false\n'
  fi
else
  printf 'prior_consumed_marker_present=false\n'
  printf 'prior_consumed_marker_exact=false\n'
fi

for spec in "coherent_marker:$new_marker" "coherent_result:$new_result" "coherent_closeout:$new_closeout"; do
  label="${spec%%:*}"
  p="${spec#*:}"
  if [ -e "$p" ]; then
    printf '%s_present=true\n' "$label"
    if [ -f "$p" ]; then
      printf '%s_sha256=%s\n' "$label" "$(sha256sum "$p" | awk '{print $1}')"
    fi
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
