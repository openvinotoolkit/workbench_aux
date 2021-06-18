# DL Workbench Python Starter

## Publish the DL Workbench Python starter

### Prerequisites
1. Make sure you have one of the latest Pythons installed (version >= 3.8)
> It is highly recommended doing the following steps using the virtual environment.
2. Install or upgrade `setuptools`, `wheel` for wheel building:
   * `python3 -m pip install -U setuptools wheel`
3. Install `twine` for package publishing:
   * `python3 -m pip install -U twine`
4. Clone the DL WB aux repository if you do not have it locally:
    * https://github.com/openvinotoolkit/workbench_aux

### Build wheel
1. Navigate into the repository root and in the `starting_package` folder;
   * Make sure you are on the desired branch (usually `master` with the latest version) with the version you want to publish.
2. **IMPORTANT**: Make sure you have incremented the package version:
   * File `setup.py`, `version` flag in the `setup` function;
   * Versioning: `YEAR.RELEASE_NUMBER.MINOR.PATCH`;
        * Example: `2021.4.0.1`
   * Increment the `PATCH` for fixes;
   * Increment the `MINOR` for minor new functionality;
   * The `YEAR.RELEASE_NUMBER` should be aligned with the OpenVINO version.
3. Build the wheel:
   * `python3 setup.py bdist_wheel`
4. The built wheel should appear in the `dist` folder;
   * Name example: `openvino_workbench-VERSION-py3-none-any.whl`
5. Check the built wheel with `twine`:
   * `twine check dist/*` 
    
### Verify the package
1. Unpack the `.whl` archive with the unpacking tool (e.g. `unzip`);
   * Make sure that all files are present, `README.md` and `METADATA` especially.
2. Install the package in the clean environment:
   * `python3 -m pip install openvino_workbench-VERSION-py3-none-any.whl`
3. Run the package with default parameters and make sure everything is ok:
   * `openvino-workbench`

### Publish the package (on the test PyPI)
1. Upload to the test repository:
    * `twine upload --repository testpypi dist/*`
    * You will be prompted for the username: use `__token__`;
    * Then you will be prompted for the password: ask `akashchi` or `artyomtugaryov` for the token.
2. After uploading there will be a link for the project on `testpypi`;
   * Verify the description, links, general package information.
3. Install the package in the clean environment:
   * `python3 -m pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple openvino-workbench==VERSION`
4. Run the package with default parameters and make sure everything is ok:
   * `openvino-workbench`

### Publish the package (on the PyPI)
1. Upload to the repository:
    * `twine upload dist/*`
    * You will be prompted for the username: use `__token__`
    * Then you will be prompted for the password: ask `akashchi` or `artyomtugaryov` for the token.
2. After uploading there will be a link for the project on `PyPI`;
   * Verify the description, links, general package information.
3. Install the package in the clean environment:
   * `python3 -m pip install openvino-workbench==VERSION`
4. Run the package with default parameters and make sure everything is ok:
   * `openvino-workbench`
