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
            print(f'{i.id}: \t {i.port_and_addr}')

    def get_finger_table(self):
        response = self.stub.get_finger_table(pb2.TEmpty())
        print(f'Node id: {response.id}')
        print("Finger table:")
        for i in response.nodes:
            print(f'{i.id}: \t {i.port_and_addr}')

    def make_connection(self, ip_and_port: str):
        try:
            self.channel = grpc.insecure_channel(ip_and_port)
            stub = pb2_grpc.ConnectStub(self.channel)
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
                        self.stub = pb2_grpc.RegistryStub(self.channel)
                        self.connected_to_registry = True
                        self.is_connected = True
                    elif (service_info == "Connected to Node"):
                        self.stub = pb2_grpc.NodeStub(self.channel)
                        self.connected_to_registry = False
                        self.is_connected = True
                    else:
                        self.connected_to_registry = False
                        self.is_connected = False
                    print(service_info)

                # Get info
                elif(command[0] == "get_info"):
                    if(self.is_connected and self.connected_to_registry):
                        self.get_chord_info()
                    elif(self.is_connected and not self.connected_to_registry):
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
                    response = self.stub.save(value_to_save)
                    print(response)
                    
                # Remove
                elif(command[0] == "remove"):
                    value_to_remove = pb2.TKeyRequest(key = command[1])
                    response = self.stub.remove(value_to_remove)
                    print(response)
                    
                # Find
                elif(command[0] == "find"):
                    value_to_find = pb2.TKeyRequest(key = command[1])
                    response = self.stub.find(value_to_find)
                    print(response)
                    success = response.is_successful
                    message = response.message
                    id = message.split(' ')
                    if(success):
                        print(f'True, {command[1]} is saved in node {id[0]}')
                    else:
                        print(f'False, {command[1]} is not exist in node {id[0]}')

        except KeyboardInterrupt:
            print("Terminating")


    

if __name__ == "__main__":
    client = Client()
    client.main_function()