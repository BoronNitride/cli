#  -*- coding: utf-8 -*-
# Author: Burkhard Neppert
#
"""
Mapping from DataContract models to Apache Avro schema.

* DataContracts are mapped to Avro protocols
* DataContract Models are mapped to Avro messages

"""
from typing import Dict, List, ForwardRef, Union, Optional
from io import StringIO
import re

from datacontract.export.writer import Writer

from datacontract.model.data_contract_specification import \
    DataContractSpecification, Model, Field, Type


_TYPE_MAP_:Dict[Type, Optional[str]]={
    Type.NUMBER: None,
    Type.DECIMAL: None,
    Type.NUMERIC: None,
    Type.INT: 'int',
    Type.INTEGER: 'int',
    Type.LONG: 'long',
    Type.BIGINT: 'long',
    Type.FLOAT: 'float',
    Type.DOUBLE: 'double',
    Type.STRING: 'string',
    Type.TEXT: 'string',
    Type.VARCHAR: 'string',
    Type.BOOLEAN: 'boolean',
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

def map_field(name: str, f: Field, w: Writer):
    pb_type=_TYPE_MAP_[f.type]
    warning=""
    if not pb_type:
        pb_type="bytes"
        # warning=f', "__warning__": "Generic mapping from {f.type} => bytes"'
    if not f.required:
        pb_type=f'["null", "{pb_type}"]'
    else:
        pb_type=f'"{pb_type}"'
    w.indent().write(f'{{"name": "{name}", "type": {pb_type}{warning}}}')



def is_message_type(f: Union[Field, Type])->bool:
    return (f.type if isinstance(f, Field) else f) in [Type.OBJECT, Type.RECORD, Type.STRUCT]

def kv_writeln(k: str, v: str, w: Writer)->Writer:
    w.writeln(f'"{k}": "{v}",')
    return w

def model_to_schema(name: str, m: Model)->str:
    with StringIO() as o:
        w=Writer(o)
        w.writeln("{")
        w.inc_indent()
        kv_writeln("name", mangle_field_name(name), w)
        kv_writeln("type", "record", w)
        w.writeln('"fields": [').inc_indent()
        write_fields(m.fields, w)
        w.dec_indent().writeln("]").dec_indent()
        w.writeln("}")
        return o.getvalue()

def write_fields(fields: Dict[str, Field], w: Writer):
    w.inc_indent()
    first=True # Shenanigans to terminate all but last line with ','
    for (name, field) in fields.items():
        if not first:
            w.endln(",")
        map_field(name, field, w)
        first=False
    w.endln()
    w.dec_indent()

def to_avroschemas(data_contract_spec: DataContractSpecification)->Dict[str, str]:
    """Create an Avro schema for each model in the data_contract_spec.

    Args:
      data_contract_spec: the data contract specification object.

    Returns:
      A dictionary with the model name as key and the string of the Avro schema as value.
    """

    return { name: model_to_schema(name, model)
             for (name, model) in data_contract_spec.models.items()}
