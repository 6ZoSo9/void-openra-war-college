#!/usr/bin/env bash
set -euo pipefail

repo="$HOME/dev/openra-rl-war-college"
engine_repo="$repo/OpenRA"
canonical_url="https://github.com/6ZoSo9/void-openra-war-college.git"

authorized_head="d8b16f1c23a74803ac4ace94045fed147c3c69fe"
acceptance_merge="1dfbed07a95b2a5cf60eed8af49e8a3355810f17"

request_sha256="de3d60e2395192a976f14fe055d27981a9c7dd31560e67eda0fbe08f6b8f917c"
request_bytes="5670"
authorization_text_sha256="6cfe4dd78c02a55c2499163b01de6f5714e0b8573100b7a888177ff1a568d139"
authorization_text_bytes="533"

invocation_path="openra_env/learning/abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2.py"
invocation_blob="9b5db375d5ae8e133de73603ffd3745352789018"
invocation_sha256="309ea6f83d7129cb1dcccd61d1451c604098860154780e545ac8139f56a1403c"

request_review_path="openra_env/learning/abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_source_binding_review_generation2.py"
request_review_blob="18e69f90b4020a775de6bb9f1b7b5346e4e531fd"
request_review_sha256="5b97f48b1ad6220bd615194b55f74f17865090c251ae08a257906678e754f862"

acceptance_path="openra_env/learning/abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_preclaim_gpu_execution_authorization_acceptance_generation2.py"
acceptance_blob="59e151aca7af20cf53b3e0a908e23d2a0c915418"
acceptance_sha256="4b2cf1b3423fe62634518e54765e67c1272a3b9765ea941ed3c540288b482c3f"

acceptance_test_path="tests/test_abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_preclaim_gpu_execution_authorization_acceptance_generation2.py"
acceptance_test_blob="95ed79dc48dc60b154c5ed0073b76c5a6f3e34ba"
acceptance_test_sha256="58d79b2d12d175dba1f558d7a261564aa46dfd67c159b15e184cd1ad538ecad8"

arm_root="$HOME/dev/void-war-college-execution/v8-generation2/generation2/pair-06/baseline"
claims_root="$arm_root/claims-v1"

prior_marker="$claims_root/pair06-v8-combat-priority-coherent-baseline-game-attempt-v1.json"
prior_result="$claims_root/pair06-v8-combat-priority-coherent-baseline-game-result-v1.json"
prior_closeout="$claims_root/pair06-v8-combat-priority-coherent-baseline-game-closeout-v1.json"
prior_marker_sha256="bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
prior_runs_root="$arm_root/runs-combat-priority-coherent-v1"
prior_failed_run="warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"

new_marker="$claims_root/pair06-v8-combat-priority-coherent-v2-baseline-game-attempt-v1.json"
new_result="$claims_root/pair06-v8-combat-priority-coherent-v2-baseline-game-result-v1.json"
new_closeout="$claims_root/pair06-v8-combat-priority-coherent-v2-baseline-game-closeout-v1.json"
new_runs_root="$arm_root/runs-combat-priority-coherent-v2-v1"

source_staging="$arm_root/frozen-source"
engine_staging="$arm_root/engine"
expected_source_commit="973802ef0a614e5afa782ff20e231e18966ae3e5"
expected_engine_commit="1607a7a6501d42a47638393ecef8b22831064932"

v8_python="$HOME/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/venv/bin/python3.12"

authorization_text='I authorize exactly one fresh pair-06 V8 V2-coherent combat-priority baseline execution described by request SHA-256 `de3d60e2395192a976f14fe055d27981a9c7dd31560e67eda0fbe08f6b8f917c` on canonical War College main `d8b16f1c23a74803ac4ace94045fed147c3c69fe`, including activation of `pair06-v8-combat-action-priority-envelope-v1`, with a maximum of one attempt and zero automatic retries. The prior consumed attempt marker `bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885` and prior authorization remain non-reusable.'

