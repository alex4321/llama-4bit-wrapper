# llama-wrapper

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

It’s a wrapper for https://github.com/johnsmith0031/alpaca_lora_4bit
which allows you to do all the monkeypatching of the library without
writing a bunch of stuff like next:

``` python
# Early load config to replace attn if needed
from arg_parser import get_config
ft_config = get_config()

from monkeypatch.peft_tuners_lora_monkey_patch import replace_peft_model_with_gptq_lora_model
replace_peft_model_with_gptq_lora_model()

if ft_config.flash_attention:
    from monkeypatch.llama_flash_attn_monkey_patch import replace_llama_attn_with_flash_attn
    replace_llama_attn_with_flash_attn()
elif ft_config.xformers:
    from monkeypatch.llama_attn_hijack_xformers import hijack_llama_attention
    hijack_llama_attention()

import autograd_4bit
if ft_config.backend.lower() == 'triton':
    autograd_4bit.switch_backend_to('triton')
else:
    autograd_4bit.switch_backend_to('cuda')
```

Instead it provide you a function like next:

``` python
load_llama_model_4bit_low_ram, _, model_to_half, _, _, AMPWrapper = import_alpaca(
    use_flash_attention=True,
    use_xformers=False,
    autograd_4bit_cuda=False,
    autograd_4bit_triton=True,
)

model, tokenizer = load_llama_model_4bit_low_ram(
    config_path="../vicuna-13b-GPTQ-4bit-128g/",
    model_path="../vicuna-13b-GPTQ-4bit-128g/vicuna-13b-4bit-128g.safetensors",
    groupsize=128,
    is_v1_model=False,
)
model_to_half(model)

wrapper = AMPWrapper(model)
wrapper.apply_generate()
```

which run all the monkeypatching inside.

## Install

``` sh
pip install llama_wrapper
```

## How to use

### Inference example

``` python
# Init modules
load_llama_model_4bit_low_ram, _, model_to_half, _, _, AMPWrapper = import_alpaca(
    use_flash_attention=True,
    use_xformers=False,
    autograd_4bit_cuda=False,
    autograd_4bit_triton=True,
)
# Init model
model, tokenizer = load_llama_model_4bit_low_ram(
    config_path="../vicuna-13b-GPTQ-4bit-128g/",
    model_path="../vicuna-13b-GPTQ-4bit-128g/vicuna-13b-4bit-128g.safetensors",
    groupsize=128,
    is_v1_model=False,
)
model_to_half(model)
# CUDA amp wrapper
wrapper = AMPWrapper(model)
wrapper.apply_generate()
# Generation
prompt = '''I think the meaning of life is'''
batch = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
batch = {k: v.cuda() for k, v in batch.items()}
start = time.time()
with torch.no_grad():
    generated = model.generate(inputs=batch["input_ids"],
                               do_sample=True,
                               use_cache=False,
                               repetition_penalty=1.1,
                               max_new_tokens=128,
                               temperature=0.9,
                               top_p=0.95,
                               top_k=40,
                               return_dict_in_generate=True,
                               output_attentions=False,
                               output_hidden_states=False,
                               output_scores=False)
result_text = tokenizer.decode(generated['sequences'].cpu().tolist()[0])
end = time.time()
print(result_text)
print(end - start)
```

It should give you something similar to this (tested it using Geforce
2080ti graphic card):

    I think the meaning of life is to be happy, and that it is our birthright. That we are supposed to feel good as human beings, and that every moment of our lives should be a celebration of that.
    “I’m not saying that we always have to be happy, or that life always has to be perfect. But I do believe that we should strive to cultivate happiness and positivity in all areas of our lives, and that we should surround ourselves with people and things that bring us joy.
    “I believe that when we are surrounded by negativity, fear, and judgment, it can dull our light and keep
    27.77907705307007
