import os, json, sys;

class Base:
    def __findbyid__(self, lista, id):
        buffer = list(filter(lambda x:x.id == id, lista ) );
        if len(buffer) == 0:
            return None;
        return buffer[0];