printf '%s\n' \
  "VOID_WAR_COLLEGE_PAIR06_V8_COMBAT_PRIORITY_COHERENT_V2_PRECISION_EXECUTE_ONCE_V1" \
  "repository=$repo" \
  "canonical_repository=$canonical_url" \
  "authorized_head=$authorized_head" \
  "acceptance_merge=$acceptance_merge" \
  "authorized_request_sha256=$request_sha256" \
  "authorized_request_bytes=$request_bytes" \
  "authorization_text_sha256=$authorization_text_sha256" \
  "authorization_text_bytes=$authorization_text_bytes" \
  "pair_slot=6" \
  "arm=baseline" \
  "doctrine=FEINTER" \
  "seed=208354846" \
  "contract_coherence_repair_v2=true" \
  "maximum_attempts=1" \
  "automatic_retries=0" \
  "fresh_preclaim_gpu_required=true" \
  "zero_foreign_cuda0_compute_processes_required=true" \
  "minimum_cuda0_free_memory_fraction=9/10" \
  "prior_consumed_attempt_marker_sha256=$prior_marker_sha256" \
  "prior_consumed_attempt_reusable=false" \
  "prior_authorization_reusable=false" \
  "preexecution_staging_cleanup=bounded_exact_only" \
  "candidate_execution_authorized=false" \
  "pair15_execution_authorized=false" \
  "pair03_replay_authorized=false" \
  "pair09_replay_authorized=false" \
  "training_authorized=false" \
  "weights_update_authorized=false" \
  "automatic_policy_promotion_authorized=false" \
  "deployment_authorized=false" \
  "void_chain_mutation_authorized=false" \
  "wallet_or_funds_action_authorized=false" \
  "remote_config_mutation=false" \
  "git_push=false"

hold() {
  printf 'HOLD: %s\n' "$*" >&2
  exit 1
}

test -d "$repo/.git" || hold "War College repository missing: $repo"
test -x "$v8_python" || hold "exact V8 Python missing: $v8_python"

cd "$repo"

test "$(git symbolic-ref -q HEAD)" = "refs/heads/main" ||
  hold "repository must begin on local main"

git diff --quiet || hold "tracked working tree changes present"
git diff --cached --quiet || hold "staged tracked changes present"

test "$(git -C "$engine_repo" rev-parse --show-toplevel 2>/dev/null)" = "$engine_repo" ||
  hold "OpenRA submodule repository identity invalid"

printf '\n=== LOCAL REMOTE OBSERVATION ===\n'
origin_url="$(git remote get-url origin 2>/dev/null || true)"
printf 'local_origin_url=%s\n' "${origin_url:-UNSET}"
printf 'local_origin_is_authority=false\n'

printf '\n=== FETCH CANONICAL WAR COLLEGE MAIN ===\n'
git fetch --quiet --no-tags "$canonical_url" \
  "+refs/heads/main:refs/void-exec/coherent-v2-canonical-main"

canonical_main="$(git rev-parse refs/void-exec/coherent-v2-canonical-main)"
printf 'canonical_main=%s\n' "$canonical_main"
test "$canonical_main" = "$acceptance_merge" ||
  hold "canonical War College main moved after fresh V2 authorization acceptance"

git cat-file -e "${authorized_head}^{commit}"
git cat-file -e "${acceptance_merge}^{commit}"

read -r merge_sha first_parent second_parent extra_parent <<EOF
$(git rev-list --parents -n1 "$acceptance_merge")
EOF
test "$merge_sha" = "$acceptance_merge" || hold "acceptance merge identity drift"
test "$first_parent" = "$authorized_head" ||
  hold "acceptance merge first parent is not the authorized head"
test -n "${second_parent:-}" && test -z "${extra_parent:-}" ||
  hold "acceptance commit is not an exact two-parent merge"

printf '\n=== PIN REVIEWED V2 AUTHORIZATION LINEAGE ===\n'
test "$(git rev-parse "$acceptance_merge:$acceptance_path")" = "$acceptance_blob" ||
  hold "V2 authorization acceptance blob drift"
test "$(git show "$acceptance_merge:$acceptance_path" | sha256sum | awk '{print $1}')" = "$acceptance_sha256" ||
  hold "V2 authorization acceptance source SHA drift"

test "$(git rev-parse "$acceptance_merge:$acceptance_test_path")" = "$acceptance_test_blob" ||
  hold "V2 authorization acceptance test blob drift"
test "$(git show "$acceptance_merge:$acceptance_test_path" | sha256sum | awk '{print $1}')" = "$acceptance_test_sha256" ||
  hold "V2 authorization acceptance test SHA drift"

test "$(git rev-parse "$authorized_head:$request_review_path")" = "$request_review_blob" ||
  hold "V2 request review blob drift"
test "$(git show "$authorized_head:$request_review_path" | sha256sum | awk '{print $1}')" = "$request_review_sha256" ||
  hold "V2 request review source SHA drift"

