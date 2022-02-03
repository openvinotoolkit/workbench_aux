"""
 OpenVINO DL Workbench Python Starter
 Setup for the DL Workbench Python Starter

 Copyright (c) 2021 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import os
import platform

from pkg_resources import parse_requirements
from setuptools import setup

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))


def extend_requirements(current_requirements: list, requirements_file_name: str) -> list:
    with open(os.path.join(PACKAGE_DIR, requirements_file_name)) as requirements_file:
        additional_requirements = [
            str(requirement) for requirement in parse_requirements(requirements_file)
        ]

        current_requirements.extend(additional_requirements)
        return current_requirements


# Collect requirements
REQUIRED_PACKAGES = []
REQUIRED_PACKAGES = extend_requirements(REQUIRED_PACKAGES, 'requirements-core.txt')

if platform.system() == 'Windows':
    REQUIRED_PACKAGES = extend_requirements(REQUIRED_PACKAGES, 'requirements-win.txt')

if platform.system() == 'Linux':
    REQUIRED_PACKAGES = extend_requirements(REQUIRED_PACKAGES, 'requirements-linux.txt')

# Read documentation which will be showed on PyPI
with open('README.md', 'r', encoding='utf-8') as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name='openvino-workbench',
    author='Intel® Corporation',
    author_email='openvino_pushbot@intel.com',
    license='OSI Approved :: Apache Software License',
    description='DL Workbench is an official UI environment of the OpenVINO™ toolkit.',
    url='https://github.com/openvinotoolkit/workbench_aux',
    version='2021.4.2',
    packages=['openvino_workbench'],
    install_requires=REQUIRED_PACKAGES,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    project_urls={
        'Documentation':
            'https://docs.openvino.ai/latest/workbench_docs_Workbench_DG_Introduction.html',
        'Feedback':
            'https://community.intel.com/t5/Intel-Distribution-of-OpenVINO/bd-p/distribution-openvino-toolkit',
        'Troubleshooting':
            'https://community.intel.com/t5/Intel-Distribution-of-OpenVINO/bd-p/distribution-openvino-toolkit'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': ['openvino-workbench=openvino_workbench.main:main']
    }
)
