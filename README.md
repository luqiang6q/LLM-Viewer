# LLM-Viewer

<img src="figs/eye.png" alt="LLM-Viewer" width="50"/>


LLM-Viewer is a tool for visualizing Language and Learning Models (LLMs) and analyzing the performance on different hardware platforms. It enables network-wise analysis, considering factors such as peak memory consumption and total inference time cost. With LLM-Viewer, you can gain valuable insights into LLM inference and performance optimization.
You can use LLM-Viewer in a web browser or as a command line interface (CLI) tool. The web version provides a user-friendly interface for easy configuration and visualization, you can access it at [LLM-Viewer Web](http://llm-viewer.com).

We invite you to read our paper [LLM Inference Unveiled: Survey and Roofline Model Insights](https://arxiv.org/pdf/2402.16363.pdf).
In this paper, we provide a comprehensive analysis of the latest advancements in efficient LLM inference using LLM-Viewer. 

This ongoing project will be updated. TODO list:
- Show shape of tensors.
- Pre-process and post-process for non-transformer layers.
- Show the whole network.
- Expand hardware platform compatibility and allow manual configuration of hardware parameters.
- Increase support for more LLMs and enable manual configuration of model graphs.

## Workflow

![LLM-Viewer Workflow](figs/workflow.svg)

As shown in the Figure, the workflow consists of the following steps:

1. Input the LLM and gather essential information about each layer, including the computation count, input and output tensor shapes, and data dependencies.
2. Provide input for the hardware and generate a roofline model that takes into account the computation capacity and memory bandwidth of the hardware.
3. Configure the inference settings, such as the batch size, prompt token length, and generation token length.
4. Configure the optimization settings, such as the quantization bitwidth, utilization of FlashAttention, decoding methods, and other system optimization techniques.
5. Use the LLM-Viewer Analyzer to analyze the performance of each layer based on the roofline model and layer information. It also tracks the memory usage of each layer and calculates the peak memory consumption based on data dependencies. The overall network performance of the LLM can be obtained by aggregating the results of all layers.
6. Generate a report that provides information such as the maximum performance and performance bottlenecks of each layer and the network, as well as the memory footprint. The report can be used to analyze curves, such as batch size-performance and sequence length-performance curves, to understand how different settings impact performance.
7. Access the LLM-Viewer web viewer for convenient visualization of the network architecture and analysis results. This tool facilitates easy configuration adjustment and provides access to various data for each layer.

## Web Usage

To use LLM-Viewer in a web browser, go to the web-site [LLM-Viewer Web](http://llm-viewer.com).
You can click the node to get the detailed analysis of the layer.

You can click node/module to get node/module profile info.

## CLI Usage

Clone the LLM-Viewer repository from GitHub: 
```git clone https://github.com/hahnyuan/LLM-Viewer.git   ```

Install requirements
```pip install transformers flask flask_cors easydict numpy onnx onnxsim prettytable```

### Profile build-in LLM and SD models
To analyze an LLM using LLM-Viewer in command line interface (cli), run the following command:

```bash
python3 analyze_cli.py facebook/opt-125m nvidia_A6000
python3 analyze_cli.py meta-llama/Llama-2-7b-hf nvidia_A6000 --batchsize 1 --seqlen 2048
python3 analyze_cli.py meta-llama/Llama-2-13b-hf nvidia_A6000 --batchsize 16 --seqlen 2048
python3 analyze_cli.py meta-llama/Llama-2-13b-hf nvidia_A6000 --batchsize 1 --seqlen 8192

# stable_diffusion models
python3 analyze_cli.py stable_diffusion nvidia_A6000 --batchsize 1 --time_steps 20
```
The build-in models can be found in backend_settings.py.Now, support llama, Qwen, stable_diffusion.
The hardware info can be found in hardwares/hardware_params.py.

NOTE: The time estimated by the roofline model represents the theoretical performance that the hardware can achieve. 
The purpose of creating this tool is to help readers gain a clearer understanding of the key factors that influence LLM inference. 
Only the relative relationships can be referenced. 

### Profile Onnx
```bash
python3 analyze_cli.py OnnxFile nvidia_A6000 \
--model_path data/onnx/resnet50-v2-7.onnx \
--input_shape_info data:1,3,224,224 \
--w_bit 8 \
--a_bit 8 \
--compute_dtype INT8 \
--save_csv_path output/onnx_profile_resnet50.csv
```

NOTE: Onnx profile only support origin onnx OP.If you want to profile customize OP, add your node into net_parsers/onnx/node.py.

onnx profile info without hardware_profile:
![Onnx Profile Info without hardware_profile](figs/onnx_profile_info.png)
onnx profile info with hardware_profile:
![onnx profile info with hardware_profile](figs/onnx_profile_info_hardware.png)
## Citation

If you are using LLM-Viewer in your research, please cite our paper:

```
@misc{yuan2024llm,
      title={LLM Inference Unveiled: Survey and Roofline Model Insights}, 
      author={Zhihang Yuan and Yuzhang Shang and Yang Zhou and Zhen Dong and Chenhao Xue and Bingzhe Wu and Zhikai Li and Qingyi Gu and Yong Jae Lee and Yan Yan and Beidi Chen and Guangyu Sun and Kurt Keutzer},
      year={2024},
      eprint={2402.16363},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```