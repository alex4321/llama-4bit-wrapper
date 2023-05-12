# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_finetune.ipynb.

# %% auto 0
__all__ = ['lora_model_zeros_and_scales_to_half']

# %% ../nbs/01_finetune.ipynb 3
from peft import PeftModel

# %% ../nbs/01_finetune.ipynb 5
def lora_model_zeros_and_scales_to_half(
        model: PeftModel # Original model
    ) -> PeftModel: # Converted model
    """
    Convert zeros and scales for PeftModel to half-precision
    """
    for _, m in model.named_modules():
        if "Autograd4bitQuantLinear" in str(type(m)) or "Linear4bitLt" in str(type(m)):
            if hasattr(m, "is_v1_model") and m.is_v1_model:
                m.zeros = m.zeros.half()
            m.scales = m.scales.half()
    return model
