from typing import Dict
from datacontract.export.avro_converter import to_avroschemas
from  fastavro.schema import parse_schema
from json import loads

from .fixtures import DATA_SPEC, DATA_SPEC_REQUIRED
from .resources.protobuf_out import REFS


def test_avro_exports():

    avro_protocols:Dict[str, str]=to_avroschemas(DATA_SPEC)
    avro_protocols.update(to_avroschemas(DATA_SPEC_REQUIRED))
    # Valid json ?
    avro_protocols_struct={k: parse_schema(loads(v)) for (k, v) in avro_protocols.items()}
    # There does not scheme to be a grammar for Avro schema against which we can validate.
