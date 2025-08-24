from collections.abc import Sequence
from dataclasses import dataclass

_DELIMITER = "\r\n"

@dataclass
class SimpleString:
    data: str

    def as_str(self):
        return self.data

    def resp_encode(self):
        return f"+{self.data}{_DELIMITER}".encode()


@dataclass
class Error:
    data: str

    def as_str(self):
        return self.data

    def resp_encode(self):
        return f"-{self.data}{_DELIMITER}".encode()


@dataclass
class Integer:
    value: int

    def as_str(self):
        return self.value

    def resp_encode(self):
        return f":{self.value}{_DELIMITER}".encode()


@dataclass
class BulkString:
    data: bytes

    def as_str(self):
        return self.data.decode()

    def resp_encode(self):
        return f"${len(self.data)}{_DELIMITER}{self.data}{_DELIMITER}".encode() if self.data is not None \
            else f"$-1{_DELIMITER}".encode()


@dataclass
class Array(Sequence):
    data: list

    def __getitem__(self, i):
        return self.data[i]

    def __len__(self):
        return len(self.data)
    
    def resp_encode(self):
        if self.data is None:
            return f"*-1{_DELIMITER}".encode()
        
        else:
            length = len(self.data)
            encoded_string = f'*{length}{_DELIMITER}'.encode()
            for i in self.data:
                encoded_string += i.resp_encode()
            
            return encoded_string