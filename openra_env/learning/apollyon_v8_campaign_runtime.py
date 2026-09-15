"""Reviewed source-only War College tool runtime for accepted Apollyon V8.

V8 was accepted as a deterministic local adapter under a fixed chat-template,
canonical tool schema, and textual tool-call parser, but that accepted surface
was not previously bound to the current War College campaign.  This module
freezes that transport and composes it with the already-reviewed campaign
representation/output translation.  It does not load model weights, start a
runtime, launch a game, train, mutate weights, or grant campaign authority.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

from .apollyon_v10_campaign_translation import (
    translate_campaign_turn,
    translate_runtime_tool_call,
    translation_contract,
)

RUNTIME_SCHEMA = "void.apollyon.v8-campaign-tool-runtime.v1"
RUNTIME_CONTRACT_SCHEMA = "void.apollyon.v8-campaign-tool-runtime-contract.v1"
CAMPAIGN_INPUT_KIND = "legacy_current_tool_list_plus_compact_state_json"
V8_ACCEPTED_INPUT_KIND = "current_state_fact_line_plus_canonical_tools"

V8_ADAPTER_SHA256 = (
    "ba792bd9472b0f9ee8e7acb5b40115a41c4def378fe74438b2f33d43b742b0e6"
)
V8_TRAINING_REPORT_SHA256 = (
    "b9286ec3535e2a16df20dbbac742b61e37b479e0808f3bdceb34eec54a127d75"
)
V8_FINAL_ACCEPTANCE_PACK_SHA256 = (
    "61935b744187c272bd1d5f920b8b3031728a534a66fd74a72befaadee18bb239"
)
V8_FINAL_ACCEPTANCE_DRIVER_SHA256 = (
    "8ab9e197ba605799cf511407f9e95042935264b18a6bb5af056fee07df2284e8"
)
V8_ACCEPTED_EVALUATOR_SHA256 = (
    "8c39267872ba797b30ce2ff7a2174863d7a5d4c8061afc6db8571786a7ea5f27"
)
V10_TRANSLATION_SOURCE_SHA256 = (
    "2d32351dff8d96a3254436305c2c402ea06c9a344b6b3ea67cb70c512eef2d53"
)
V10_TRANSLATION_CONTRACT_SHA256 = (
    "69c862387dad806681c5d066fea8e87836d2c0825f792ae293177c23cddee38b"
)

BASE_MODEL_REPOSITORY = "unsloth/Qwen3.5-4B"
BASE_MODEL_RESOLVED_REVISION = "3764fa359b9082ea5a1e4a5e3ac3aaf6e9671636"
BASE_MODEL_CONFIG_SHA256 = (
    "14687c353af8012cc1b563b3aeeefaa0b78d8780d8ea5270c73fe9fcdb7387f2"
)
BASE_MODEL_SHARD1_SHA256 = (
    "26a93f066e1916adb13453dae5a0c707c0fbc71299ed98779571a907b8e74c61"
)
BASE_MODEL_SHARD2_SHA256 = (
    "cb544bd9bfae93dc59b0f22b292f5933573854a7f9b97835c67060d7d910e188"
)
BASE_MODEL_INDEX_SHA256 = (
    "cf3f798ee02ba45f9622aa8892a47369ab667d0afbf154ee7c2212de42e6302d"
)
CHAT_TEMPLATE_SHA256 = (
    "8452ca85cb1e0ff04304c02f417a53305d5ba17f6eb9d5693343ad8355f985a8"
)
TOKENIZER_JSON_SHA256 = (
    "87a7830d63fcf43bf241c3c5242e96e62dd3fdc29224ca26fed8ea333db72de4"
)
TOKENIZER_CONFIG_SHA256 = (
    "04e9017bf53d513db997ce8a472ec0cef89339c7ab3af449e561af79fd45cb71"
)
MERGES_SHA256 = "3bd640ba6d8da8f5844f3548b7e2184fc664dd670e1447e425a48dbaaad1ef43"
VOCAB_SHA256 = "4ab0d5c096294054b66444a116a20baf6e29998fc1fae410ffe4b6fadbc56b5c"
ADDED_TOKENS_SHA256 = (
    "e5f9bfb644ead13bd36dd6cfc41553a93b7c264c0a2e1ac67d033aa8250c8538"
)
SPECIAL_TOKENS_MAP_SHA256 = (
    "ce5cbe737f4aacc7696180aac743091101b59e4dc5a338d9fc8a6f716aa513f7"
)
PROCESSOR_CONFIG_SHA256 = (
    "14932921ca485d458a04dafd8069fbb0a4505622a48208d19ed247115801385b"
)
V8_ADAPTER_CONFIG_SHA256 = (
    "a294abd44f7db7c1ba2c6362c5f5f99bbaa94b63eaa50401776a571025c2aacc"
)
V8_ADAPTER_TOKENIZER_CONFIG_SHA256 = (
    "1a71fa1e006db5fddc1903926f8d645a608a598504e630c1d82fb7057ee30978"
)
RUNTIME_PIP_FREEZE_SHA256 = (
    "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
)

MAX_NEW_TOKENS = 128
MAX_SEQUENCE_LENGTH = 1024
GENERATION_SEED = 3407
FINAL_ACCEPTANCE_TRANSFER_CORRECT = 28
FINAL_ACCEPTANCE_TRANSFER_TOTAL = 32
FINAL_ACCEPTANCE_LEGACY_CORRECT = 24
FINAL_ACCEPTANCE_LEGACY_TOTAL = 32
FINAL_ACCEPTANCE_FORMAT_CLEAN = 64
FINAL_ACCEPTANCE_FORMAT_TOTAL = 64

TRANSFER_SYSTEM_PROMPT = (
    "You are an Apollyon-v3 shadow-training candidate controlling Red Alert "
    "through tools. Treat the newest game state and deterministic guard feedback "
    "as authoritative. Prefer a legal useful action that is available now over "
    "passive waiting. Deploy an idle undeployed MCV before advancing. Start an "
    "explicitly available required structure if it is not already pending. "
    "Advance only when accepted work needs time or no better action exists. "
    "Issue at most one mutation-capable tool call per response. Relevant tools: "
    "get_game_state(); deploy_unit(unit_id); advance(ticks=1..50); "
    "move_units(unit_ids,target_x,target_y,queued=false); "
    "build_unit(unit_type,count=1); "
    "build_and_place(building_type,cell_x=0,cell_y=0); "
    "cancel_production(item_type)."
)
LEGACY_SYSTEM_PROMPT = (
    "You are an Apollyon-v3 shadow-training candidate controlling an RTS through "
    "tools. Treat the newest game state and deterministic guard feedback as "
    "authoritative. Do not repeat a mutation a guard has rejected. Observe fresh "
    "state after a mutation when later state is stale. Respect literal map bounds "
    "and current production availability. Issue at most one mutation-capable tool "
    "call per response. Relevant tools: get_game_state(); deploy_unit(unit_id); "
    "advance(ticks=1..50); move_units(unit_ids,target_x,target_y,queued=false); "
    "build_unit(unit_type,count=1); "
    "build_and_place(building_type,cell_x=0,cell_y=0); "
    "cancel_production(item_type)."
)

ACCEPTED_TOOL_NAMES = (
    "get_game_state",
    "deploy_unit",
    "advance",
    "move_units",
    "build_unit",
    "build_and_place",
    "cancel_production",
)

_ACCEPTED_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_game_state",
            "description": "Get the current game-state summary.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "deploy_unit",
            "description": "Deploy a deployable unit such as an MCV.",
            "parameters": {
                "type": "object",
                "properties": {"unit_id": {"type": "integer"}},
                "required": ["unit_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "advance",
            "description": "Advance game time. ticks must be 1 through 50.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticks": {"type": "integer", "minimum": 1, "maximum": 50}
                },
                "required": ["ticks"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "move_units",
            "description": "Move selected units to a legal map cell.",
            "parameters": {
                "type": "object",
                "properties": {
                    "unit_ids": {"type": "string"},
                    "target_x": {"type": "integer"},
                    "target_y": {"type": "integer"},
                    "queued": {"type": "boolean", "default": False},
                },
                "required": ["unit_ids", "target_x", "target_y"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "build_unit",
            "description": "Queue production of a currently available unit type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "unit_type": {"type": "string"},
                    "count": {"type": "integer", "minimum": 1, "default": 1},
                },
                "required": ["unit_type"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "build_and_place",
            "description": (
                "Queue a structure for construction and automatic placement."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "building_type": {"type": "string"},
                    "cell_x": {"type": "integer", "default": 0},
                    "cell_y": {"type": "integer", "default": 0},
                },
                "required": ["building_type"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_production",
            "description": "Cancel an item confirmed present in a production queue.",
            "parameters": {
                "type": "object",
                "properties": {"item_type": {"type": "string"}},
                "required": ["item_type"],
                "additionalProperties": False,
            },
        },
    },
]

_TOOL_RE = re.compile(
    r"<tool_call>\s*<function=([^>\r\n]+)>\s*(.*?)</function>\s*</tool_call>",
    re.DOTALL,
)
_PARAM_RE = re.compile(
    r"<parameter=([^>\r\n]+)>\s*(.*?)\s*</parameter>",
    re.DOTALL,
)


class V8CampaignRuntimeError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V8CampaignRuntimeError(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def _tool_name(tool: Mapping[str, Any]) -> str:
    _require(tool.get("type") == "function", "runtime tool must be function")
    function = tool.get("function")
    _require(isinstance(function, Mapping), "runtime tool.function missing")
    name = function.get("name")
    _require(isinstance(name, str) and bool(name), "runtime tool name missing")
    return name


def _parse_scalar(text: str) -> Any:
    text = text.strip()
    low = text.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "none"):
        return None
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", text):
        return float(text)
    if text.startswith(("{", "[", '"')):
        try:
            return json.loads(text)
        except Exception:
            pass
    return text


def parse_v8_tool_output(text: str) -> dict[str, Any]:
    """Parse the exact textual tool-call wire format used by accepted V8."""
    _require(isinstance(text, str) and bool(text.strip()), "V8 output must be text")
    calls: list[dict[str, Any]] = []
    for match in _TOOL_RE.finditer(text):
        name = match.group(1).strip()
        body = match.group(2)
        arguments: dict[str, Any] = {}
        duplicate = False
        for param in _PARAM_RE.finditer(body):
            key = param.group(1).strip()
            _require(bool(key), "empty V8 parameter name")
            if key in arguments:
                duplicate = True
            arguments[key] = _parse_scalar(param.group(2))
        calls.append(
            {
                "tool": name,
                "arguments": arguments,
                "duplicate_parameter": duplicate,
                "span": (match.start(), match.end()),
            }
        )

    _require(len(calls) == 1, "V8 output must contain exactly one tool call")
    call = calls[0]
    _require(not call["duplicate_parameter"], "V8 output has duplicate parameter")
    prefix = text[: call["span"][0]].strip()
    suffix = text[call["span"][1] :].strip()
    _require(not suffix, "V8 output has trailing content after tool call")
    return {
        "tool": call["tool"],
        "arguments": dict(call["arguments"]),
        "reasoning_prefix_present": bool(prefix),
        "exactly_one_tool_call": True,
        "no_duplicate_parameters": True,
        "suffix_clean": True,
    }


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _require_exact_file(path: Path, expected_sha256: str, label: str) -> None:
    _require(path.is_file() and not path.is_symlink(), f"{label} missing or symlinked")
    _require(_sha256_file(path) == expected_sha256, f"{label} SHA-256 drift")


def verify_v8_runtime_assets(*, model_dir: Path, adapter_dir: Path) -> dict[str, Any]:
    """Verify exact local runtime bytes without loading the model."""
    model = Path(model_dir).expanduser().resolve()
    adapter = Path(adapter_dir).expanduser().resolve()
    _require(model != adapter, "model and adapter directories must be distinct")
    required = [
        (model / "config.json", BASE_MODEL_CONFIG_SHA256, "base config"),
        (
            model / "model.safetensors-00001-of-00002.safetensors",
            BASE_MODEL_SHARD1_SHA256,
            "base shard 1",
        ),
        (
            model / "model.safetensors-00002-of-00002.safetensors",
            BASE_MODEL_SHARD2_SHA256,
            "base shard 2",
        ),
        (model / "model.safetensors.index.json", BASE_MODEL_INDEX_SHA256, "base index"),
        (model / "chat_template.jinja", CHAT_TEMPLATE_SHA256, "base chat template"),
        (model / "tokenizer.json", TOKENIZER_JSON_SHA256, "base tokenizer"),
        (model / "tokenizer_config.json", TOKENIZER_CONFIG_SHA256, "base tokenizer config"),
        (model / "merges.txt", MERGES_SHA256, "base merges"),
        (model / "vocab.json", VOCAB_SHA256, "base vocab"),
        (model / "added_tokens.json", ADDED_TOKENS_SHA256, "base added tokens"),
        (
            model / "special_tokens_map.json",
            SPECIAL_TOKENS_MAP_SHA256,
            "base special tokens",
        ),
        (model / "processor_config.json", PROCESSOR_CONFIG_SHA256, "base processor config"),
        (adapter / "adapter_config.json", V8_ADAPTER_CONFIG_SHA256, "V8 adapter config"),
        (adapter / "adapter_model.safetensors", V8_ADAPTER_SHA256, "V8 adapter weights"),
        (adapter / "chat_template.jinja", CHAT_TEMPLATE_SHA256, "V8 adapter chat template"),
        (adapter / "tokenizer.json", TOKENIZER_JSON_SHA256, "V8 adapter tokenizer"),
        (
            adapter / "tokenizer_config.json",
            V8_ADAPTER_TOKENIZER_CONFIG_SHA256,
            "V8 adapter tokenizer config",
        ),
    ]
    for path, expected, label in required:
        _require_exact_file(path, expected, label)
    return {
        "model_dir": model,
        "adapter_dir": adapter,
        "verified_file_count": len(required),
        "runtime_execution_performed": False,
        "model_execution_performed": False,
    }


class FrozenV8LocalToolRuntime:
    """Dormant exact-byte V8 runtime surface; loading is always explicit."""

    def __init__(self, *, model: Any, tokenizer: Any, torch_module: Any) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self._torch = torch_module

    @classmethod
    def load(cls, *, model_dir: Path, adapter_dir: Path):
        verify_v8_runtime_assets(model_dir=model_dir, adapter_dir=adapter_dir)
        import os

        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        __import__("unsloth")
        import torch
        from peft import PeftModel
        from unsloth import FastModel

        torch.manual_seed(GENERATION_SEED)
        torch.cuda.manual_seed_all(GENERATION_SEED)
        model, processor = FastModel.from_pretrained(
            model_name=str(Path(model_dir).expanduser().resolve()),
            max_seq_length=MAX_SEQUENCE_LENGTH,
            dtype=torch.bfloat16,
            load_in_4bit=False,
            load_in_8bit=False,
            full_finetuning=False,
            local_files_only=True,
        )
        tokenizer = getattr(processor, "tokenizer", processor)
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token = tokenizer.eos_token
        _require(tokenizer.pad_token_id is not None, "tokenizer has no usable pad/eos token")
        model = PeftModel.from_pretrained(
            model,
            str(Path(adapter_dir).expanduser().resolve()),
            is_trainable=False,
            local_files_only=True,
        )
        model.eval()
        return cls(model=model, tokenizer=tokenizer, torch_module=torch)

    def generate(self, *, messages: Sequence[Mapping[str, Any]], tools: Sequence[Mapping[str, Any]]) -> str:
        _require(len(messages) == 2, "V8 runtime requires exact two-message current input")
        _current_runtime_names(tools)
        prompt = self.tokenizer.apply_chat_template(
            list(messages),
            tools=list(tools),
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        encoded = self.tokenizer(
            prompt,
            return_tensors="pt",
            add_special_tokens=False,
        )
        encoded = {key: value.to("cuda") for key, value in encoded.items()}
        prompt_len = int(encoded["input_ids"].shape[1])
        with self._torch.inference_mode():
            output = self.model.generate(
                **encoded,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=False,
                use_cache=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        new_ids = output[0, prompt_len:].detach().cpu()
        return self.tokenizer.decode(new_ids, skip_special_tokens=True).strip()

    def decide_campaign_turn(
        self,
        *,
        state: Mapping[str, Any],
        typed_tools: Sequence[Mapping[str, Any]],
        tool_contract: Mapping[str, Any],
        doctrine: str,
        round_no: int,
        feedback: str = "",
    ) -> dict[str, Any]:
        turn = translate_campaign_turn_for_v8(
            state=state,
            typed_tools=typed_tools,
            tool_contract=tool_contract,
            doctrine=doctrine,
            round_no=round_no,
            feedback=feedback,
        )
        raw = self.generate(messages=turn["messages"], tools=turn["tools"])
        action = translate_v8_output_to_campaign(
            text=raw,
            runtime_tools=turn["tools"],
            tool_contract=tool_contract,
        )
        return {
            "runtime_input": turn,
            "raw_model_output": raw,
            "campaign_action": action,
            "host_mutation_performed": False,
        }


def _frozen_runtime_tools(
    translated_tools: Sequence[Mapping[str, Any]],
    tool_contract: Mapping[str, Any],
) -> list[dict[str, Any]]:
    current_names = [_tool_name(tool) for tool in translated_tools]
    _require(
        len(current_names) == len(set(current_names)),
        "translated campaign tool names collide",
    )
    available = set(current_names) & set(ACCEPTED_TOOL_NAMES)
    accepted = {_tool_name(tool): tool for tool in _ACCEPTED_TOOLS}
    output: list[dict[str, Any]] = []

    for name in ACCEPTED_TOOL_NAMES:
        if name not in available:
            continue
        tool = deepcopy(accepted[name])
        params = tool["function"]["parameters"]
        props = params["properties"]
        if name == "advance":
            props["ticks"]["minimum"] = 50
            props["ticks"]["maximum"] = 50
        elif name == "build_unit":
            legal_units = list(tool_contract.get("legal_units", []))
            _require(bool(legal_units), "build_unit exposed without legal units")
            props["unit_type"]["enum"] = legal_units
            props["count"]["maximum"] = 3
        elif name == "build_and_place":
            legal_buildings = list(tool_contract.get("legal_buildings", []))
            _require(bool(legal_buildings), "build_and_place exposed without legal buildings")
            props["building_type"]["enum"] = legal_buildings
            props["cell_x"]["minimum"] = 0
            props["cell_x"]["maximum"] = 0
            props["cell_y"]["minimum"] = 0
            props["cell_y"]["maximum"] = 0
        output.append(tool)

    _require(bool(output), "V8 campaign runtime has no currently available accepted tools")
    return output


def _v8_current_state_prompt(
    *,
    state: Mapping[str, Any],
    tool_contract: Mapping[str, Any],
    runtime_tool_names: Sequence[str],
    doctrine: str,
    round_no: int,
    feedback: str,
) -> str:
    def rows(label: str, values: Sequence[Mapping[str, Any]], *, include_flags: bool) -> str:
        rendered: list[str] = []
        for row in sorted(values, key=lambda value: int(value["id"])):
            base = (
                f"{int(row['id'])}:{row['type']}@"
                f"({int(row['cell_x'])},{int(row['cell_y'])})"
            )
            if include_flags:
                idle = row.get("idle", row.get("is_idle"))
                base += (
                    f" idle={str(bool(idle)).lower()}"
                    f" can_attack={str(bool(row['can_attack'])).lower()}"
                )
            rendered.append(base)
        return f"{label}=[" + ",".join(rendered) + "]"

    economy = state["economy"]
    map_info = state["map"]
    width = int(map_info["width"])
    height = int(map_info["height"])
    facts = [
        f"tick={int(state['tick'])}",
        f"round={round_no}",
        f"opponent_doctrine={json.dumps(doctrine, ensure_ascii=False)}",
        f"cash={int(economy['cash'])}",
        f"ore={int(economy['ore'])}",
        f"harvesters={int(economy['harvester_count'])}",
        f"power_balance={int(state['power_balance'])}",
        rows("own_units", state["units_summary"], include_flags=True),
        rows("own_buildings", state["buildings_summary"], include_flags=False),
        rows("visible_enemies", state["enemy_summary"], include_flags=False),
        rows("visible_enemy_buildings", state["enemy_buildings_summary"], include_flags=False),
        "production_items=" + json.dumps(list(state["production_items"]), separators=(",", ":")),
        "available_production="
        + json.dumps(list(state["available_production"]), separators=(",", ":")),
        "legal_buildings="
        + json.dumps(list(tool_contract.get("legal_buildings", [])), separators=(",", ":")),
        "legal_units="
        + json.dumps(list(tool_contract.get("legal_units", [])), separators=(",", ":")),
        f"map_bounds=x=0..{width - 1},y=0..{height - 1}",
        f"explored_percent={float(state['explored_percent']):.6f}",
        "CURRENT_ALLOWED_TOOL_NAMES="
        + json.dumps(list(runtime_tool_names), separators=(",", ":")),
    ]
    if feedback.strip():
        facts.append("guard_feedback=" + json.dumps(feedback, ensure_ascii=False))
    return "CURRENT STATE: " + "; ".join(facts) + ". Choose exactly one current tool action."


def translate_campaign_turn_for_v8(
    *,
    state: Mapping[str, Any],
    typed_tools: Sequence[Mapping[str, Any]],
    tool_contract: Mapping[str, Any],
    doctrine: str,
    round_no: int,
    feedback: str = "",
) -> dict[str, Any]:
    """Translate one current campaign turn into the frozen V8 input surface."""
    _require(isinstance(feedback, str), "feedback must be string")
    selected_system = LEGACY_SYSTEM_PROMPT if feedback.strip() else TRANSFER_SYSTEM_PROMPT
    translated = translate_campaign_turn(
        system=selected_system,
        state=state,
        typed_tools=typed_tools,
        tool_contract=tool_contract,
        doctrine=doctrine,
        round_no=round_no,
        feedback=feedback,
    )
    raw_tools = translated.get("tools")
    _require(isinstance(raw_tools, list), "campaign translation tools missing")
    runtime_tools = _frozen_runtime_tools(raw_tools, tool_contract)
    runtime_names = [_tool_name(tool) for tool in runtime_tools]
    user_prompt = _v8_current_state_prompt(
        state=state,
        tool_contract=tool_contract,
        runtime_tool_names=runtime_names,
        doctrine=doctrine,
        round_no=round_no,
        feedback=feedback,
    )
    messages = [
        {"role": "system", "content": selected_system},
        {"role": "user", "content": user_prompt},
    ]

    body = {
        "schema": RUNTIME_SCHEMA,
        "messages": deepcopy(messages),
        "tools": runtime_tools,
        "generation": {
            "max_sequence_length": MAX_SEQUENCE_LENGTH,
            "max_new_tokens": MAX_NEW_TOKENS,
            "do_sample": False,
            "use_cache": True,
            "add_special_tokens": False,
            "add_generation_prompt": True,
            "enable_thinking": False,
            "seed": GENERATION_SEED,
        },
        "binding": {
            "campaign_input_kind": CAMPAIGN_INPUT_KIND,
            "accepted_input_kind": V8_ACCEPTED_INPUT_KIND,
        "accepted_user_prompt_prefix": "CURRENT STATE:",
        "current_state_fact_renderer_reviewed": True,
            "system_prompt_family": "legacy" if feedback.strip() else "transfer",
            "runtime_tool_names": runtime_names,
            "source_translation_sha256": translated["translation_sha256"],
            "uses_current_state_only": True,
            "uses_current_tool_list_only": True,
            "tool_schema_change": "narrowing_only",
            "fabricated_information": False,
            "runtime_execution_performed": False,
            "model_execution_performed": False,
            "game_mutation_performed": False,
        },
    }
    return {**body, "runtime_input_sha256": _sha256(body)}


def _current_runtime_names(runtime_tools: Sequence[Mapping[str, Any]]) -> set[str]:
    _require(
        isinstance(runtime_tools, Sequence)
        and not isinstance(runtime_tools, (str, bytes, bytearray)),
        "runtime tools must be sequence",
    )
    names = [_tool_name(tool) for tool in runtime_tools]
    _require(len(names) == len(set(names)), "runtime tool names contain duplicates")
    _require(set(names).issubset(set(ACCEPTED_TOOL_NAMES)), "runtime contains unaccepted V8 tool")
    accepted = {_tool_name(tool): tool for tool in _ACCEPTED_TOOLS}
    for tool in runtime_tools:
        name = _tool_name(tool)
        function = tool["function"]
        _require(
            function.get("description") == accepted[name]["function"]["description"],
            f"V8 runtime tool description drift: {name}",
        )
        params = function.get("parameters")
        _require(isinstance(params, Mapping), f"V8 runtime parameters missing: {name}")
        _require(params.get("type") == "object", f"V8 runtime parameter type drift: {name}")
        _require(params.get("additionalProperties") is False, f"V8 runtime extra args enabled: {name}")
        props = params.get("properties")
        _require(isinstance(props, Mapping), f"V8 runtime properties missing: {name}")
        if name in {"get_game_state", "deploy_unit", "move_units", "cancel_production"}:
            _require(tool == accepted[name], f"V8 frozen tool schema drift: {name}")
        elif name == "advance":
            _require(params.get("required") == ["ticks"], "V8 advance required args drift")
            _require(set(props) == {"ticks"}, "V8 advance properties drift")
            ticks = props["ticks"]
            _require(
                isinstance(ticks, Mapping)
                and ticks.get("type") == "integer"
                and ticks.get("minimum") == 50
                and ticks.get("maximum") == 50,
                "V8 advance schema must be narrowed to exactly 50 ticks",
            )
        elif name == "build_unit":
            _require(params.get("required") == ["unit_type"], "V8 build_unit required args drift")
            _require(set(props) == {"unit_type", "count"}, "V8 build_unit properties drift")
            unit_type = props["unit_type"]
            count = props["count"]
            legal = unit_type.get("enum") if isinstance(unit_type, Mapping) else None
            _require(
                isinstance(unit_type, Mapping)
                and unit_type.get("type") == "string"
                and isinstance(legal, list)
                and bool(legal)
                and len(legal) == len(set(legal))
                and all(isinstance(value, str) and bool(value) for value in legal),
                "V8 build_unit legal-unit narrowing invalid",
            )
            _require(
                isinstance(count, Mapping)
                and count.get("type") == "integer"
                and count.get("minimum") == 1
                and count.get("maximum") == 3
                and count.get("default") == 1,
                "V8 build_unit count narrowing drift",
            )
        elif name == "build_and_place":
            _require(
                params.get("required") == ["building_type"],
                "V8 build_and_place required args drift",
            )
            _require(
                set(props) == {"building_type", "cell_x", "cell_y"},
                "V8 build_and_place properties drift",
            )
            building_type = props["building_type"]
            legal = building_type.get("enum") if isinstance(building_type, Mapping) else None
            _require(
                isinstance(building_type, Mapping)
                and building_type.get("type") == "string"
                and isinstance(legal, list)
                and bool(legal)
                and len(legal) == len(set(legal))
                and all(isinstance(value, str) and bool(value) for value in legal),
                "V8 build_and_place legal-building narrowing invalid",
            )
            for coordinate in ("cell_x", "cell_y"):
                value = props[coordinate]
                _require(
                    isinstance(value, Mapping)
                    and value.get("type") == "integer"
                    and value.get("minimum") == 0
                    and value.get("maximum") == 0
                    and value.get("default") == 0,
                    f"V8 {coordinate} narrowing drift",
                )
    return set(names)


def _is_int(value: Any) -> bool:
    return type(value) is int


def translate_v8_output_to_campaign(
    *,
    text: str,
    runtime_tools: Sequence[Mapping[str, Any]],
    tool_contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Parse one accepted-format V8 tool call and map it to the campaign host."""
    parsed = parse_v8_tool_output(text)
    tool = parsed["tool"]
    args = dict(parsed["arguments"])
    available = _current_runtime_names(runtime_tools)
    _require(tool in available, f"V8 selected unavailable runtime tool: {tool}")

    if tool == "get_game_state":
        _require(args == {}, "get_game_state arguments invalid")
    elif tool == "deploy_unit":
        _require(set(args) == {"unit_id"}, "deploy_unit arguments invalid")
        _require(_is_int(args["unit_id"]) and args["unit_id"] > 0, "deploy_unit id invalid")
    elif tool == "advance":
        _require(args == {"ticks": 50}, "V8 campaign advance must be exactly 50 ticks")
    elif tool == "move_units":
        _require(
            set(args).issubset({"unit_ids", "target_x", "target_y", "queued"}),
            "move_units arguments invalid",
        )
        _require(
            {"unit_ids", "target_x", "target_y"}.issubset(args),
            "move_units required arguments missing",
        )
        _require(isinstance(args["unit_ids"], str) and bool(args["unit_ids"]), "unit_ids invalid")
        _require(_is_int(args["target_x"]) and _is_int(args["target_y"]), "movement coordinates invalid")
        queued = args.get("queued", False)
        _require(type(queued) is bool, "move_units queued invalid")
        args["queued"] = queued
    elif tool == "build_unit":
        _require(set(args).issubset({"unit_type", "count"}), "build_unit arguments invalid")
        _require("unit_type" in args, "build_unit unit_type missing")
        _require(
            isinstance(args["unit_type"], str)
            and args["unit_type"] in tool_contract.get("legal_units", []),
            "V8 selected illegal unit",
        )
        count = args.get("count", 1)
        _require(_is_int(count) and 1 <= count <= 3, "V8 unit count invalid")
        args["count"] = count
    elif tool == "build_and_place":
        _require(
            set(args).issubset({"building_type", "cell_x", "cell_y"}),
            "build_and_place arguments invalid",
        )
        _require("building_type" in args, "build_and_place building_type missing")
        _require(
            isinstance(args["building_type"], str)
            and args["building_type"] in tool_contract.get("legal_buildings", []),
            "V8 selected illegal building",
        )
        _require(args.get("cell_x", 0) == 0, "V8 nonzero placement x is not campaign-reviewed")
        _require(args.get("cell_y", 0) == 0, "V8 nonzero placement y is not campaign-reviewed")
        args = {"building_type": args["building_type"]}
    elif tool == "cancel_production":
        _require(set(args) == {"item_type"}, "cancel_production arguments invalid")
        _require(isinstance(args["item_type"], str) and bool(args["item_type"]), "cancel item invalid")
    else:
        raise V8CampaignRuntimeError(f"unsupported accepted V8 tool: {tool}")

    mapped = translate_runtime_tool_call(
        tool=tool,
        arguments=args,
        tool_contract=tool_contract,
    )
    return {
        **mapped,
        "v8_wire_format": "v1_tool_call_text",
        "reasoning_prefix_present": parsed["reasoning_prefix_present"],
        "host_validation_unchanged": True,
    }