test "$(git rev-parse "$authorized_head:$invocation_path")" = "$invocation_blob" ||
  hold "V2 coherent invocation blob drift"
test "$(git show "$authorized_head:$invocation_path" | sha256sum | awk '{print $1}')" = "$invocation_sha256" ||
  hold "V2 coherent invocation source SHA drift"

actual_auth_text_sha="$(
  printf '%s' "$authorization_text" | sha256sum | awk '{print $1}'
)"
actual_auth_text_bytes="$(
  printf '%s' "$authorization_text" | wc -c | tr -d ' '
)"
test "$actual_auth_text_sha" = "$authorization_text_sha256" ||
  hold "fresh V2 authorization text SHA drift"
test "$actual_auth_text_bytes" = "$authorization_text_bytes" ||
  hold "fresh V2 authorization text byte-length drift"

printf '%s\n' \
  "canonical_acceptance_bound=true" \
  "authorization_acceptance_source_bound=true" \
  "authorization_acceptance_test_bound=true" \
  "request_review_source_bound=true" \
  "coherent_v2_invocation_source_bound=true" \
  "fresh_v2_authorization_text_bound=true"

printf '\n=== PROVE PRIOR V1 COHERENT ATTEMPT REMAINS SEALED ===\n'
test -f "$prior_marker" || hold "prior V1 coherent consumed marker missing"
actual_prior_marker_sha="$(sha256sum "$prior_marker" | awk '{print $1}')"
printf 'prior_consumed_marker_sha256=%s\n' "$actual_prior_marker_sha"
test "$actual_prior_marker_sha" = "$prior_marker_sha256" ||
  hold "prior V1 coherent consumed marker drift"

test ! -e "$prior_result" ||
  hold "unexpected prior V1 coherent failed result exists"
test ! -e "$prior_closeout" ||
  hold "unexpected prior V1 coherent failed closeout exists"
test -d "$prior_runs_root/$prior_failed_run" ||
  hold "preserved prior V1 coherent failed run missing"

printf '%s\n' \
  "prior_consumed_attempt_reusable=false" \
  "prior_authorization_reusable=false" \
  "prior_failed_result_absent=true" \
  "prior_failed_closeout_absent=true" \
  "prior_failed_run_preserved=true"

printf '\n=== PROVE FRESH V2 COHERENT NAMESPACE ===\n'
for p in "$new_marker" "$new_result" "$new_closeout"; do
  if [ -e "$p" ]; then
    printf 'existing_v2_coherent_evidence_path=%s\n' "$p"
    hold "fresh V2 coherent evidence already exists; do not execute"
  fi
done

if [ -e "$new_runs_root" ]; then
  test -d "$new_runs_root" ||
    hold "V2 coherent runs root exists but is not a directory"
  test -z "$(find "$new_runs_root" -mindepth 1 -maxdepth 1 -print -quit)" ||
    hold "V2 coherent runs root is not empty"
fi

printf '%s\n' \
  "coherent_v2_attempt_marker_absent=true" \
  "coherent_v2_result_absent=true" \
  "coherent_v2_closeout_absent=true" \
  "coherent_v2_runs_root_fresh=true"

registered_worktree() {
  local root="$1"
  local target="$2"
  git -C "$root" worktree list --porcelain |
    awk -v p="$target" '$1=="worktree" && $2==p {found=1} END{exit !found}'
}

cleanup_exact_staging_worktree() {
  local label="$1"
  local root="$2"
  local target="$3"
  local expected="$4"

  if [ -e "$target" ]; then
    registered_worktree "$root" "$target" ||
      hold "$label staging path exists but is not registered"

    actual_head="$(git -C "$target" rev-parse HEAD 2>/dev/null || true)"
    test "$actual_head" = "$expected" ||
      hold "$label staging HEAD drift: ${actual_head:-UNAVAILABLE}"

    if git -C "$target" symbolic-ref -q HEAD >/dev/null 2>&1; then
      hold "$label staging worktree is attached to a branch"
    fi

    test -z "$(git -C "$target" status --porcelain=v1 --untracked-files=all)" ||
      hold "$label staging worktree is dirty"

    printf '%s_verified_exact_clean_detached_registered=true\n' "$label"
    git -C "$root" worktree remove "$target"

    test ! -e "$target" ||
      hold "$label staging path remained after bounded cleanup"
    if registered_worktree "$root" "$target"; then
      hold "$label staging worktree remained registered after bounded cleanup"
    fi
    printf '%s_staging_removed=true\n' "$label"
  else
    if registered_worktree "$root" "$target"; then
      hold "$label staging worktree is registered but path is absent"
    fi
    printf '%s_staging_already_absent=true\n' "$label"
  fi
}

