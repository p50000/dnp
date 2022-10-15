import grpc
import chord_pb2 as pb2
import chord_pb2_grpc as pb2_grpc

class Client:
    def __init__(self):
        self.channel = None
        self.stub = None

        self.connected_to_registry = False
        self.is_connected = False

    def get_chord_info(self):
        response = self.stub.get_chord_info(pb2.TEmpty())
        for i in response.nodes:
            print(f'{i.ip}: \t {i.port_and_addr}')

    def get_finger_table(self):
        response = self.stub.get_finger_table(pb2.TEmpty())
        print(f'Node id: {response.id}')
        print("Finger table:")
        for i in response.nodes:
            print(f'{i.ip}: \t {i.port_and_addr}')

    def make_connection(ip_and_port: str):
        try:
            channel = grpc.insecure_channel(ip_and_port)
            stub = pb2_grpc.ConnectStub(channel)
        except:
            print("Something wrong")
            return "Error"

        service_info = stub.service_info(pb2.TEmpty())

        print("got service info: " + f'{service_info}')

        return service_info.message

    def main_function(self):    
        try: 
            while True:
                user_input = input()
                command = user_input.split(' ')
                
                # Connection
                if (command[0] == "connect"):
                    ip_and_port = command[1]
                    service_info = self.make_connection(ip_and_port)
                    if (service_info == "Connected to Registry"):
                        stub = pb2_grpc.RegistryStub(self.channel)
                        connected_to_registry = True
                        is_connected = True
                    elif (service_info == "Connected to Node"):
                        stub = pb2_grpc.NodeStub(self.channel)
                        connected_to_registry = False
                        is_connected = True
                    else:
                        connected_to_registry = False
                        is_connected = False
                    print(service_info)

                # Get info
                elif(command[0] == "get_info"):
                    if(is_connected and connected_to_registry):
                        self.get_chord_info()
                    elif(is_connected and not connected_to_registry):
                        self.get_finger_table()
                    else:
                        print("Not connected to any Node or Registry")    

                # Save
                elif(command[0] == "save"):
                    key = command[1].replace('"', '')

                    command.pop(0) #delete command name
                    command.pop(0) #delete key

                    text = ' '.join(str(e) for e in command)
                    value_to_save = pb2.TSaveRequest(key = key, text = text)
                    response = stub.save(value_to_save)
                    print(response)
                    
                # Remove
                elif(command[0] == "remove"):
                    value_to_remove = pb2.TKeyRequest(key = command[1])
                    response = stub.remove(value_to_remove)
                    print(response)
                    
                # Find
                elif(command[0] == "find"):
                    value_to_find = pb2.TKeyRequest(key = command[1])
                    response = stub.find(value_to_find)
                    print(response)
        except KeyboardInterrupt:
            print("Terminating")


    

if __name__ == "__main__":
    client = Client()
    client.main_function()