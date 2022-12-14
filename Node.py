import sys
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
        if register_info.id== -1:
            raise Exception("I don't know Python!")

        self.ip_and_port = f'{node_ip}:{node_port}'
        self.m = register_info.message
        self.id = register_info.id
        self.m_pow = 2 ** int(self.m) 
        self.table = dict()
        print("Connected to Registry")

        finger_table = self.registry_stub.populate_finger_table(pb2.TPopulateFingerTableRequest(id = self.id)).nodes
        # getting values from successor
        if (len(finger_table) >= 2):
            id = finger_table[1].id
            if self.id == id:
                return
            ip_and_port = finger_table[1].port_and_addr
            new_channel = grpc.insecure_channel(ip_and_port)
            new_node_stub = pb2_grpc.NodeStub(new_channel) 
            values = new_node_stub.get_values(pb2.TGetValuesRequest(id = self.id)).values
            for value in values:
                k = value.key
                v = value.text
                #print(f'Gol {k}, {v} for node {self.id}')
                hash_value = zlib.adler32(k.encode())
                target_id = hash_value % self.m_pow
                if not self.in_right(self.id, id, target_id):
                    #print(f'Saving {k}, {v} in node {self.id}')
                    self.table[k] = v

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
            if self.in_left(finger_table[i].id, finger_table[i + 1].id, k):
                return finger_table[i].id
        return -1

    def get_values(self, request, context):
        pred_id = request.id
        ans = []
        for k, v in self.table.items():
            ans.append(pb2.TKeyValue(key = k, text = v))
        for value in ans:
            k = value.key
            v = value.text
            hash_value = zlib.adler32(k.encode())
            target_id = hash_value % self.m_pow
            if not self.in_right(pred_id, self.id, target_id):
                del self.table[k]
        return pb2.TGetValuesResponse(values = ans)


    def get_finger_table(self, request, context):
        finger_table = self.registry_stub.populate_finger_table(pb2.TPopulateFingerTableRequest(id = self.id)).nodes
        return pb2.TGetFingerTableResponse(id = self.id, nodes = finger_table[1:])

    def save(self, request, context):
        text = request.text
        key = request.key
        hash_value = zlib.adler32(key.encode())
        target_id = hash_value % self.m_pow
        finger_table = self.registry_stub.populate_finger_table(pb2.TPopulateFingerTableRequest(id = self.id))

        lookup_result = self.lookup(finger_table.nodes, target_id)

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
                msg = pb2.TSaveRequest(key = key, text = text)
                return new_node_stub.save(msg)

    def remove(self, request, context):
        key = request.key
        hash_value = zlib.adler32(key.encode())
        target_id = hash_value % self.m_pow
        finger_table = self.registry_stub.populate_finger_table(pb2.TPopulateFingerTableRequest(id = self.id))

        lookup_result = self.lookup(finger_table.nodes, target_id)

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
                msg = pb2.TKeyRequest(key = key)
                return new_node_stub.remove(msg)

    def find(self, request, context):
        key = request.key
        hash_value = zlib.adler32(key.encode())
        target_id = hash_value % self.m_pow
        finger_table = self.registry_stub.populate_finger_table(pb2.TPopulateFingerTableRequest(id = self.id))

        lookup_result = self.lookup(finger_table.nodes, target_id)

        if(lookup_result==-1):
            print("Lookup failure")

        if(self.id==lookup_result):
            if(key in self.table):
                msg = pb2.TSuccessResponse(is_successful=True, message=f'{target_id} {self.ip_and_port}')
                return msg
            else:
                msg = pb2.TSuccessResponse(is_successful=False, message=f'{target_id} {self.ip_and_port}')
                return msg
        else:
            ip_and_port = find_node_in_finger_table(lookup_result, finger_table)

            if(ip_and_port==None):
                msg = pb2.TSuccessResponse(is_successful=False, message = f'{target_id} Could not find ip and port for node {lookup_result}')
                return msg
            else:
                new_channel = grpc.insecure_channel(ip_and_port)
                new_node_stub = pb2_grpc.NodeStub(new_channel) 
                msg = pb2.TKeyRequest(key = key)
                return new_node_stub.find(msg)

    def try_saving_to_succ(self, k, v):
        finger_table = self.registry_stub.populate_finger_table(pb2.TPopulateFingerTableRequest(id = self.id)).nodes
        if len(finger_table) < 2:
            return pb2.TSuccessResponse(is_successful=True, message = f'No second node')
        ip_and_port = finger_table[1].port_and_addr
        new_channel = grpc.insecure_channel(ip_and_port)
        new_node_stub = pb2_grpc.NodeStub(new_channel) 

        return new_node_stub.save(pb2.TSaveRequest(key = k, text = v))
        
    def quit(self):
        self.registry_stub.deregister(pb2.TDeregisterRequest(id=self.id))
        cnt = 0
        for k, v in self.table.items():
            while not self.try_saving_to_succ(k, v).is_successful:
                cnt += 1

class ConnectHandler(pb2_grpc.RegistryServicer):
    def service_info(self, request, context):
        return pb2.TSuccessResponse(is_successful = True, message = "Connected to Node")




if __name__ == "__main__":
    registry_ip, registry_port = registry_info[0], registry_info[1]
    node_ip, node_port = node_info[0], node_info[1]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port(f'{node_ip}:{node_port}')
    
    channel = grpc.insecure_channel(f'{registry_ip}:{registry_port}')
    nodeHandler = ServiceHandler(channel, node_ip, node_port)
    pb2_grpc.add_NodeServicer_to_server(nodeHandler, server)
    pb2_grpc.add_ConnectServicer_to_server(ConnectHandler(), server)
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        nodeHandler.quit()
        print('Quitting')
