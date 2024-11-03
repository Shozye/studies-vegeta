from collections import deque
from concurrent import futures
import logging
import time

import grpc
import chat_pb2
import chat_pb2_grpc



class ChatServicer(chat_pb2_grpc.ChatServerServicer):
    def __init__(self):
        self.clients = []  
        self.messages = []

    def ChatStream(self, request, context):
        self.clients.append(context)
        message_index = 0
        
        try:
            while True:
                while message_index < len(self.messages):
                    yield self.messages[message_index]
                    message_index += 1
        
                time.sleep(1) 
        finally:
            self.clients.remove(context)  

    def SendNote(self, request, context):
        note = chat_pb2.Note(name=request.name, message=request.message)
        self.messages.append(note)
        return chat_pb2.Empty()  # Return an empty response
    
    def printDebugInformation(self, request, context):
        print(f"{self.messages=}, {request=}, {context=}")
        return chat_pb2.Empty()  
    
def serve():
    port = "50052"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServerServicer_to_server(ChatServicer(), server)

    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()