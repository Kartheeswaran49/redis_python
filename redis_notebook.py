# %%
import sys
import os
# %%
from pyredis import protocol
# %%
protocol.extract_frame_from_buffer(
    b"*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n"
)
# %%
os.path.abspath("..")
# %%
sys.path.append('d:\\GIT\\Mine\\redis_python')
# %%
os.getcwd()
# %%
sys.prefix
# %%
sys.base_prefix
# %%
buffer = b"+OK\r\n"
buffer[0]
# %%
buffer = b"$5\r\nhello\r\n"
separator = buffer.find(protocol._MSG_SEPARATOR)
separator
# %%
payload = buffer[1:separator].decode()
payload
# %%
buffer[1:separator]
# %%
len(buffer)
# %%
end_of_message = separator + 2 + int(payload)
end_of_message
# %%
buffer[separator + 2 : end_of_message]
# %%
buffer
# %%
chr(buffer[0])
# %%
separator = buffer.find(protocol._MSG_SEPARATOR)
separator
# %%
type(buffer[1:separator].decode())
# %%
buffer = b"*1\r\n$4\r\nping\r\n"
separator = buffer.find(protocol._MSG_SEPARATOR)
separator
# %%
positions = []
start = 0
while True:
    idx = buffer.find(protocol._MSG_SEPARATOR, start)
    print(f"idx: {idx}")
    if idx == -1:
        break
    positions.append(idx)
    start = idx + len(protocol._MSG_SEPARATOR)
    print(f"start: {start}")
positions
# %%
len(protocol._MSG_SEPARATOR)
# %%
-1 not in positions
# %%
buffer = b"*1\r\n$4\r\nping\r\n"
protocol.extract_frame_from_buffer(buffer)
# %%
protocol.extract_frame_from_buffer(b'$4\r\n')
# %%
protocol.find_all(b"$4\r\nping\r\n")
# %%
protocol.handle_bulk_string(b"$4\r\nping\r\n")
# %%
from collections.abc import Sequence
from dataclasses import dataclass

@dataclass
class BadArray(Sequence):  
    data: list

    # Notice: no __getitem__, no __len__ !

# Now if we try to create a BadArray:
bad = BadArray([1, 2, 3])

# %%
from dataclasses import dataclass

@dataclass
class SimpleArray:
    data: list

    def __getitem__(self, i):
        return self.data[i]

    def __len__(self):
        return len(self.data)

# Usage
arr = SimpleArray([10, 20, 30])

print(arr[0])    # 10
print(len(arr))  # 3
for item in arr:
    print(item)

# %%
testt = [10, 20, 30]
testt.count()
# %%
__MSG_SEPARATOR = b"\r\n"
len(__MSG_SEPARATOR)
# %%
import socket
# %%
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 6379))

    server_socket.listen(1)
    print("Server is listening on port 6379...")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")
conn, addr
# %%
