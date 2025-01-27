from ..base_parser import BaseParser
from net_graph.module import Module
from net_graph.base_nodes import *
from net_graph.network import Network
from transformers import AutoConfig
from types import SimpleNamespace


class LLMParser(BaseParser):
    def __init__(self, model_id, args: dict):
        super().__init__(model_id, args)
        if model_id is None:
            self.p = SimpleNamespace(**args)
        else:
            self.p = AutoConfig.from_pretrained(model_id, trust_remote_code=True)

    def parse(self):
        use_flashattention = self.args.get("use_flashattention", False)

        modules=[]
        embedding=Module(name="embedding", nodes=[
        Embedding("embeded_feature", ["input_inds"], {"out_features":self.p.hidden_size, "vocab_size":self.p.vocab_size})])
        modules.append(embedding)

        for i in range(self.p.num_hidden_layers):
            if i==0:
                input_name="embedding.embeded_feature"
            else:
                input_name=f"transformer_layer{i-1}.mlp_add"
            nodes=[
                Norm("attn_norm", [input_name]),
                Linear("q_proj", ["attn_norm"], {"out_features":self.p.hidden_size}),
                LinearWithStoreKVCache("k_proj", ["attn_norm"], {"out_features":self.p.hidden_size//self.p.num_attention_heads*self.p.num_key_value_heads}),
                LinearWithStoreKVCache("v_proj", ["attn_norm"], {"out_features":self.p.hidden_size//self.p.num_attention_heads*self.p.num_key_value_heads}),
                ReshapeTranspose("q_reshape", ["q_proj"], {"shape":["input_shape[0]",self.p.num_attention_heads,"input_shape[1]", self.p.hidden_size//self.p.num_attention_heads]}),
                ReshapeTranspose("k_reshape", ["k_proj"], {"shape":["input_shape[0]",self.p.num_key_value_heads,self.p.hidden_size//self.p.num_attention_heads,"input_shape[1]"]}),
                ReshapeTranspose("v_reshape", ["v_proj"], {"shape":["input_shape[0]",self.p.num_key_value_heads,"input_shape[1]", self.p.hidden_size//self.p.num_attention_heads]})
            ]
            if use_flashattention:
                nodes.extend([
                    FlashAttention("flash_attention", ["q_reshape", "k_reshape", "v_reshape"]),
                    ReshapeTranspose("sv_reshape", ["flash_attention"], {"shape":["input_shape[0]","input_shape[2]", self.p.hidden_size]}),
                ])
            else:
                nodes.extend([
                    MatmulWithLoadKVCache("qk_matmul", ["q_reshape", "k_reshape"], {"concat_dim":-1}),
                    Softmax("softmax", ["qk_matmul"]),
                    MatmulWithLoadKVCache("sv_matmul", ["softmax", "v_reshape"], {"concat_dim":-2}),
                    ReshapeTranspose("sv_reshape", ["sv_matmul"], {"shape":["input_shape[0]","input_shape[2]", self.p.hidden_size]}),
                ])
            nodes+=[
                Linear("out_proj", ["sv_reshape"], {"out_features":self.p.hidden_size}),
                Add("attn_add", [input_name, "out_proj"]),
                Norm("mlp_norm", ["attn_add"]),
                Linear("gate_proj", ["mlp_norm"], {"out_features":self.p.intermediate_size}),
                Linear("up_proj", ["mlp_norm"], {"out_features":self.p.intermediate_size}),
                Activation("mlp_act", ["up_proj", "gate_proj"]),
                Linear("down_proj", ["mlp_act"], {"out_features":self.p.hidden_size}),
                Add("mlp_add", ["attn_add", "down_proj"])
            ]
            transformer_layer=Module(name=f"transformer_layer{i}",nodes=nodes)
            modules.append(transformer_layer)

        lm_head=Module(name="lm_head", nodes=[
            Norm("lm_head_norm", [f"transformer_layer{self.p.num_hidden_layers-1}.mlp_add"]),
            Linear("lm_head", ["lm_head_norm"], {"out_features":self.p.vocab_size})
        ])
        modules.append(lm_head)

        return Network(modules=modules)
