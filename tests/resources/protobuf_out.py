basic="""syntax = "proto3";
message basic {
  // Warning: generic mapping from Type.NUMBER => bytes
  optional bytes  NUMBER = 1;
  // Warning: generic mapping from Type.DECIMAL => bytes
  optional bytes  DECIMAL = 2;
  // Warning: generic mapping from Type.NUMERIC => bytes
  optional bytes  NUMERIC = 3;
  optional int32  INT = 4;
  optional int32  INTEGER = 5;
  optional int64  LONG = 6;
  // Warning: generic mapping from Type.BIGINT => bytes
  optional bytes  BIGINT = 7;
  optional float  FLOAT = 8;
  optional double  DOUBLE = 9;
  optional string  STRING = 10;
  optional string  TEXT = 11;
  optional string  VARCHAR = 12;
  optional bool  BOOLEAN = 13;
  // Warning: generic mapping from Type.TIMESTAMP => bytes
  optional bytes  TIMESTAMP = 14;
  // Warning: generic mapping from Type.TIMESTAMP_TZ => bytes
  optional bytes  TIMESTAMP_TZ = 15;
  // Warning: generic mapping from Type.TIMESTAMP_NTZ => bytes
  optional bytes  TIMESTAMP_NTZ = 16;
  // Warning: generic mapping from Type.DATE => bytes
  optional bytes  DATE = 17;
  // Warning: generic mapping from Type.ARRAY => bytes
  optional bytes  ARRAY = 18;
  optional bytes  BYTES = 19;
  // Warning: generic mapping from Type.NULL => bytes
  optional bytes  NULL = 20;
}
"""

struct="""syntax = "proto3";
message struct {
  message m_flat {
    // Warning: generic mapping from Type.NUMBER => bytes
    optional bytes  NUMBER = 1;
    // Warning: generic mapping from Type.DECIMAL => bytes
    optional bytes  DECIMAL = 2;
    // Warning: generic mapping from Type.NUMERIC => bytes
    optional bytes  NUMERIC = 3;
    optional int32  INT = 4;
    optional int32  INTEGER = 5;
    optional int64  LONG = 6;
    // Warning: generic mapping from Type.BIGINT => bytes
    optional bytes  BIGINT = 7;
    optional float  FLOAT = 8;
    optional double  DOUBLE = 9;
    optional string  STRING = 10;
    optional string  TEXT = 11;
    optional string  VARCHAR = 12;
    optional bool  BOOLEAN = 13;
    // Warning: generic mapping from Type.TIMESTAMP => bytes
    optional bytes  TIMESTAMP = 14;
    // Warning: generic mapping from Type.TIMESTAMP_TZ => bytes
    optional bytes  TIMESTAMP_TZ = 15;
    // Warning: generic mapping from Type.TIMESTAMP_NTZ => bytes
    optional bytes  TIMESTAMP_NTZ = 16;
    // Warning: generic mapping from Type.DATE => bytes
    optional bytes  DATE = 17;
    // Warning: generic mapping from Type.ARRAY => bytes
    optional bytes  ARRAY = 18;
    optional bytes  BYTES = 19;
    // Warning: generic mapping from Type.NULL => bytes
    optional bytes  NULL = 20;
  }
  message m_nested {
    // Warning: generic mapping from Type.STRUCT => bytes
    optional bytes  a = 1;
    // Warning: generic mapping from Type.STRUCT => bytes
    optional bytes  b = 2;
  }
  // Warning: generic mapping from Type.STRUCT => bytes
  optional bytes  flat = 1;
  // Warning: generic mapping from Type.STRUCT => bytes
  optional bytes  nested = 2;
}
"""

REFS={"basic": basic, "struct": struct}