printf '\n=== BOUNDED STALE STAGING CLEANUP ===\n'
cleanup_exact_staging_worktree \
  engine "$engine_repo" "$engine_staging" "$expected_engine_commit"
cleanup_exact_staging_worktree \
  source "$repo" "$source_staging" "$expected_source_commit"

printf '%s\n' \
  "bounded_staging_cleanup_complete=true" \
  "force_remove=false" \
  "worktree_prune=false" \
  "attempt_marker_created_during_cleanup=false" \
  "gpu_observation_performed_during_cleanup=false" \
  "runtime_execution_performed_during_cleanup=false"

printf '\n=== ALIGN LOCAL MAIN TO ACCEPTANCE MERGE ===\n'
initial_head="$(git rev-parse HEAD)"
printf 'initial_local_head=%s\n' "$initial_head"

git merge-base --is-ancestor "$initial_head" "$acceptance_merge" ||
  test "$initial_head" = "$acceptance_merge" ||
  hold "local main is ahead/diverged from authorized V2 acceptance lineage"

restore_main() {
  status=$?
  trap - EXIT INT TERM
  cd "$repo" || true
  git reset --hard "$acceptance_merge" >/dev/null 2>&1 || true
  git update-ref -d refs/void-exec/coherent-v2-canonical-main >/dev/null 2>&1 || true
  printf '\n=== LOCAL MAIN RESTORE ===\n'
  printf 'restored_local_main=%s\n' "$(git rev-parse HEAD 2>/dev/null || printf UNKNOWN)"
  if [ "$status" -ne 0 ]; then
    printf 'execution_terminal=HOLD_OR_FAILURE\n'
    printf 'automatic_retry=false\n'
  fi
  exit "$status"
}
trap restore_main EXIT INT TERM

git reset --hard "$acceptance_merge" >/dev/null

printf '\n=== ENTER AUTHORIZED V2 EXECUTION HEAD ===\n'
git reset --hard "$authorized_head" >/dev/null

test "$(git symbolic-ref -q HEAD)" = "refs/heads/main" ||
  hold "authorized V2 execution checkout is not local main"
test "$(git rev-parse HEAD)" = "$authorized_head" ||
  hold "authorized V2 execution head mismatch"
git diff --quiet || hold "tracked source dirty after authorized-head reset"
git diff --cached --quiet || hold "staged source dirty after authorized-head reset"

printf '%s\n' \
  "authorized_execution_head_active=true" \
  "canonical_remote_branch_mutation=false" \
  "git_push=false"

printf '\n=== ONE-SHOT V2 COHERENT COMBAT-PRIORITY EXECUTION ===\n'
printf '%s\n' \
  "IMPORTANT: exactly one invocation follows" \
  "IMPORTANT: no shell retry loop exists" \
  "IMPORTANT: fresh GPU admission occurs inside reviewed V2 invocation before claim" \
  "IMPORTANT: GPU admission failure consumes no fresh attempt" \
  "IMPORTANT: after fresh create-only claim, any later failure consumes this authorization"

PYTHONDONTWRITEBYTECODE=1 \
PYTHONNOUSERSITE=1 \
PYTHONPATH="$repo" \
"$v8_python" -B - "$authorized_head" "$invocation_sha256" <<'PY'
from __future__ import annotations

import json
import sys

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as invocation,
)

expected_main_head = sys.argv[1]
expected_source_sha256 = sys.argv[2]

result = invocation.execute_pair06_v8_combat_priority_coherent_v2_baseline_game(
    expected_main_head=expected_main_head,
    expected_invocation_source_sha256=expected_source_sha256,
    execution_authorization_accepted=True,
    policy_activation_authorization_accepted=True,
    execution_confirm=invocation.EXECUTION_CONFIRM_TOKEN,
    policy_confirm=invocation.POLICY_CONFIRM_TOKEN,
)

print("VOID_PAIR06_V8_COMBAT_PRIORITY_COHERENT_V2_EXECUTION_RESULT_V1")
print(json.dumps(result, sort_keys=True, separators=(",", ":"), default=str))
print("execution_terminal=GREEN")
print("automatic_retry=false")
PY

printf '\n=== ONE-SHOT RETURN ===\n'
printf '%s\n' \
  "invocation_returned=true" \
  "automatic_retry=false" \
  "script_retry_loop=false"
