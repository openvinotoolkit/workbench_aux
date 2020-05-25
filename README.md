# OpenVINO DL Workbench

## Table of Contents

- [About](#about)
- [Licence](#licence)
- [Downloading Installation Script](#install-script)
- [Starting DL Workbench](#running)

## <a id="about">About</a>
DL Workbench is a web-based graphical environment that enables users to visualize, fine-tune, and 
compare performance of deep learning models on various Intel® architecture configurations, such as CPU,
Intel® Processor Graphics (GPU), Intel® Movidius™ Neural Compute Stick 2 (NCS 2), and Intel® Vision Accelerator Design with Intel® Movidius™ VPUs.

DL Workbench is a part of [OpenVINO Toolkit](https://github.com/openvinotoolkit/openvino).

## <a id="licence">Licence</a>
DL Workbench is licensed under [Apache License Version 2.0](LICENSE).
By contributing to the project, you agree to the license and copyright terms therein 
and release your contribution under these terms.

## <a id="install-script">Downloading Installation Script</a>

To **start** or **update** DL Workbench, you should run the `starting script`. You can either download the script manually, or use the following wget command to download it:
```sh
wget https://raw.githubusercontent.com/openvinotoolkit/workbench_aux/master/start_workbench.sh
```

When the script downloading process is complete, proceed to the [Starting DL Workbench](#running) section.

## <a id="running">Starting DL Workbench</a>

You can start the latest version of DL Workbench with the following command:
```bash
./start_workbench.sh -IMAGE_NAME openvino/workbench
```

> **NOTE**: To see the list of available arguments in a terminal, run the following command:
> ```bash
> ./start_workbench.sh --help
> ```

Refer to [documentation](./docs/Install_from_Docker_Hub.md) for additional information.
