from cgitb import lookup
import sys
from turtle import right
import grpc
import zlib
import chord_pb2 as pb2
import chord_pb2_grpc as pb2_grpc
from concurrent import futures

args = sys.argv
registry_info = args[1].split(':')
node_info = args[2].split(':')

def find_node_in_finger_table(lookup_result, finger_table):
    ip_and_port = None
    for node in finger_table.nodes:
        if(node.id==lookup_result):
            ip_and_port = node.port_and_addr
    return ip_and_port



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
        if self.in_right(finger_table[0].id, self.id, k):
            return self.id
        elif self.in_right(self.id, finger_table[1].id, k):
            return finger_table[1].id
        for i in range(1, len(finger_table) - 1):
            if self.in_left(finger_table[i].id, finger_table[i + 1, k].id):
                return i
        return -1


    def get_finger_table(self, request, context):
        finger_table = self.registry_stub.populate_finger_table(pb2.TEmpty())
        return finger_table[1:]

    def save(self, request, context):
        text = request.text
        key = request.key
        hash_value = zlib.adler32(key.encode())
        target_id = hash_value % 2 ** self.m
        finger_table = self.registry_stub.populate_finger_table(pb2.TEmpty())

        lookup_result = lookup(finger_table, target_id)

        if(lookup_result==-1):
            print("Lookup failure")
        if(self.id==lookup_result):
            if(bool(self.table.get(key))):
                msg = pb2.TSuccessResponse(is_successful=False, message = f'{key} is alredy exists in node {target_id}')
                return msg
            else:
                self.table[key] = text
                msg = pb2.TSuccessResponse(is_successful=True, message = f'{key} is saved in node {target_id}')
                return msg
        else:
            ip_and_port = find_node_in_finger_table(lookup_result, finger_table)

            if(ip_and_port==None):
                msg = pb2.TSuccessResponse(is_successful=False, message = f'Could not find ip and port for node {lookup_result}')
                return msg
            else:
                new_channel = grpc.insecure_channel(ip_and_port)
                new_node_stub = pb2_grpc.NodeStub(new_channel) 
                msg = pb2.TSaveRequest(key, text)
                return new_node_stub.save(msg)

    def remove(self, request, context):
        key = request.key
        hash_value = zlib.adler32(key.encode())
        target_id = hash_value % 2 ** self.m
        finger_table = self.registry_stub.populate_finger_table(pb2.TEmpty())

        lookup_result = lookup(finger_table, target_id)

        if(lookup_result==-1):
            print("Lookup failure")
        if(self.id==lookup_result):
            try:
                del self.table[key]
                msg = pb2.TSuccessResponse(is_successful=True, message=f'{key} is removed from node {target_id}')
                return msg

            except:
                msg = pb2.TSuccessResponse(is_successful=False, message=f'{key} is not exist in table on node {target_id}')
                return msg
        else:
            ip_and_port = find_node_in_finger_table(lookup_result, finger_table)

            if(ip_and_port==None):
                msg = pb2.TSuccessResponse(is_successful=False, message = f'Could not find ip and port for node {lookup_result}')
                return msg
            else: 
                new_channel = grpc.insecure_channel(ip_and_port)
                new_node_stub = pb2_grpc.NodeStub(new_channel) 
                msg = pb2.TKeyRequest(key)
                return new_node_stub.remove(msg)

    def find(self, request, context):
        key = request.key
        hash_value = zlib.adler32(key.encode())
        target_id = hash_value % 2 ** self.m
        finger_table = self.registry_stub.populate_finger_table(pb2.TEmpty())

        lookup_result = lookup(finger_table, target_id)

        if(lookup_result==-1):
            print("Lookup failure")

        if(self.id==lookup_result):
            ip_and_port = find_node_in_finger_table(lookup_result, finger_table)

            if(ip_and_port==None):
                msg = pb2.TSuccessResponse(is_successful=False, message = f'Could not find ip and port for node {lookup_result}')
                return msg
            else:
                msg = pb2.TSuccessResponse(is_successful=True, message=ip_and_port)
                return msg
        else:
            ip_and_port = find_node_in_finger_table(lookup_result, finger_table)

            if(ip_and_port==None):
                msg = pb2.TSuccessResponse(is_successful=False, message = f'Could not find ip and port for node {lookup_result}')
                return msg
            else:
                new_channel = grpc.insecure_channel(ip_and_port)
                new_node_stub = pb2_grpc.NodeStub(new_channel) 
                msg = pb2.TKeyRequest(key)
                return new_node_stub.find(msg)

    def try_saving_to_succ(self, k, v):
        finger_table = self.registry_stub.populate_finger_table(pb2.TEmpty())
        ip_and_port = find_node_in_finger_table(1, finger_table)
        new_channel = grpc.insecure_channel(ip_and_port)
        new_node_stub = pb2_grpc.NodeStub(new_channel) 
        try:
            return new_node_stub.save(pb2.TSaveRequest(key = k, value = v))
        except:
            return pb2.TSuccessResponse(is_successful=False, message = f'Failed to save key')


    def quit(self):
        cnt = 0
        for k, v in self.table.items():
            while not self.try_saving_to_succ(k, v).is_successful():
                cnt += 1
            print(f'Saved kay {k} after {cnt} attempts')

class ConnectHandler(pb2_grpc.RegistryServicer):
    def service_info(self, request, context):
        return pb2.TSuccessResponse(is_successful = True, message = "Connected to Node")




if __name__ == "__main__":
    registry_ip, registry_port = registry_info[0], registry_info[1]
    node_ip, node_port = node_info[0], node_info[1]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port(f'{node_ip}:{node_port}')
    server.start()
    
    channel = grpc.insecure_channel(f'{registry_ip}:{registry_port}')
    nodeHandler = ServiceHandler(channel, node_ip)
    pb2_grpc.add_NodeServicer_to_server(ServiceHandler(), server)
    pb2_grpc.add_ConnectServicer_to_server(ConnectHandler(), server)
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        nodeHandler.quit()
        print('Quitting')
