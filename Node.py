import sys
from turtle import right
import grpc
import chord_pb2 as pb2
import chord_pb2_grpc as pb2_grpc

args = sys.argv
registry_info = args[1].split(':')
node_info = args[2].split(':')

class ServiceHandler(pb2_grpc.NodeServicer):

    def __init__(self, channel, node_ip, node_port):
        self.registry_stub = pb2_grpc.RegistryStub(channel)
        msg = pb2.TRegisterRequest(ipaddr = node_ip, port = int(node_port))

        register_info = self.registry_stub.register(msg)
        # вот тут надо обработать респонс
        self.m = register_info.message
        self.id = register_info.id
        self.m_pow = int(self.m) ** 2
        print("Connected to Registry")

    def in_left(self, left, right, k):
        if right > left:
            return k >= left and k < right
        else:
            return (k >= left and k < self.m_pow) or (k < right)
    
    def in_right(self, left, right, k):
        if right > left:
            return k > left and k <= right
        else:
            return (k > left and k < self.m_pow) or (k <= right)

    def lookup(self, finger_table, k):
        if self.in_right(finger_table[0].id, self.id):
            return self.id
        elif self.in_right(self.id, finger_table[1].id):
            return finger_table[1].id
        for i in range(1, len(finger_table) - 1):
            if self.in_left(finger_table[i].id, finger_table[i + 1].id):
                return i
        return -1


    def get_finger_table(self):
        finger_table = self.registry_stub.populate_finger_table()
        return finger_table

    def save(self, key, text):

    def remove(self, key):

    def find(self, key):

if __name__ == "__main__":
    registry_ip, registry_port = registry_info[0], registry_info[1]
    node_ip, node_port = node_info[0], node_info[1]
    
    channel = grpc.insecure_channel(f'{registry_ip}:{registry_port}')
    registry_stub = pb2_grpc.RegistryStub(channel)
    print("Connected to Registry")

    msg = pb2.TRegisterRequest(ipaddr = node_ip, port = int(node_port))
    response = registry_stub.register(msg)
