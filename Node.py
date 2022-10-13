import sys
import grpc
import chord_pb2 as pb2
import chord_pb2_grpc as pb2_grpc

args = sys.argv
registry_info = args[1].split(':')
node_info = args[2].split(':')


registry_ip, registry_port = registry_info[0], registry_info[1]
node_ip, node_port = node_info[0], node_info[1]

channel = grpc.insecure_channel(f'{registry_ip}:{registry_port}')
stub = pb2_grpc.RegistryStub(channel)
print("Connected to Registry")

def get_finger_table():
    finger_table = stub.populate_finger_table
    return finger_table

def save(key, text)

def remove(key)

def find(key)

if __name__ == "__main__":

    

    msg = pb2.TRegisterRequest(ipaddr = node_ip, port = int(node_port))
    response = stub.register(msg)
