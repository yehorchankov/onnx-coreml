from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Dict, Text, Any, Callable
from coremltools.models.neural_network import NeuralNetworkBuilder  #type: ignore
from ._graph import Node, Graph

class ErrorHandling(object):
  '''
  To handle errors and addition of custom layers
  '''

  def __init__(self,
               add_custom_layers = False, # type: bool
               custom_conversion_functions = dict(), # type: Dict[Text, Any]
               custom_layer_nodes = [], # type : List[Node]
               disable_coreml_rank5_mapping = False
               ):
      # type: (...) -> None
      self.add_custom_layers = add_custom_layers
      self.custom_conversion_functions = custom_conversion_functions
      self.custom_layer_nodes = custom_layer_nodes
      self.disable_coreml_rank5_mapping = disable_coreml_rank5_mapping
      # TODO: Remove following error message once, disable_coreml_rank5_mapping is default to True
      self.coreml_3_rerun_message = ''
      if not disable_coreml_rank5_mapping:
        self.coreml_3_rerun_message = '\nPlease try converting again with disable_coreml_rank5_mapping=True' \
                                                        ' and coremltools 3.0 latest beta'


  def unsupported_op(self,
                     node,  # type: Node
                    ):
      # type: (...) -> Callable[[Any, Node, Graph, ErrorHandling], None]
      '''
      Either raise an error for an unsupported op type or return custom layer add function
      '''
      if self.add_custom_layers:
        from ._operators import _convert_custom
        return _convert_custom
      else:
        raise TypeError(
          "ONNX node of type {} is not supported. {}\n".format(node.op_type, self.coreml_3_rerun_message)
        )


  def unsupported_op_configuration(self,
                                   builder, # type: NeuralNetworkBuilder
                                   node, # type: Node
                                   graph, # type: Graph
                                   err_message, # type: Text
                                   ):
      # type: (...) -> None
      '''
      Either raise an error for an unsupported attribute or add a custom layer.
      '''
      if self.add_custom_layers:
        from ._operators import _convert_custom
        _convert_custom(builder, node, graph, self)
      else:
        raise TypeError(
          "Error while converting op of type: {}. Error message: {} {}\n".format(node.op_type, err_message,
                                                                                  self.coreml_3_rerun_message)
        )


  def missing_initializer(self,
                          node, # type: Node
                          err_message, # type: Text
                          ):
      # type: (...) -> None
      '''
      Missing initializer error
      '''
      raise ValueError(
        "Missing initializer error in op of type {}, with input name = {}, "
        "output name = {}. Error message: {} {}\n".
        format(node.op_type, node.inputs[0], node.outputs[0], err_message, self.coreml_3_rerun_message)
      )

  def unsupported_feature_warning(self,
                                  node, # type: Node
                                  err_message, # type: Text
                                  ):
      # type: (...) -> None
      '''
      Unsupported feature warning
      '''
      print(
        "Warning: Unsupported Feature in op of type {}, with input name = {}, "
        "output name = {}. Warning message: {} {}\n".
        format(node.op_type, node.inputs[0], node.outputs[0], err_message, self.coreml_3_rerun_message)
      )



