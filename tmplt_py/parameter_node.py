import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

# message type used in this example.
# Custom message types can also be used
# to know all available interfaces:
# > ros2 interface list
# To know what contains a messages of type 'String'
# > ros2 interface show example_interfaces/msg/String
from example_interfaces.msg import String 

PARAM_NAME="name"

class ParameterNode(Node):
    def __init__(self):
        super().__init__("parameter")
        self.get_logger().info("parameter has started...")
        # ROS timer functionality : “Execute this function every X seconds”
        self.create_timer(1, self.print_name_callback)

        # declare a ROS parameter : -> use data type of the default value to associate a type to the parameter
        self.declare_parameter(PARAM_NAME, "R2D2")

        # get parameter value
        self._name = self.get_parameter(PARAM_NAME).value

        # make the parameter modifyable at runtime (by other nodes, ...)
        self.add_on_set_parameters_callback(self.parameters_callback)


        # publish on the "/print_name" topic
        self._publisher = self.create_publisher(String, "print_name", 10)
    
    def print_name_callback(self) -> None:
        """ usually we name the publisher callback using the topic name from which it 
            processes data
        """
        msg = String()
        msg.data = f"Hello this is {self._name}"
        self._publisher.publish(msg)

    def parameters_callback(self, params:list[Parameter]) -> None:
        # NOTE : the callback is not called for an unknown reason... Current ROS2 bug? 
        for param in params:
            if param.name == PARAM_NAME:
                self._name = param.value
                

    
def main(args=None):
    rclpy.init(args=args)
    node = ParameterNode()
    rclpy.spin(node) # optional : required if we want the node to stay alive
    rclpy.shutdown()


if __name__ == "__main__":
    main()

    # Note : to test this code works:
    # > ros2 topic echo /print_name
    # > ros2 parameter set /name "C3PO"
    # > ros2 parameter get /name