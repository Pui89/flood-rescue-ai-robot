"""Gemma 4 multimodal reasoning adapter for flood-rescue scene analysis.

Uses the official Transformers interface for google/gemma-4-31B-it.
Model weights are downloaded at runtime and are not stored here.
The model is advisory and never directly controls robot actuators.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

MODEL_ID = "google/gemma-4-31B-it"


class Gemma4FloodReasoner:
    """Run Gemma 4 31B IT for multimodal flood-rescue reasoning."""

    def __init__(self, model_id: str = MODEL_ID, max_new_tokens: int = 256):
        self.model_id = model_id
        self.max_new_tokens = max_new_tokens
        self._processor = None
        self._model = None

    def _load(self) -> None:
        if self._model is not None:
            return
        from transformers import AutoModelForMultimodalLM, AutoProcessor
        self._processor = AutoProcessor.from_pretrained(self.model_id)
        self._model = AutoModelForMultimodalLM.from_pretrained(
            self.model_id, device_map="auto"
        )

    def reason(self, prompt: str, image_url: Optional[str] = None) -> str:
        """Return a multimodal reasoning response; never issue actuator commands."""
        self._load()
        content = []
        if image_url:
            content.append({"type": "image", "url": image_url})
        content.append({"type": "text", "text": prompt})
        messages = [{"role": "user", "content": content}]

        inputs = self._processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self._model.device)

        outputs = self._model.generate(**inputs, max_new_tokens=self.max_new_tokens)
        prompt_len = inputs["input_ids"].shape[-1]
        return self._processor.decode(
            outputs[0][prompt_len:], skip_special_tokens=True
        )

    def structured_decision(
        self,
        scene_summary: Dict[str, Any],
        image_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Return a conservative structured rescue decision."""
        prompt = (
            "You are the multimodal reasoning layer of a flood-rescue robot. "
            "Return ONLY valid JSON with keys: priority, rationale, confidence, "
            "next_steps, target_id, requires_human_review. Treat unseen or "
            "occluded people as unknown. Never claim a person is absent merely "
            "because detection is missing. Prefer re-observation when visibility "
            "is uncertain. Never output motor or actuator commands. The "
            "deterministic safety controller has final authority.\n\n"
            f"Scene summary:\n{json.dumps(scene_summary, ensure_ascii=False)}"
        )
        raw = self.reason(prompt, image_url=image_url)
        try:
            decision = json.loads(raw)
            if not isinstance(decision, dict):
                raise ValueError("response is not a JSON object")
            return decision
        except (json.JSONDecodeError, TypeError, ValueError):
            return {
                "priority": "reobserve",
                "rationale": "Invalid structured output; require fresh observation.",
                "confidence": 0.0,
                "next_steps": [
                    "refresh_rgb",
                    "refresh_thermal_or_nir",
                    "refresh_depth_or_lidar",
                ],
                "target_id": None,
                "requires_human_review": True,
            }
