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

#############
Starting the Docker Container
#############

Prerequisites
~~~~~~~~~~~~~

* Install AIMET in a Docker container. 
* Define `WORKSPACE`, `docker_container_name`, and `docker_image_name`.

See :doc:`torch_install_docker`.

Procedure
~~~~~~~~~

Step 1
------

Ensure that a docker named `$docker_container_name` is not already running:

.. code-block:: bash

    docker ps -a | grep ${docker_container_name} && docker kill ${docker_container_name}

Step 2
------

Run the container from the command line:

.. code-block:: bash

    docker run --rm -it -u $(id -u ${USER}):$(id -g ${USER}) \
    -v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro \
    -v ${HOME}:${HOME} -v ${WORKSPACE}:${WORKSPACE} \
    -v "/local/mnt/workspace":"/local/mnt/workspace" \
    --entrypoint /bin/bash -w ${WORKSPACE} --hostname ${docker_container_name} ${docker_image_name}


.. admonition:: NOTE
   
    * Modify the `docker run` command based on the environment and filesystem on your host machine.
   
    * If nvidia-docker 2.0 is installed, add `--gpus all` to the `docker run` command in order to enable GPU access inside the docker container.

    * If nvidia-docker 1.0 is installed, replace `docker run` with `nvidia-docker run` to enable GPU access inside the docker container.
    
    * To run the Visualization APIs from docker container, enable port forwarding by adding this option to the `docker run` command:
      -p ${port_id}:${port_id} 

Next Steps
~~~~~~~~~~

:doc:`Test AIMET in the Docker container <test_aimet_docker>`.