import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from benchmark.exceptions import ModelLoadError, InferenceError


class HuggingFaceModel:
    """
    Wrapper around Hugging Face causal language models
    for safe loading and inference.
    """

    def __init__(
        self,
        model_id: str,
        device: str = "cpu",
        dtype: str = "float32",
    ):
        self.model_id = model_id
        self.device = device
        self.dtype = dtype

        self.tokenizer = None
        self.model = None

        self._load_model()

    def _get_torch_dtype(self):
        if self.dtype == "float16":
            return torch.float16
        return torch.float32

    def _load_model(self):
        """
        Load tokenizer and model safely.
        """
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_id,
                use_fast=True,
            )

            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=self._get_torch_dtype(),
            )

            self.model.to(self.device)
            self.model.eval()

        except Exception as exc:
            raise ModelLoadError(
                f"Failed to load model '{self.model_id}': {exc}"
            ) from exc

    def generate(
        self,
        prompt: str,
        generation_config: dict,
    ) -> tuple[str, int]:
        """
        Run safe text generation.

        Returns:
            output_text (str)
            output_tokens (int)
        """
        try:
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
            )

            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=generation_config.get("max_new_tokens", 128),
                    temperature=generation_config.get("temperature", 0.7),
                    top_p=generation_config.get("top_p", 0.9),
                    do_sample=generation_config.get("do_sample", True),
                )

            generated_ids = outputs[0]
            output_text = self.tokenizer.decode(
                generated_ids,
                skip_special_tokens=True,
            )

            output_tokens = len(generated_ids)

            return output_text, output_tokens

        except RuntimeError as exc:
            # Typical OOM or CUDA failure
            raise InferenceError(
                f"Inference failed for model '{self.model_id}': {exc}"
            ) from exc