def v8_tool_runtime_contract() -> dict[str, Any]:
    """Return the reviewed nonexecuting V8 campaign tool-runtime contract."""
    v10_contract = translation_contract()
    _require(
        v10_contract["translation_contract_sha256"] == V10_TRANSLATION_CONTRACT_SHA256,
        "V10 campaign translation contract drift",
    )
    translation_path = Path(__file__).with_name("apollyon_v10_campaign_translation.py")
    _require(translation_path.is_file(), "V10 campaign translation source missing")
    _require(
        hashlib.sha256(translation_path.read_bytes()).hexdigest()
        == V10_TRANSLATION_SOURCE_SHA256,
        "V10 campaign translation source drift",
    )

    accepted_tool_schema_sha256 = _sha256(_ACCEPTED_TOOLS)
    body = {
        "schema": RUNTIME_CONTRACT_SCHEMA,
        "campaign_input_kind": CAMPAIGN_INPUT_KIND,
        "accepted_input_kind": V8_ACCEPTED_INPUT_KIND,
        "v8_adapter_sha256": V8_ADAPTER_SHA256,
        "v8_training_report_sha256": V8_TRAINING_REPORT_SHA256,
        "v8_final_acceptance_pack_sha256": V8_FINAL_ACCEPTANCE_PACK_SHA256,
        "v8_final_acceptance_driver_sha256": V8_FINAL_ACCEPTANCE_DRIVER_SHA256,
        "v8_accepted_evaluator_sha256": V8_ACCEPTED_EVALUATOR_SHA256,
        "v10_translation_source_sha256": V10_TRANSLATION_SOURCE_SHA256,
        "v10_translation_contract_sha256": V10_TRANSLATION_CONTRACT_SHA256,
        "base_model_repository": BASE_MODEL_REPOSITORY,
        "base_model_resolved_revision": BASE_MODEL_RESOLVED_REVISION,
        "base_model_config_sha256": BASE_MODEL_CONFIG_SHA256,
        "base_model_shard1_sha256": BASE_MODEL_SHARD1_SHA256,
        "base_model_shard2_sha256": BASE_MODEL_SHARD2_SHA256,
        "base_model_index_sha256": BASE_MODEL_INDEX_SHA256,
        "chat_template_sha256": CHAT_TEMPLATE_SHA256,
        "tokenizer_json_sha256": TOKENIZER_JSON_SHA256,
        "tokenizer_config_sha256": TOKENIZER_CONFIG_SHA256,
        "merges_sha256": MERGES_SHA256,
        "vocab_sha256": VOCAB_SHA256,
        "added_tokens_sha256": ADDED_TOKENS_SHA256,
        "special_tokens_map_sha256": SPECIAL_TOKENS_MAP_SHA256,
        "processor_config_sha256": PROCESSOR_CONFIG_SHA256,
        "v8_adapter_config_sha256": V8_ADAPTER_CONFIG_SHA256,
        "v8_adapter_tokenizer_config_sha256": V8_ADAPTER_TOKENIZER_CONFIG_SHA256,
        "runtime_pip_freeze_sha256": RUNTIME_PIP_FREEZE_SHA256,
        "accepted_tool_names": list(ACCEPTED_TOOL_NAMES),
        "final_acceptance_transfer_correct": FINAL_ACCEPTANCE_TRANSFER_CORRECT,
        "final_acceptance_transfer_total": FINAL_ACCEPTANCE_TRANSFER_TOTAL,
        "final_acceptance_legacy_correct": FINAL_ACCEPTANCE_LEGACY_CORRECT,
        "final_acceptance_legacy_total": FINAL_ACCEPTANCE_LEGACY_TOTAL,
        "final_acceptance_format_clean": FINAL_ACCEPTANCE_FORMAT_CLEAN,
        "final_acceptance_format_total": FINAL_ACCEPTANCE_FORMAT_TOTAL,
        "accepted_tool_schema_sha256": accepted_tool_schema_sha256,
        "transfer_system_prompt_sha256": hashlib.sha256(TRANSFER_SYSTEM_PROMPT.encode()).hexdigest(),
        "legacy_system_prompt_sha256": hashlib.sha256(LEGACY_SYSTEM_PROMPT.encode()).hexdigest(),
        "tool_wire_format": "v1_tool_call_text",
        "parser_exactly_one_tool_call": True,
        "parser_rejects_duplicate_parameters": True,
        "parser_rejects_trailing_suffix": True,
        "reasoning_prefix_allowed": True,
        "max_sequence_length": MAX_SEQUENCE_LENGTH,
        "max_new_tokens": MAX_NEW_TOKENS,
        "deterministic_generation": True,
        "do_sample": False,
        "enable_thinking": False,
        "current_state_only": True,
        "current_tool_list_authoritative": True,
        "accepted_user_prompt_prefix": "CURRENT STATE:",
        "current_state_fact_renderer_reviewed": True,
        "tool_schema_narrowing_only": True,
        "local_runtime_loader_implemented": True,
        "runtime_assets_hash_verified_before_load": True,
        "offline_only_model_load": True,
        "accepted_chat_template_generation_implemented": True,
        "campaign_decision_adapter_implemented": True,
        "advance_narrowed_to_shared_50_ticks": True,
        "production_output_maps_to_current_typed_identity": True,
        "placement_coordinates_must_be_zero_or_absent": True,
        "host_validation_unchanged": True,
        "fabricated_information_allowed": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_started": False,
        "game_mutation_performed": False,
        "training": False,
        "weights_updated": False,
        "automatic_corpus_admission": False,
        "automatic_policy_promotion": False,
    }
    return {**body, "tool_runtime_contract_sha256": _sha256(body)}
