AI Model Efficiency Toolkit (AIMET) is a software toolkit for quantizing and compressing models to enable efficient inference on edge devices with fixed-point AI accelerators.

AIMET uses post-training and fine-tuning techniques to optimize pre-trained floating-point (for example, FP32) models to minimize accuracy loss due to quantization or compression.

The following figure shows a high-level view of the AIEMT workflow. 

.. image:: ../../images/AIMET_index_no_fine_tune.png

You start with a trained model in the PyTorch, TensorFlow, or Keras training framework. This trained model is passed to AIMET using APIs for quantization and compression. AIMET returns a quantized and compressed version of the model that you fine-tune (or train further for a small number of epochs) to recover lost accuracy. You then export via ONNX, meta, or h5 to an on-target runtime like Qualcomm\ |reg| Neural Processing SDK.
