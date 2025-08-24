import socket
import typer
from typing_extensions import Annotated

from pyredis.protocol import encode_message, extract_frame_from_buffer
from pyredis.message_types import Array, BulkString

DEFAULT_PORT = 6379
DEFAULT_SERVER = "127.0.0.1"
RECV_SIZE = 1024


def encode_command(command):
    return Array([BulkString(p) for p in command.split()])


def main(
    server: Annotated[str, typer.Argument()] = DEFAULT_SERVER,
    port: Annotated[int, typer.Argument()] = DEFAULT_PORT,
):
    with socket.socket() as client_socket:
        client_socket.connect((server, port))

        buffer = bytearray()

        while True:
            command = input(f"{server}:{port}>")

            if command == "quit":
                print('Quitting...')
                break
            else:
                print(f'encode_command(command): {encode_command(command)}')
                encoded_message = encode_message(encode_command(command))
                print(f'encoded_message: {encoded_message}')
                client_socket.send(encoded_message)

                while True:
                    data = client_socket.recv(RECV_SIZE)
                    print(f'data: {data}')
                    buffer.extend(data)
                    print(f'buffer: {buffer}')

                    frame, frame_size = extract_frame_from_buffer(buffer)
                    print(f'frame, frame_size: {frame, frame_size}')

                    if frame:
                        buffer = buffer[frame_size:]
                        if isinstance(frame, Array):
                            for count, item in enumerate(frame.data):
                                print(f'{count + 1}) "{item.as_str()}"')
                        else:
                            print(f'type: {type(frame)}')
                            print(frame.as_str())
                        break


if __name__ == "__main__":
    typer.run(main)