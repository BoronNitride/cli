from typing import Dict
from datacontract.model.data_contract_specification import Model, Field, Type, DataContractSpecification

def is_compound(t: Type)->bool:
    return t in [Type.OBJECT, Type.RECORD, Type.STRUCT]


BASIC_FIELDS:Dict[str, Field]={t.name: Field(type=t) for t in Type if not is_compound(t)}

BASIC_FIELDS_REQUIRED:Dict[str, Field]={t.name+"_REQ": Field(type=t, required=True) for t in Type if not is_compound(t)}

FLAT_STRUCT:Field=Field(type=Type.STRUCT, fields=BASIC_FIELDS)

FLAT_STRUCT_REQUIRED:Field=Field(type=Type.STRUCT, fields=BASIC_FIELDS_REQUIRED)

NESTED_STRUCT:Field=Field(type=Type.STRUCT, fields={'a': FLAT_STRUCT, 'b': FLAT_STRUCT})


NESTED_STRUCT_REQUIRED:Field=Field(type=Type.STRUCT, fields={'a_req': FLAT_STRUCT_REQUIRED, 'b_req': FLAT_STRUCT_REQUIRED})


DATA_SPEC=DataContractSpecification(models={'basic': Model(fields=BASIC_FIELDS),
                                            'struct': Model(fields={'flat': FLAT_STRUCT,
                                                                    'nested': NESTED_STRUCT})})


DATA_SPEC_REQUIRED=DataContractSpecification(models={'basic_req': Model(fields=BASIC_FIELDS_REQUIRED),
                                            'struct_req': Model(fields={'flat_req': FLAT_STRUCT_REQUIRED,
                                                                    'nested_req': NESTED_STRUCT_REQUIRED})})


# The modelling of Type and Field makes recursive structs cumbersome.
# RECURSIVE_STRUCT:Field=Field(type=Type.STRUCT, fields={'left': <no what here ?>})
