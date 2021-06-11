# OpenVINO™ Deep Learning Workbench Python Starter

Copyright © 2018-2021 Intel Corporation

> LEGAL NOTICE: Your use of this software and any required dependent software (the “Software Package”) is subject to the terms and conditions of the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0.html).

## Introduction

Deep Learning Workbench is a web-based graphical environment with a convenient user-friendly interface and a wide range of customization options designed to make the development of deep learning models significantly easier. 

The DL Workbench is an official UI environment of the OpenVINO™ toolkit that enables you to:

- Learn what neural networks are, how they work, and how to analyze their architectures and performance.
- Get familiar with the OpenVINO™ ecosystem and its main components without installing it on your system.
- Measure and interpret model performance.
- Analyze the quality of your model and visualize output.
- Optimize your model and prepare it for deployment on the target system.

In the DL Workbench, you can use the following OpenVINO™ toolkit components:

Component  |                 Description 
|:------------------:|:------------------|
| [Model Downloader and Model Converter](https://docs.openvinotoolkit.org/latest/omz_tools_downloader.html)| **Model Downloader** is a tool for getting access to the collection of high-quality pre-trained deep learning [public](https://docs.openvinotoolkit.org/latest/omz_models_group_public.html) and [Intel](https://docs.openvinotoolkit.org/latest/omz_models_group_intel.html)-trained models. The tool downloads model files from online sources and, if necessary, patches them with Model Optimizer. <br> **Model Converter** is a tool for converting the models stored in a format other than the Intermediate Representation (IR) into that format using Model Optimizer. |
| [Model Optimizer](https://docs.openvinotoolkit.org/latest/openvino_docs_MO_DG_Deep_Learning_Model_Optimizer_DevGuide.html) |**Model Optimizer** imports, converts, and optimizes models that were trained in certain frameworks to the IR format used in OpenVINO tools. <br>Supported frameworks include TensorFlow\*, Caffe\*, Kaldi*\*, MXNet\*, and ONNX\*.  
| [Benchmark Tool](https://docs.openvinotoolkit.org/latest/openvino_inference_engine_tools_benchmark_tool_README.html)| **Benchmark Application** allows you to estimate deep learning inference performance on supported devices for synchronous and asynchronous modes.   
| [Accuracy Checker](https://docs.openvinotoolkit.org/latest/omz_tools_accuracy_checker.html) |**Accuracy Checker**  is a deep learning accuracy validation tool that allows you to evaluate accuracy on the given dataset by collecting one or several metric values. 
| [Post-Training Optimization Tool](https://docs.openvinotoolkit.org/latest/pot_README.html)|**Post-Training Optimization Tool** allows you to optimize trained models with advanced capabilities, such as quantization and low-precision optimizations, without the need to retrain or fine-tune models.                               |


## System Requirements

The complete list of recommended requirements is available in the [documentation](https://docs.openvinotoolkit.org/latest/workbench_docs_Workbench_DG_Prerequisites.html).

To successfully run the DL Workbench with Python Starter, install Python 3.6 or higher.

Prerequisite | Linux* | Windows* | macOS*
:----- | :----- |:----- |:-----
Operating system|Ubuntu\* 18.04|Windows\* 10 | macOS\* 10.15 Catalina
Available RAM space| 8 GB\** | 8 GB\** | 8 GB\**
Available storage space| 10 GB + space for imported artifacts| 10 GB + space for imported artifacts| 10 GB + space for imported artifacts
Docker\*| Docker CE 18.06.1 | Docker Desktop 2.3.0.3|Docker CE 18.06.1

Windows*, Linux* and MacOS* support CPU targets. GPU, Intel® Neural Compute Stick 2 and Intel® Vision Accelerator Design with Intel® Movidius™ VPUs are supported only for Linux*.

## Install the DL Workbench Starter

### Step 1. Set Up Python Virtual Environment

To avoid dependency conflicts, use a virtual environment. Skip this step only if you do want to install all dependencies globally.

Create virtual environment by executing the following commands in your terminal:

* On Linux and MacOS:
```
python3 -m pip install --user virtualenv
python3 -m venv venv
```
* On Windows:
```
py -m pip install --user virtualenv
py -m venv venv
```
### Step 2. Activate Virtual Environment

* On Linux and MacOS:
```
source venv/bin/activate
```
* On Windows:
```
venv\Scripts\activate
```

### Step 3. Update PIP to the Latest Version
Run the command below:

```
python -m pip install --upgrade pip
```
### Step 4. Install the Python Wrapper
```
pip install -U openvino-workbench
```
### Step 5. Verify the Installation

To verify that the package is properly installed, run the command below:
```
openvino-workbench --help
```
You will see the help message for the starting package if installation finished successfully.

## Use the DL Workbench Starter

To start the latest available version of the DL Workbench, execute the following command:

```
openvino-workbench --image openvino/workbench:2021.4
```

You can see the list of available arguments with the following command:
```
openvino-workbench --help
```

Refer to the [documentation](https://docs.openvinotoolkit.org/latest/workbench_docs_Workbench_DG_Introduction.html) for additional information.

# Additional Resources
* [Release Notes](https://software.intel.com/content/www/us/en/develop/articles/openvino-relnotes.html)
* [Documentation](https://docs.openvinotoolkit.org/latest/workbench_docs_Workbench_DG_Introduction.html)
* [Feedback](https://community.intel.com/t5/Intel-Distribution-of-OpenVINO/bd-p/distribution-openvino-toolkit)
* [Troubleshooting](https://community.intel.com/t5/Intel-Distribution-of-OpenVINO/bd-p/distribution-openvino-toolkit)
