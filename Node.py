from cgitb import lookup
import sys
from turtle import right
import grpc
import zlib
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
        self.table = dict()
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
        hash_value = zlib.adler32(key.encode())
        target_id = hash_value % 2 ** self.m
        finger_table = self.get_finger_table()

        lookup_result = lookup(finger_table, target_id)
        if(self.id==lookup_result):
            if(bool(self.table.get(key))):
                msg = pb2.TSuccessResponse(is_successful=False, message = f'{key} is alredy exists in node {target_id}')
                return msg
            else:
                self.table[key] = text
                msg = pb2.TSuccessResponse(is_successful=True, message = f'{key} is saved in node {target_id}')
                return msg
        else:
            ip_and_port = None

            # Извени за этот кринж я правда не умею в питон
            for node in finger_table.nodes:
                if(node.id==lookup_result):
                    ip_and_port = node.port_and_addr
                    print(f'Founded ip and port for node with ip: {lookup_result}')

            new_channel = grpc.insecure_channel(ip_and_port)
            new_node_stub = pb2_grpc.NodeStub(new_channel) 
            return new_node_stub.save(key, text)


    def remove(self, key):
        hash_value = zlib.adler32(key.encode())
        target_id = hash_value % 2 ** self.m
        finger_table = self.get_finger_table()

        lookup_result = lookup(finger_table, target_id)
        if(self.id==lookup_result):
            try:
                del self.table[key]
                msg = pb2.TSuccessResponse(is_successful=True, message=f'{key} is removed from node {target_id}')
                return msg

            except:
                msg = pb2.TSuccessResponse(is_successful=False, message=f'{key} is not exist in table on node {target_id}')
                return msg
        else:
            ip_and_port = None

            # Извени за этот кринж я правда не умею в питон
            for node in finger_table.nodes:
                if(node.id==lookup_result):
                    ip_and_port = node.port_and_addr
                    print(f'Founded ip and port for node with ip: {lookup_result}')

            new_channel = grpc.insecure_channel(ip_and_port)
            new_node_stub = pb2_grpc.NodeStub(new_channel) 
            return new_node_stub.remove(key)

    def find(self, key):
        hash_value = zlib.adler32(key.encode())
        target_id = hash_value % 2 ** self.m
        finger_table = self.get_finger_table()

        lookup_result = lookup(finger_table, target_id)
        if(self.id==lookup_result):


if __name__ == "__main__":
    registry_ip, registry_port = registry_info[0], registry_info[1]
    node_ip, node_port = node_info[0], node_info[1]
    
    channel = grpc.insecure_channel(f'{registry_ip}:{registry_port}')
    registry_stub = pb2_grpc.RegistryStub(channel)
    print("Connected to Registry")

    msg = pb2.TRegisterRequest(ipaddr = node_ip, port = int(node_port))
    response = registry_stub.register(msg)