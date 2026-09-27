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
  "VOID_PAIR06_COHERENT_STALE_WORKTREE_CLEANUP_V1" \
  "cleanup_scope=exact_two_verified_staging_worktrees_only" \
  "force_remove=false" \
  "worktree_prune=false" \
  "submodule_update=false" \
  "gpu_observation=false" \
  "attempt_marker_creation=false" \
  "runtime_execution=false" \
  "automatic_retry=false"

hold() {
  printf 'HOLD: %s\n' "$*" >&2
  exit 1
}

registered() {
  local root="$1" target="$2"
  git -C "$root" worktree list --porcelain |
    awk -v p="$target" '$1=="worktree" && $2==p {found=1} END{exit !found}'
}

verify_exact_worktree() {
  local label="$1" root="$2" target="$3" expected="$4"

  test -e "$target" || hold "$label staging worktree missing"
  registered "$root" "$target" || hold "$label staging worktree not registered"

  actual_head="$(git -C "$target" rev-parse HEAD)"
  test "$actual_head" = "$expected" ||
    hold "$label staging worktree HEAD drift: $actual_head"

  if git -C "$target" symbolic-ref -q HEAD >/dev/null 2>&1; then
    hold "$label staging worktree is attached to a branch"
  fi

  test -z "$(git -C "$target" status --porcelain=v1 --untracked-files=all)" ||
    hold "$label staging worktree is dirty"

  printf '%s_verified=true\n' "$label"
  printf '%s_head=%s\n' "$label" "$actual_head"
  printf '%s_clean=true\n' "$label"
  printf '%s_detached=true\n' "$label"
  printf '%s_registered=true\n' "$label"
}

test "$(git -C "$repo" rev-parse --show-toplevel 2>/dev/null)" = "$repo" ||
  hold "source repository identity invalid"
test "$(git -C "$engine_repo" rev-parse --show-toplevel 2>/dev/null)" = "$engine_repo" ||
  hold "engine submodule repository identity invalid"

printf '\n=== VERIFY ATTEMPT BOUNDARY ===\n'
test -f "$old_marker" || hold "prior consumed marker missing"
actual_old_marker_sha="$(sha256sum "$old_marker" | awk '{print $1}')"
test "$actual_old_marker_sha" = "$old_marker_sha" ||
  hold "prior consumed marker drift"

for p in "$new_marker" "$new_result" "$new_closeout"; do
  test ! -e "$p" || hold "fresh coherent evidence already exists: $p"
done

if [ -e "$new_runs" ]; then
  test -d "$new_runs" || hold "coherent runs root is not a directory"
  test -z "$(find "$new_runs" -mindepth 1 -maxdepth 1 -print -quit)" ||
    hold "coherent runs root is not empty"
fi

printf '%s\n' \
  "prior_consumed_marker_exact=true" \
  "coherent_attempt_marker_absent=true" \
  "coherent_result_absent=true" \
  "coherent_closeout_absent=true" \
  "coherent_runs_root_empty=true" \
  "fresh_authorization_unconsumed=true"

printf '\n=== VERIFY STALE STAGING WORKTREES ===\n'
verify_exact_worktree source "$repo" "$source_wt" "$expected_source_commit"
verify_exact_worktree engine "$engine_repo" "$engine_wt" "$expected_engine_commit"

printf '\n=== REMOVE ENGINE STAGING WORKTREE ===\n'
git -C "$engine_repo" worktree remove "$engine_wt"
test ! -e "$engine_wt" || hold "engine staging path remained after removal"
if registered "$engine_repo" "$engine_wt"; then
  hold "engine staging worktree remained registered"
fi
printf 'engine_staging_removed=true\n'

printf '\n=== REMOVE SOURCE STAGING WORKTREE ===\n'
git -C "$repo" worktree remove "$source_wt"
test ! -e "$source_wt" || hold "source staging path remained after removal"
if registered "$repo" "$source_wt"; then
  hold "source staging worktree remained registered"
fi
printf 'source_staging_removed=true\n'

printf '\n=== POST-CLEANUP ATTEMPT BOUNDARY ===\n'
test "$(sha256sum "$old_marker" | awk '{print $1}')" = "$old_marker_sha" ||
  hold "prior consumed marker changed during cleanup"

for p in "$new_marker" "$new_result" "$new_closeout"; do
  test ! -e "$p" || hold "fresh coherent evidence appeared during cleanup: $p"
done

if [ -e "$new_runs" ]; then
  test -z "$(find "$new_runs" -mindepth 1 -maxdepth 1 -print -quit)" ||
    hold "coherent runs root changed during cleanup"
fi

printf '%s\n' \
  "prior_consumed_marker_still_exact=true" \
  "fresh_authorization_still_unconsumed=true" \
  "gpu_observation_performed=false" \
  "attempt_marker_created=false" \
  "runtime_execution_performed=false" \
  "cleanup_terminal=GREEN"
