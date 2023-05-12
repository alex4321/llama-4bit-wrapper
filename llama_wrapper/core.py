# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['import_llama']

# %% ../nbs/00_core.ipynb 4
def _apply_peft_tuners_monkeypatch():
    from alpaca_lora_4bit.monkeypatch.peft_tuners_lora_monkey_patch import replace_peft_model_with_int4_lora_model

    replace_peft_model_with_int4_lora_model()

# %% ../nbs/00_core.ipynb 5
def _apply_flash_attention_monkeypatch():
    from alpaca_lora_4bit.monkeypatch.llama_flash_attn_monkey_patch import replace_llama_attn_with_flash_attn

    replace_llama_attn_with_flash_attn()

# %% ../nbs/00_core.ipynb 6
def _apply_xformers_monkeypatch():
    from alpaca_lora_4bit.monkeypatch.llama_attn_hijack_xformers import hijack_llama_attention

    hijack_llama_attention()

# %% ../nbs/00_core.ipynb 7
def import_llama(
        use_flash_attention: bool, # Use flash attention monkeypatch or not (shouldn't be used with use_xformerts)
        use_xformers: bool, # Use xformers monkeypatch or not (shouldn't be used with use_flash_attention)
        autograd_4bit_cuda: bool, # Use CUDA backend for 4bit stuff
        autograd_4bit_triton: bool # Use Triton backend for 4bit stuff
    ): #load_llama_model_4bit_low_ram / load_llama_model_4bit_low_ram_and_offload / model_to_half / model_to_float / Autograd4bitQuantLinear / AMPWrapper
    """
    Do all the monkeypatching than return important objects of alpaca_lora_4bit library (arg_parser, train_data, load_llama_model_4bit_low_ram, load_llama_model_4bit_low_ram_and_offload, model_to_half, model_to_float, apply_gradient_checkpointing, Autograd4bitQuantLinear, AMPWrapper)
    """
    _apply_peft_tuners_monkeypatch()
    assert not (use_flash_attention and use_xformers)
    if use_flash_attention:
        _apply_flash_attention_monkeypatch()
    if use_xformers:
        _apply_xformers_monkeypatch()
    from alpaca_lora_4bit import autograd_4bit
    assert autograd_4bit_cuda ^ autograd_4bit_triton
    if autograd_4bit_cuda:
        autograd_4bit.switch_backend_to("cuda")
    if autograd_4bit_triton:
        autograd_4bit.switch_backend_to("triton")
    
    from alpaca_lora_4bit.autograd_4bit import load_llama_model_4bit_low_ram, load_llama_model_4bit_low_ram_and_offload, Autograd4bitQuantLinear, \
        model_to_half, model_to_float
    from alpaca_lora_4bit.amp_wrapper import AMPWrapper
    from alpaca_lora_4bit import train_data, arg_parser
    from alpaca_lora_4bit.gradient_checkpointing import apply_gradient_checkpointing

    return arg_parser, train_data, load_llama_model_4bit_low_ram, load_llama_model_4bit_low_ram_and_offload, model_to_half, model_to_float, apply_gradient_checkpointing, Autograd4bitQuantLinear, AMPWrapper
