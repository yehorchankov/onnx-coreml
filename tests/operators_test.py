from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from onnx.numpy_helper import from_array

from tests._test_utils import _test_single_node, \
    _random_array, _conv_pool_output_size


class SingleOperatorTest(unittest.TestCase):

    def test_conv(self):  # type: () -> None
        kernel_shape = (3, 2)
        strides = (2, 3)
        pads = (4, 2, 4, 2)
        dilations = (1, 2)
        group = 1
        weight = from_array(_random_array((16, 3, 3, 2)), name="weight")

        input_shape = (1, 3, 224, 224)
        output_size = _conv_pool_output_size(input_shape, dilations,
                                             kernel_shape, pads, strides)

        output_shape = (1, int(weight.dims[0]), output_size[0], output_size[1])

        _test_single_node(
            "Conv",
            [input_shape],
            [output_shape],
            initializer=[weight],
            dilations=dilations,
            group=group,
            kernel_shape=kernel_shape,
            pads=pads,
            strides=strides
        )

    def test_conv_without_pads(self):  # type: () -> None
        kernel_shape = (3, 2)
        strides = (2, 3)
        dilations = (1, 2)
        group = 1
        weight = from_array(_random_array((16, 3, 3, 2)), name="weight")

        input_shape = (1, 3, 224, 224)
        output_size = _conv_pool_output_size(input_shape, dilations,
                                             kernel_shape, [0, 0, 0, 0],
                                             strides)

        output_shape = (1, int(weight.dims[0]), output_size[0], output_size[1])
        _test_single_node(
            "Conv",
            [input_shape],
            [output_shape],
            initializer=[weight],
            dilations=dilations,
            group=group,
            kernel_shape=kernel_shape,
            strides=strides
        )

    def test_max_pool(self):  # type: () -> None
        kernel_shape = (5, 3)
        pads = (2, 1, 2, 1)
        strides = (1, 2)

        input_shape = (1, 3, 224, 224)

        output_size = _conv_pool_output_size(input_shape, [1, 1],
                                             kernel_shape, pads, strides)

        output_shape = (1, 3, output_size[0], output_size[1])

        _test_single_node(
            "MaxPool",
            [input_shape],
            [output_shape],
            kernel_shape=kernel_shape,
            pads=pads,
            strides=strides
        )

        output_size = _conv_pool_output_size(input_shape, [1, 1],
                                             kernel_shape, [0, 0, 0, 0],
                                             strides)
        output_shape = (1, 3, output_size[0], output_size[1])
        _test_single_node(
            "MaxPool",
            [input_shape],
            [output_shape],
            kernel_shape=kernel_shape,
            strides=strides
        )

    def test_avg_pool(self):  # type: () -> None
        kernel_shape = (5, 3)
        pads = (2, 1, 2, 1)
        strides = (1, 2)

        input_shape = (1, 3, 224, 224)
        output_size = _conv_pool_output_size(input_shape, (1, 1),
                                             kernel_shape, pads, strides)
        output_shape = (1, 3, output_size[0], output_size[1])
        _test_single_node(
            "AveragePool",
            [input_shape],
            [output_shape],
            kernel_shape=kernel_shape,
            pads=pads,
            strides=strides
        )

        output_size = _conv_pool_output_size(input_shape, (1, 1),
                                             kernel_shape, [0, 0, 0, 0],
                                             strides)
        output_shape = (1, 3, output_size[0], output_size[1])
        _test_single_node(
            "AveragePool",
            [input_shape],
            [output_shape],
            kernel_shape=kernel_shape,
            strides=strides
        )

    def test_bn(self):  # type: () -> None
        scale = from_array(_random_array((3,)), name="scale")
        bias = from_array(_random_array((3,)), name="bias")
        mean = from_array(_random_array((3,)), name="mean")
        var = from_array(_random_array((3,)), name="var")

        epsilon = 1e-5
        momentum = 0.001

        op_types = ["BatchNormalization", "SpatialBN"]
        for op_type in op_types:
            _test_single_node(
                "BatchNormalization",
                [(1, 3, 224, 224)],
                [(1, 3, 224, 224)],
                initializer=[scale, bias, mean, var],
                is_test=1,
                epsilon=epsilon,
                momentum=momentum,
                consumed_inputs=[0, 0, 0, 1, 1]
            )

            # epsilon by default
            _test_single_node(
                "BatchNormalization",
                [(1, 3, 224, 224)],
                [(1, 3, 224, 224)],
                initializer=[scale, bias, mean, var],
                is_test=1,
                # epsilon=epsilon,
                momentum=momentum,
                consumed_inputs=[0, 0, 0, 1, 1]
            )

    def test_gemm(self):  # type: () -> None
        input_shape = (1, 2048, 1)
        output_shape = (1, 5)
        W = from_array(
            _random_array((output_shape[1], input_shape[1])), name="weight"
        )
        b = from_array(
            _random_array((output_shape[1],)), name="bias"
        )
        _test_single_node(
            "Gemm",
            [input_shape],
            [output_shape],
            initializer=[W, b],
            decimal=3,
            broadcast=1,
            transB=1
        )

    def test_lrn(self):  # type: () -> None
        _test_single_node(
            "LRN",
            [(1, 3, 224, 224)],
            [(1, 3, 224, 224)],
            alpha=9.99e-5,
            beta=0.75,
            bias=1.0,
            size=5
        )


if __name__ == '__main__':
    unittest.main()
