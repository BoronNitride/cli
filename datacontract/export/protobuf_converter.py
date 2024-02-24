#  -*- coding: utf-8 -*-
# Author: Burkhard Neppert
#
"""
Mapping from DataContract models to protobuf 3 message schema.

"""
from typing import Dict, List, ForwardRef, Union, Optional
from pydantic import BaseModel
from io import StringIO
import re

from datacontract.export.writer import Writer

from datacontract.model.data_contract_specification import \
    DataContractSpecification, Model, Field, Type


_TYPE_MAP_:Dict[Type, Optional[str]]={
    Type.NUMBER: None,
    Type.DECIMAL: None,
    Type.NUMERIC: None,
    Type.INT: 'int32',
    Type.INTEGER: 'int32',
    Type.LONG: 'int64',
    Type.BIGINT: None,
    Type.FLOAT: 'float',
    Type.DOUBLE: 'double',
    Type.STRING: 'string',
    Type.TEXT: 'string',
    Type.VARCHAR: 'string',
    Type.BOOLEAN: 'bool',
    Type.TIMESTAMP: None,
    Type.TIMESTAMP_TZ: None,
    Type.TIMESTAMP_NTZ: None,
    Type.DATE: None,
    Type.ARRAY: None,
    Type.OBJECT: None,
    Type.RECORD: None,
    Type.STRUCT: None,
    Type.BYTES: 'bytes',
    Type.NULL: None
}

def _prefix_name(name:str)->str:
    return "F"+name if re.match(r"^[^a-zA-Z]", name) else name

def _sub_message_name(name:str)->str:
    return "m_"+name

def mangle_field_name(name:str)->str:
    return _prefix_name(re.sub(r"[^a-zA-Z0-9_-]", "", name))

def map_field(name: str, f: Field, idx: int, w: Writer):
    pb_type=_TYPE_MAP_[f.type]
    if not pb_type:
        pb_type="bytes"
        w.writeln(f"// Warning: generic mapping from {f.type} => bytes")
    w.writeln(f'{"" if f.required else "optional "}{pb_type}  {mangle_field_name(name)} = {idx};')





def is_message_type(f: Union[Field, Type])->bool:
    return (f.type if isinstance(f, Field) else f) in [Type.OBJECT, Type.RECORD, Type.STRUCT]

def model_to_message(name: str, m: Model)->str:
    sub_messages=[(name, field) for (name, field) in m.fields.items() if is_message_type(field)]
    with StringIO() as o:
        w=Writer(o)
        w.write("syntax = ").quote("proto3").writeln(";")
        w.writeln(f"message {name} {{")
        w.inc_indent()
        for name, field in sub_messages:
            w.writeln(f"message {_sub_message_name(name)} {{")
            write_fields(field.fields, w)
            w.writeln("}")
        w.dec_indent()
        write_fields(m.fields, w)
        w.writeln("}")
        return o.getvalue()

def write_fields(fields: Dict[str, Field], w: Writer):
    w.inc_indent()
    for idx, (name, field) in enumerate(fields.items(), 1):
        map_field(name, field, idx, w)
    w.dec_indent()

def to_protubufschemas(data_contract_spec: DataContractSpecification)->Dict[str, str]:
    """Create a google protobuf 3 message for each model in the data_contract_spec.

    Cave at 1: many data types from the DataContract schema like TIMESTAMP_NTZ have no unambigous mapping
    to protobuf's type system. This function maps those types to the generice protobuf bytes type.

    Args:
      data_contract_spec: the data contract specification object.

    Returns:
      A dictionary with the model name as key and the string of the protobuf 3 schema as value.

    """
    return { name: model_to_message(name, model)
             for (name, model) in data_contract_spec.models.items()}
