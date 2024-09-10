.. # =============================================================================
   #  @@-COPYRIGHT-START-@@
   #
   #  Copyright (c) 2022-2023, Qualcomm Innovation Center, Inc. All rights reserved.
   #
   #  Redistribution and use in source and binary forms, with or without
   #  modification, are permitted provided that the following conditions are met:
   #
   #  1. Redistributions of source code must retain the above copyright notice,
   #     this list of conditions and the following disclaimer.
   #
   #  2. Redistributions in binary form must reproduce the above copyright notice,
   #     this list of conditions and the following disclaimer in the documentation
   #     and/or other materials provided with the distribution.
   #
   #  3. Neither the name of the copyright holder nor the names of its contributors
   #     may be used to endorse or promote products derived from this software
   #     without specific prior written permission.
   #
   #  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
   #  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   #  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   #  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
   #  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
   #  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
   #  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
   #  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
   #  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
   #  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
   #  POSSIBILITY OF SUCH DAMAGE.
   #
   #  SPDX-License-Identifier: BSD-3-Clause
   #
   #  @@-COPYRIGHT-END-@@
   # =============================================================================

##################################
AIMET ONNX Installation in Docker
##################################

This page provides instructions to install the ONNX AIMET package inside a development Docker container.

Prerequisites
~~~~~~~~~~~~~

ONNX installation of AIMET in Docker requires the following host platform setup:

* 64-bit Intel x86-compatible processor
* Linux Ubuntu: 22.04 LTS
* bash command shell
* For GPU variants:
    * Nvidia GPU card (Compute capability 5.2 or later)
    * nvidia-docker - Installation instructions: https://github.com/NVIDIA/nvidia-docker
* For GPU acceleration: 
    * An Nvidia CUDA-enabled GPU. Both CUDA and cuDNN-enabled (the more advanced CUDA interface) GPUs are supported.
    * An Nvidia driver, version 455  or later. (The latest driver is always recommended, especially if using a newer GPU.)
* Create a workspace directory on the system where you will check out the code and build and run the Docker image.

Procedure
~~~~~~~~~

Step 1: Set the workspace
-------------------------

Set the workspace to the directory created in the prerequisites:

.. code-block:: bash

    WORKSPACE="<absolute_path_to_workspace>"

Step 2: Set the Docker container name
-------------------------------------

Choose and set a name for the container. You can choose an arbitrary name for the container; we recommend including "aimet" in the name:

.. code-block:: bash

    docker_container_name="aimet-dev-<any_name>"

Step 3: Set the variant
----------------------------------

Set the variant to one of the ONNX variants by setting `AIMET_VARIANT`:

.. code-block:: bash

    export AIMET_VARIANT=<variant_string>

where `variant_string` is one of:

========= ===============
ONNX Docker variants
-------------------------
Variant   variant_string
========= ===============
ONNX GPU   onnx-gpu
ONNX CPU   onnx-cpu

Step 4: Set the image name
--------------------------

Set the image name. Do one of the following:

- If you are using a prebuilt Docker image, do the following:

.. code-block:: bash

    docker_image_name="artifacts.codelinaro.org/codelinaro-aimet/aimet-dev:latest.${AIMET_VARIANT}"

- If you are building the Docker image locall, you can choose an arbitrary name for the image; we recommend including "aimet" in the name:

.. code-block:: bash

    docker_image_name="aimet-dev-docker:<any_tag>"


Step 5: (optional) Build the Docker image locally
---------------------------------------------

To build the docker image locally, run the following command. If you're using a pre-built Docker image, skip this step.

.. code-block:: bash

    docker build -t ${docker_image_name} -f $WORKSPACE/aimet/Jenkins/Dockerfile.${AIMET_VARIANT} .


Next Steps
~~~~~~~~~~

:doc:`Start the Docker container <docker_start>`.