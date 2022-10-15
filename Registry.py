from email import message
import sys
import grpc
from music21 import key
import chord_pb2_grpc as pb2_grpc
import chord_pb2 as pb2
from sortedcontainers import SortedDict
from concurrent import futures
import random 

class ServiceHandler(pb2_grpc.RegistryServicer):
    def __init__(self, m):
        self.nodes = SortedDict()
        self.addresses = set()
        self.m = m
        self.max_pow = 2 ** m
        random.seed(0)

    def generate_id(self):
        id = random.randint(0,2**self.m-1) 
        while id in self.nodes:
            id = random.randint(0,2**self.m-1) 
        return id
    
    def get_predecessor(self, succ_id):
        return self.nodes.peekitem(self.nodes.bisect_key_left(succ_id) - 1)

    def get_successor(self, id):
        return self.nodes.peekitem(self.nodes.bisect_key_left(id) % self.max_pow)

    def print_node(name, id, addr):
        print(name + "for is node with id " + str(id) + "and addr " + addr)

    def register(self, request, context):
        ipaddr = request.ipaddr, port = request.port
        ipaddr_port = ipaddr + ":" + str(port)

        if ipaddr_port in self.addresses:
            return pb2.TRegisterResponse(id = -1, message = "ERROR: This address is already registeref")
        id = self.generate_id()

        self.addresses.add(ipaddr_port)
        self.nodes[id] = ipaddr_port
        
        return pb2.TRegisterResponse(id = id, message = str(self.m))

    def deregister(self, request, context):
        id = request.id
        if not id in self.nodes:
            return pb2.TSuccessResponse(is_successful = False, message = "ERROR: no such id found")
        self.nodes.pop(id)
        
        return pb2.TSuccessResponse(is_successful = True, message = "Node  uccessfully deregistered")

    def populate_finger_table(self, request, context):
        id = request.id
        print("Populating finger table for node " + str(id))
        ids_in_table = set()
        finger_table = []

        pred_id, pred_addr = self.get_predecessor(id)
        finger_table.append(pb2.TIdAndAddr(id = pred_id, port_and_addr = pred_addr))
        self.print_node("Predecessor", pred_id, pred_addr)

        pow = 1
        for i in range(0, self.m):
            succ_id, succ_addr = self.get_successor((id + pow) % self.max_pow)
            if not succ_id in ids_in_table:
                ids_in_table.add(succ_id)
                finger_table.append(pb2.TIdAndAddr(id = succ_id, port_and_addr = succ_addr))
        return pb2.TPopulateFingerTableResponse(nodes = finger_table)
    
    def get_chord_info(self, request, context):
        chord = []

        for key in self.nodes.keys():
            chord.append(pb2.TIdAndAddr(id = key, port_and_addr = self.nodes[key]))
        return pb2.TGetChordInfoResponse(nodes = chord)



class ConnectHandler(pb2_grpc.RegistryServicer):
    def service_info(self, request, context):
        return pb2.TSuccessResponse(is_successful = True, message = "Connected to Registry")



if __name__ == '__main__':
    port = sys.argv[1]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RegistryServicer_to_server(ServiceHandler(m = 5), server)
    pb2_grpc.add_ConnectServicer_to_server(ConnectHandler(), server)
    
    server.add_insecure_port(f'127.0.0.1:{port}')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Shutting down')