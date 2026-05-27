import rclpy
from rclpy.node import Node

# message type used in this example.
# Custom message types can also be used
# to know all available interfaces:
# > ros2 interface list
# To know what contains a messages of type 'String'
# > ros2 interface show example_interfaces/msg/String
from example_interfaces.msg import String 

class ParameterNode(Node):
    def __init__(self):
        super().__init__("parameter")
        self.get_logger().info("parameter has started...")
        # ROS timer functionality : “Execute this function every X seconds”
        self.create_timer(1, self.print_name_callback)

        # declare a ROS parameter : -> use data type of the default value to associate a type to the parameter
        self.declare_parameter("name", "R2D2")


        # get parameter value
        self._name = self.get_parameter("name").value

        # publish on the "/counter" topic
        self._publisher = self.create_publisher(String, "print_name", 10)
    
    def print_name_callback(self) -> None:
        """ usually we name the publisher callback using the topic name from which it 
            processes data
        """
        msg = String()
        msg.data = f"Hello this is {self._name}"
        self._publisher.publish(msg)

    
def main(args=None):
    rclpy.init(args=args)
    node = ParameterNode()
    rclpy.spin(node) # optional : required if we want the node to stay alive
    rclpy.shutdown()


if __name__ == "__main__":
    main()

    # Note : to test this code works:
    # > ros2 topic echo /counter