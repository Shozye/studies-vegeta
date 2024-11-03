import sys
import grpc
import chat_pb2
import chat_pb2_grpc
import threading

class ChatClient:
    def __init__(self, username: str, port: str):
        self.username = username
        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.stub = chat_pb2_grpc.ChatServerStub(self.channel)
        self.listener_thread = threading.Thread(target=self.listen_for_messages)
        self.listener_thread.start()

    def listen_for_messages(self):
        for note in self.stub.ChatStream(chat_pb2.Empty()):
            print(f"{note.name}: {note.message}")

    def send_message(self, message):
        note = chat_pb2.Note(name=self.username, message=message)
        self.stub.SendNote(note)

    def send_debug(self):
        self.stub.printDebugInformation(chat_pb2.Empty())

    def close(self):
        self.channel.close()

def main():
    port = "50052"
    username = input("Enter your username: ")
    client = ChatClient(username, port)

    try:
        while True:
            message = input()
            if message.lower() == "exit":
                break
            if message.lower() == "debug":
                client.send_debug()
                continue
            client.send_message(message)
    except KeyboardInterrupt:
        pass
    finally:
        client.close()

if __name__ == "__main__":
    main()
