import os, json;
#https://dev.to/bshadmehr/reflecting-on-pythons-reflection-a-guide-to-metaprogramming-basics-1bhk
#https://stackoverflow.com/questions/34327719/get-keys-from-json-in-python
class Config:
    def __init__(self, path):
        self.path = path;
        self.__constructor__(self, json.load( open(path, 'r') ) );

    def __constructor__(self, obj, data):
        for key in data.keys():
            if type(data[key]) != dict:
                setattr(obj, key, data[key] );
            else:
                buffer = object();
                setattr(obj, key, buffer );
                self.__constructor__( buffer,  data[key] );