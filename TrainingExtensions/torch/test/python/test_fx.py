# /usr/bin/env python3.5
# -*- mode: python -*-
# =============================================================================
#  @@-COPYRIGHT-START-@@
#
#  Copyright (c) 2021, Qualcomm Innovation Center, Inc. All rights reserved.
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

import pytest
import json
import os
import copy
from packaging import version
import torch
from torchvision import models

from aimet_torch import elementwise_ops
from aimet_torch.quantsim_config import quantsim_config
from aimet_torch.examples.test_models import ModelWithFunctionalReLU, SingleResidual, ModelWithDuplicateReLU
from aimet_torch.quantsim import QuantizationSimModel


class TestFX:


    def test_fx_with_relu(self):
        """
        test torch fx with functional ReLUs
        """
        if version.parse(torch.__version__) >= version.parse("1.8"):
            from aimet_torch.fx import replace_functional_by_module
            input_shape = (1, 3, 32, 32)
            input_tensor = torch.randn(*input_shape)
            model = ModelWithFunctionalReLU().eval()
            model_copy = copy.deepcopy(model)

            model_transformed = replace_functional_by_module(model_copy)
            print(model_transformed)

            assert isinstance(model_transformed.module_relu, torch.nn.ReLU)
            assert isinstance(model_transformed.module_relu_1, torch.nn.ReLU)
            assert isinstance(model_transformed.module_relu_2, torch.nn.ReLU)
            assert isinstance(model_transformed.module_relu_3, torch.nn.ReLU)

            assert torch.allclose(model(input_tensor), model_transformed(input_tensor))

    def test_fx_with_add(self):
        """
        test torch fx with elementwise Add
        """
        if version.parse(torch.__version__) >= version.parse("1.8"):
            from aimet_torch.fx import replace_functional_by_module
            input_shape = (1, 3, 32, 32)
            input_tensor = torch.randn(*input_shape)
            model = SingleResidual().eval()
            model_copy = copy.deepcopy(model)

            model_transformed = replace_functional_by_module(model_copy)
            print(model_transformed)

            assert isinstance(model_transformed.module_add, elementwise_ops.Add)
            assert torch.allclose(model(input_tensor), model_transformed(input_tensor))

    def test_fx_with_duplicate_relu(self):
        """
        test torch fx with Duplicate/Reused module ReLU
        """
        if version.parse(torch.__version__) >= version.parse("1.8"):
            from aimet_torch.fx import replace_functional_by_module
            input_shape = (1, 3, 32, 32)
            input_tensor = torch.randn(*input_shape)
            model = ModelWithDuplicateReLU().eval()
            model_copy = copy.deepcopy(model)

            model_transformed = replace_functional_by_module(model_copy)

            assert isinstance(model_transformed.relu, torch.nn.ReLU)
            assert isinstance(model_transformed.module_relu_1, torch.nn.ReLU)
            assert isinstance(model_transformed.module_relu_2, torch.nn.ReLU)
            assert isinstance(model_transformed.module_relu_3, torch.nn.ReLU)

            assert torch.allclose(model(input_tensor), model_transformed(input_tensor))

    def test_fx_with_resnet18(self):
        """
        test torch fx with torchvision Resnet18
        """
        if version.parse(torch.__version__) >= version.parse("1.8"):
            from aimet_torch.fx import replace_functional_by_module
            input_shape = (1, 3, 224, 224)
            input_tensor = torch.randn(*input_shape)
            model = models.resnet18().eval()
            model_copy = copy.deepcopy(model)

            model_transformed = replace_functional_by_module(model_copy)
            print(model_transformed)

            assert torch.allclose(model(input_tensor), model_transformed(input_tensor))

    @pytest.mark.cuda
    def test_fx_with_resnet18_with_cuda(self):
        """
        test torch fx with torchvision Resnet18 CUDA
        """
        if version.parse(torch.__version__) >= version.parse("1.8"):
            from aimet_torch.fx import replace_functional_by_module
            input_shape = (1, 3, 224, 224)
            input_tensor = torch.randn(*input_shape).cuda()
            model = models.resnet18().cuda().eval()
            model_copy = copy.deepcopy(model)

            model_transformed = replace_functional_by_module(model_copy)
            print(model_transformed)

            assert torch.allclose(model(input_tensor), model_transformed(input_tensor))

    def test_fx_with_functional_relu_quantsim(self):
        """
        test torch fx with QuantSim
        """
        if version.parse(torch.__version__) >= version.parse("1.8"):
            from aimet_torch.fx import replace_functional_by_module
            input_shape = (1, 3, 32, 32)
            input_tensor = torch.randn(*input_shape)
            model = ModelWithFunctionalReLU().eval()
            model_copy = copy.deepcopy(model)

            model_transformed = replace_functional_by_module(model_copy)

            quant_sim_for_modified_model = QuantizationSimModel(model_transformed, dummy_input=input_tensor)
            print(quant_sim_for_modified_model)

            # Conv --> ReLU supergroup is detected correctly
            assert quant_sim_for_modified_model.model.conv1.output_quantizer.enabled == False
            assert quant_sim_for_modified_model.model.module_relu.output_quantizer.enabled == True

            assert quant_sim_for_modified_model.model.conv2.output_quantizer.enabled == False
            assert quant_sim_for_modified_model.model.module_relu_1.output_quantizer.enabled == True

            assert quant_sim_for_modified_model.model.fc1.output_quantizer.enabled == False
            assert quant_sim_for_modified_model.model.module_relu_2.output_quantizer.enabled == True

            assert quant_sim_for_modified_model.model.fc2.output_quantizer.enabled == False
            assert quant_sim_for_modified_model.model.module_relu_3.output_quantizer.enabled == True

    def test_fx_with_functional_relu_quantsim_eval(self):
        """
        test torch fx with QuantSim evaluation
        """
        if version.parse(torch.__version__) >= version.parse("1.8"):
            from aimet_torch.fx import replace_functional_by_module
            input_shape = (1, 3, 32, 32)
            input_tensor = torch.randn(*input_shape)
            model = ModelWithFunctionalReLU().eval()
            model_copy = copy.deepcopy(model)

            model_transformed = replace_functional_by_module(model_copy)

            quantsim_config = {
                "defaults": {
                    "ops": {
                        "is_output_quantized": "True",
                        "is_symmetric": "False"
                    },
                    "params": {
                        "is_quantized": "True",
                        "is_symmetric": "True"
                    }
                },
                "params": {},
                "op_type": {},
                "supergroups": [],
                "model_input": {},
                "model_output": {}
            }
            with open('./data/quantsim_config.json', 'w') as f:
                json.dump(quantsim_config, f)

            quant_sim_for_original_model = QuantizationSimModel(model, dummy_input=input_tensor,
                                                                config_file='./data/quantsim_config.json')

            quant_sim_for_modified_model = QuantizationSimModel(model_transformed, dummy_input=input_tensor,
                                                                config_file='./data/quantsim_config.json')

            # Disable output activation quantizer for ReLUs to compare with original quantsim.model eval
            quant_sim_for_modified_model.model.module_relu.output_quantizer.enabled = False
            quant_sim_for_modified_model.model.module_relu_1.output_quantizer.enabled = False
            quant_sim_for_modified_model.model.module_relu_2.output_quantizer.enabled = False
            quant_sim_for_modified_model.model.module_relu_3.output_quantizer.enabled = False

            def model_eval(model: torch.nn.Module, dummy_input: torch.Tensor):
                model.eval()
                with torch.no_grad():
                    model(dummy_input)

            quant_sim_for_original_model.compute_encodings(model_eval, input_tensor)
            quant_sim_for_modified_model.compute_encodings(model_eval, input_tensor)

            # Eval for both models
            assert torch.allclose(quant_sim_for_original_model.model(input_tensor),
                                  quant_sim_for_modified_model.model(input_tensor))

            # Compare encodings for last layer for both models
            assert quant_sim_for_original_model.model.fc2.output_quantizer.encoding.min ==\
                   quant_sim_for_modified_model.model.fc2.output_quantizer.encoding.min

            if os.path.exists('./data/quantsim_config.json'):
                os.remove('./data/quantsim_config.json')

    def test_fx_with_elementwise_add_quantsim(self):
        """
        test torch fx with elementwise Add
        """
        if version.parse(torch.__version__) >= version.parse("1.8"):
            from aimet_torch.fx import replace_functional_by_module
            input_shape = (1, 3, 32, 32)
            input_tensor = torch.randn(*input_shape)
            model = SingleResidual().eval()
            model_copy = copy.deepcopy(model)

            model_transformed = replace_functional_by_module(model_copy)
            print(model_transformed)

            assert isinstance(model_transformed.module_add, elementwise_ops.Add)
            assert torch.allclose(model(input_tensor), model_transformed(input_tensor))

            quantsim_config.ELEMENTWISE_OP_TYPES = []
            quant_sim_for_modified_model = QuantizationSimModel(model_transformed, dummy_input=input_tensor)
            print(quant_sim_for_modified_model)

            # Add + ReLU Supergroup
            # Add's output quantizer should be disabled, and ReLU's output quantizer should be enabled
            assert quant_sim_for_modified_model.model.module_add.output_quantizer.enabled == False
            assert quant_sim_for_modified_model.model.relu3.output_quantizer.enabled == True
