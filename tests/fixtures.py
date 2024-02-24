from typing import Dict
from datacontract.model.data_contract_specification import Model, Field, Type, DataContractSpecification

def is_compound(t: Type)->bool:
    return t in [Type.OBJECT, Type.RECORD, Type.STRUCT]


BASIC_FIELDS:Dict[str, Field]={t.name: Field(type=t) for t in Type if not is_compound(t)}

FLAT_STRUCT:Field=Field(type=Type.STRUCT, fields=BASIC_FIELDS)

NESTED_STRUCT:Field=Field(type=Type.STRUCT, fields={'a': FLAT_STRUCT, 'b': FLAT_STRUCT})


DATA_SPEC=DataContractSpecification(models={'basic': Model(fields=BASIC_FIELDS),
                                            'struct': Model(fields={'flat': FLAT_STRUCT,
                                                                    'nested': NESTED_STRUCT})})


# The modelling of Type and Field makes recursive structs cumbersome.
# RECURSIVE_STRUCT:Field=Field(type=Type.STRUCT, fields={'left': <no what here ?>})
