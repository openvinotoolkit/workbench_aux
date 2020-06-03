# OpenVINO™ Deep Learning Workbench

## Table of Contents

- [About](#about)
- [License](#license)
- [Install DL Workbench](#install)
    - [Single-Line Start](#single-line-start)
    - [Step-by-Step Start](#manual-start)
- [Useful Links](#links)

## <a id="about">About</a>

[OpenVINO](https://github.com/openvinotoolkit/openvino)™ DL Workbench is a web-based
graphical environment that enables users to visualize, fine-tune, and compare performance of deep
learning models on various Intel® architecture configurations, such as CPU, Intel® Processor
Graphics (GPU), Intel® Movidius™ Neural Compute Stick 2 (NCS 2), and Intel® Vision Accelerator
Design with Intel® Movidius™ VPUs.

The intuitive web-based interface of the DL Workbench allows you to easily use various sophisticated OpenVINO™ toolkit components:

* [Model Downloader](https://docs.openvinotoolkit.org/latest/_tools_downloader_README.html) to
    download models from the Intel® 
    [Open Model Zoo](https://docs.openvinotoolkit.org/latest/_models_intel_index.html) with pretrained 
    models for a range of different tasks

* [Model Optimizer](https://docs.openvinotoolkit.org/latest/_docs_MO_DG_Deep_Learning_Model_Optimizer_DevGuide.html)
    to transform models into the Intermediate Representation (IR) format

* [Post-Training Optimization tool](https://docs.openvinotoolkit.org/latest/_README.html) to
  calibrate a model and then execute it in the INT8 precision

* [Accuracy Checker](https://docs.openvinotoolkit.org/latest/_tools_accuracy_checker_README.html) to
  determine the accuracy of a model

## <a id="license">License</a>

DL Workbench is licensed under the [Apache License Version 2.0](LICENSE). By contributing to the
project, you agree to the license and copyright terms therein and release your contribution under
these terms.

## <a id="install">Install DL Workbench</a>

This section describes how to start the DL Workbench using the `start_workbench.sh` script, which
works on Linux OS\* and macOS\*.

For other installation, see [Install DL Workbench](./docs/Install_DL_Workbench.md).        
For additional details, such as prerequisites, security, and troubleshooting, see 
[OpenVINO DL Workbench documentation](https://docs.openvinotoolkit.org/latest/_docs_Workbench_DG_Introduction.html).

To start or update the DL Workbench, run the starting script with a single-line command or manually.
Two sections below describe the both options.

> **IMPORTANT**: To download the script using the command line, you must have GNU Wget or cURL installed.

#### <a id="single-line-start">Single-Line Start</a>

Choose one of the options:
* Single-line command with GNU Wget:
```bash
wget https://raw.githubusercontent.com/openvinotoolkit/workbench_aux/master/start_workbench.sh && bash start_workbench.sh
```

* Single-line command with cURL:
```bash
curl -o start_workbench.sh https://raw.githubusercontent.com/openvinotoolkit/workbench_aux/master/start_workbench.sh && bash start_workbench.sh
```

> **NOTE**: Execution of any of the above commands starts the DL Workbench in the interactive mode
> with CPU support only. Go to the <a href="#args">List of All Arguments</a> for other options.

#### <a id="manual-start">Step-by-Step Start</a>

1. Choose one of the options to download the script:
   * Download with GNU Wget:
   ```bash
   wget https://raw.githubusercontent.com/openvinotoolkit/workbench_aux/master/start_workbench.sh
   ```
   * Download with cURL:
   ```bash
   curl -o start_workbench.sh https://raw.githubusercontent.com/openvinotoolkit/workbench_aux/master/start_workbench.sh
   ```

2. Open a terminal in the directory with the downloaded script and run the following command to make
   the file executable:
```bash
chmod +x start_workbench.sh
```

3. Run the Docker container with the highest available version of the DL Workbench with the
   following command: 
```
./start_workbench.sh -IMAGE_NAME openvino/workbench
```

> **NOTE**: To see the list of available arguments in a terminal, run the following command:
> ```bash
> ./start_workbench.sh --help
> ```

## <a id="links">Useful Links</a>

* [OpenVINO DL Workbench Documentation](https://docs.openvinotoolkit.org/latest/_docs_Workbench_DG_Introduction.html)
* [Support Forum](https://software.intel.com/en-us/forums/intel-distribution-of-openvino-toolkit)
* [Release Notes](https://software.intel.com/content/www/us/en/develop/articles/openvino-relnotes.html#inpage-nav-2-7)
