#  -*- coding: utf-8 -*-
# Author: Burkhard Neppert
#
"""Helper class to create formatted and indented output, e.g. for code fragments.
"""
from __future__ import annotations

from typing import Any, List

def upperFst(id:str)->str:
    return id[0].upper()+id[1:] if id else id;

def lowerFst(id:str)->str:
    return id[0].lower()+id[1:] if id else id;

def camelSegments(id:str)->List[str]:
    split=[idx for (idx, c) in enumerate(id) if c.isupper()]
    if split==[]:
        return [id]
    if split[0]!=0:
        split=[0]+split
    return [id[split[i]:split[i+1]]for (i, _) in enumerate(split[:-1])]+[id[split[-1]:]]

def kebab(id:str, sep:str='-')->str:
    return sep.join(camelSegments(id))

def camel(id:str, sep:str="-")->str:
    return "".join([upperFst(s) for s in id.split(sep)])

class Writer:

    # To write to a string use an io.StringIO for iothing

    def __init__(self, iothing=None, tab="  "):
        self.iothing=iothing
        self.__tab__=tab
        self.__indent__=""

    def writeln(self, *out)->Writer:
        """Print indentation, the content and start new line"""
        print(self.__indent__, *out, file=self.iothing, sep="")
        return self

    def endln(self, *out)->Writer:
        """Print content and start new line. Don't print indentation"""
        print(*out, file=self.iothing, sep="")
        return self

    def write(self, *out)->Writer:
        print(*out, file=self.iothing, sep="", end="")
        return self

    def indent(self, *out)->Writer:
        print(self.__indent__, *out, file=self.iothing, sep="", end="")
        return self

    def inc_indent(self)->Writer:
        self.__indent__+=self.__tab__
        return self

    def dec_indent(self)->Writer:
        self.__indent__=self.__indent__[:-(min(len(self.__indent__), len(self.__tab__)))]
        return self


    def quoted_str(self, arg:Any, qchar:str='"', escape:str="\\")->str:
        return qchar+str(arg).replace(qchar, escape+qchar)+qchar

    def quote(self, arg:Any, qchar:str='"', escape:str="\\")->Writer:
        self.write(qchar, str(arg).replace(qchar, escape+qchar), qchar)
        return self


    def close(self):
        if self.iothing is not None:
            try:
                self.iothing.close()
            except:
                print(f"Failed to close Writer::iothing {self.iothing}")
