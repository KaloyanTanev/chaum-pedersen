# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cp.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x08\x63p.proto\"4\n\x0fRegisterRequest\x12\n\n\x02y1\x18\x01 \x01(\t\x12\n\n\x02y2\x18\x02 \x01(\t\x12\t\n\x01p\x18\x03 \x01(\t\"-\n\x10RegisterResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\t\":\n\x14LoginRequestRoundOne\x12\n\n\x02id\x18\x01 \x01(\t\x12\n\n\x02r1\x18\x02 \x01(\t\x12\n\n\x02r2\x18\x03 \x01(\t\"1\n\x15LoginResponseRoundOne\x12\t\n\x01\x63\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\t\"-\n\x14LoginRequestRoundTwo\x12\n\n\x02id\x18\x01 \x01(\t\x12\t\n\x01s\x18\x02 \x01(\t\"1\n\x15LoginResponseRoundTwo\x12\t\n\x01\x62\x18\x01 \x01(\x08\x12\r\n\x05\x65rror\x18\x02 \x01(\t2\xbb\x01\n\x02\x43p\x12\x31\n\x08Register\x12\x10.RegisterRequest\x1a\x11.RegisterResponse\"\x00\x12@\n\rLoginRoundOne\x12\x15.LoginRequestRoundOne\x1a\x16.LoginResponseRoundOne\"\x00\x12@\n\rLoginRoundTwo\x12\x15.LoginRequestRoundTwo\x1a\x16.LoginResponseRoundTwo\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cp_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REGISTERREQUEST']._serialized_start=12
  _globals['_REGISTERREQUEST']._serialized_end=64
  _globals['_REGISTERRESPONSE']._serialized_start=66
  _globals['_REGISTERRESPONSE']._serialized_end=111
  _globals['_LOGINREQUESTROUNDONE']._serialized_start=113
  _globals['_LOGINREQUESTROUNDONE']._serialized_end=171
  _globals['_LOGINRESPONSEROUNDONE']._serialized_start=173
  _globals['_LOGINRESPONSEROUNDONE']._serialized_end=222
  _globals['_LOGINREQUESTROUNDTWO']._serialized_start=224
  _globals['_LOGINREQUESTROUNDTWO']._serialized_end=269
  _globals['_LOGINRESPONSEROUNDTWO']._serialized_start=271
  _globals['_LOGINRESPONSEROUNDTWO']._serialized_end=320
  _globals['_CP']._serialized_start=323
  _globals['_CP']._serialized_end=510
# @@protoc_insertion_point(module_scope)
