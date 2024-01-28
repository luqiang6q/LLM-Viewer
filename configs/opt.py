from transformers import OPTForCausalLM

def get_num_attention_heads(config):
    return getattr(config, "num_attention_heads")

def get_hidden_size(config):
    return getattr(config, "hidden_size")

def get_num_key_value_heads(config):
    return getattr(config, "num_attention_heads")

def get_num_hidden_layers(config):
    return getattr(config, "num_hidden_layers")

def get_transformer_layers(model:OPTForCausalLM):
    return model.model.decoder.layers

lm_head_name="lm_head"