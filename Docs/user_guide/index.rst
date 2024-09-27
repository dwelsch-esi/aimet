.. role:: hideitem
   :class: hideitem
.. _ug-index:

######################################
AI Model Efficiency Toolkit User Guide
######################################

AIMET supports PyTorch, TensorFlow, and Keras model frameworks. Further, there are two versions of the AIMET API for PyTorch: the original version 1 framwork and the newer version 2 framework, on which all new API development is underway. To begin, select a framework. 

There are significant differences in the implementaion and use of AIMET between frameworks, so this documentation is split by framework into separate documentation sets. 

.. tabs::

   .. tab:: **PyTorch version 2**

      We recommend using PyTorch version 2, the most popular and feature-rich option. 

      :doc:`Go to the PyTorch version 2 documentation. </user_guide/pytorch2/index>`

   .. tab:: **PyTorch version 1**

      PyTorch version 1 is still available but will eventually be deprecated. 

      :doc:`Go to the PyTorch version 1 documentation. </user_guide/pytorch1/index>`

   .. tab:: **TensorFlow or Keras**

      Use TensorFlow if you're already invested in that framework.

      :doc:`Go to the TensorFlow/Keras documentation. </user_guide/tf/index>`

   .. tab:: **ONNX**

      ONNX provides portability but lacks development features.

      :doc:`Go to the ONNX documentation. </user_guide/onnx/index>`
|

|

| |project| is a product of |author|
| Qualcomm\ |reg| Neural Processing SDK is a product of Qualcomm Technologies, Inc. and/or its subsidiaries.

.. |reg|    unicode:: U+000AE .. REGISTERED SIGN
