from typing import Dict
from datacontract.export.protobuf_converter import to_protubufschemas

from .fixtures import DATA_SPEC
from .resources.protobuf_out import REFS

def test_protobuf_exports():
    schemas:Dict[str, str]=to_protubufschemas(DATA_SPEC)
    for name, schema in schemas.items():
        assert schema==REFS[name]
