# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from paddle.utils import try_import

__all__ = ['export']


def export(layer, save_file, input_spec=None, opset_version=9, **kwargs):
    """
    Export declarative Layer as ONNX format model, which can be used for inference.
    Now, it supports a limited operater set and dynamic models.(e.g., MobileNet.)
    More features and introduction, Please reference the https://github.com/PaddlePaddle/paddle2onnx
    
    Args:
        layer (Layer): the Layer to be saved. The Layer should be staticed by `paddle.jit.to_static`.
        save_file (str): the file name to save the onnx model.
        input_spec (list[Variable], optional): Describes the input of the saved model. 
            It is the example inputs that will be passed to saved ONNX model.
            If None, all input variables of the original Layer's forward function
            would be the inputs of the saved ONNX model. Default None.
        opset_version(int, optinal): opset version of exported ONNX model.
            Now, supported opset version include 9, 10, 11. Default 9.
        kwargs: Additional keyword parameters. currently supports 'output_spec', 
            which describes the output of the saved model.
    Returns:
        None
    Examples:
        .. code-block:: python
        import paddle
        import numpy as np
        
        class Model(paddle.nn.Layer):
            def __init__(self):
                super(Model, self).__init__()
        
            def forward(self, x, y, z=False):
                if z:
                    return x + y, x - y
                else:
                    return x * y, x / y
        
        def export_with_input_spec():
            paddle.fluid.enable_dygraph() 
            model = Model()
            x_spec = paddle.static.InputSpec(shape=[None, 4], dtype='float32', name='x')
            y_spec = paddle.static.InputSpec(shape=[None, 4], dtype='float32', name='y')
            model = paddle.jit.to_static(model, input_spec=[x_spec, y_spec])
            paddle.onnx.export(model, 'dynamic_input.onnx', input_spec=[x_spec, y_spec])
        
        def export_with_input_variable():
            paddle.fluid.enable_dygraph() 
            model = Model()
            x =  paddle.fluid.dygraph.to_variable(np.array([1]).astype('float32'), name='x')
            y =  paddle.fluid.dygraph.to_variable(np.array([1]).astype('float32'), name='y')
            model = paddle.jit.to_static(model)
            out = model(x, y, z=True)
            paddle.onnx.export(model, 'pruned.onnx', input_spec=[x, y], output_spec=[out[0]])

        #export model with InputSpec, which support set dynamic shape for input.
        export_with_input_spec()

        #export model with Variable, which support prune model by set 'output_spec' with output of model.
        export_with_input_variable()
    """

    p2o = try_import('paddle2onnx')

    p2o.convert_dygraph_to_onnx(
        layer, save_file, input_spec=input_spec, opset_version=9, **kwargs)
