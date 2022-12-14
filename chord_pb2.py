# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chord.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x63hord.proto\":\n\x10TSuccessResponse\x12\x15\n\ris_successful\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x08\n\x06TEmpty\"0\n\x10TRegisterRequest\x12\x0e\n\x06ipaddr\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"0\n\x11TRegisterResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\" \n\x12TDeregisterRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"/\n\nTIdAndAddr\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x15\n\rport_and_addr\x18\x02 \x01(\t\")\n\x1bTPopulateFingerTableRequest\x12\n\n\x02id\x18\x01 \x01(\x05\":\n\x1cTPopulateFingerTableResponse\x12\x1a\n\x05nodes\x18\x01 \x03(\x0b\x32\x0b.TIdAndAddr\"3\n\x15TGetChordInfoResponse\x12\x1a\n\x05nodes\x18\x01 \x03(\x0b\x32\x0b.TIdAndAddr\"A\n\x17TGetFingerTableResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x1a\n\x05nodes\x18\x02 \x03(\x0b\x32\x0b.TIdAndAddr\"&\n\tTKeyValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\"\x1f\n\x11TGetValuesRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"0\n\x12TGetValuesResponse\x12\x1a\n\x06values\x18\x01 \x03(\x0b\x32\n.TKeyValue\")\n\x0cTSaveRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\"\x1a\n\x0bTKeyRequest\x12\x0b\n\x03key\x18\x01 \x01(\t2\xfc\x01\n\x08Registry\x12\x31\n\x08register\x12\x11.TRegisterRequest\x1a\x12.TRegisterResponse\x12\x34\n\nderegister\x12\x13.TDeregisterRequest\x1a\x11.TSuccessResponse\x12T\n\x15populate_finger_table\x12\x1c.TPopulateFingerTableRequest\x1a\x1d.TPopulateFingerTableResponse\x12\x31\n\x0eget_chord_info\x12\x07.TEmpty\x1a\x16.TGetChordInfoResponse2\xf2\x01\n\x04Node\x12\x35\n\x10get_finger_table\x12\x07.TEmpty\x1a\x18.TGetFingerTableResponse\x12\x35\n\nget_values\x12\x12.TGetValuesRequest\x1a\x13.TGetValuesResponse\x12(\n\x04save\x12\r.TSaveRequest\x1a\x11.TSuccessResponse\x12\'\n\x04\x66ind\x12\x0c.TKeyRequest\x1a\x11.TSuccessResponse\x12)\n\x06remove\x12\x0c.TKeyRequest\x1a\x11.TSuccessResponse25\n\x07\x43onnect\x12*\n\x0cservice_info\x12\x07.TEmpty\x1a\x11.TSuccessResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chord_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TSUCCESSRESPONSE._serialized_start=15
  _TSUCCESSRESPONSE._serialized_end=73
  _TEMPTY._serialized_start=75
  _TEMPTY._serialized_end=83
  _TREGISTERREQUEST._serialized_start=85
  _TREGISTERREQUEST._serialized_end=133
  _TREGISTERRESPONSE._serialized_start=135
  _TREGISTERRESPONSE._serialized_end=183
  _TDEREGISTERREQUEST._serialized_start=185
  _TDEREGISTERREQUEST._serialized_end=217
  _TIDANDADDR._serialized_start=219
  _TIDANDADDR._serialized_end=266
  _TPOPULATEFINGERTABLEREQUEST._serialized_start=268
  _TPOPULATEFINGERTABLEREQUEST._serialized_end=309
  _TPOPULATEFINGERTABLERESPONSE._serialized_start=311
  _TPOPULATEFINGERTABLERESPONSE._serialized_end=369
  _TGETCHORDINFORESPONSE._serialized_start=371
  _TGETCHORDINFORESPONSE._serialized_end=422
  _TGETFINGERTABLERESPONSE._serialized_start=424
  _TGETFINGERTABLERESPONSE._serialized_end=489
  _TKEYVALUE._serialized_start=491
  _TKEYVALUE._serialized_end=529
  _TGETVALUESREQUEST._serialized_start=531
  _TGETVALUESREQUEST._serialized_end=562
  _TGETVALUESRESPONSE._serialized_start=564
  _TGETVALUESRESPONSE._serialized_end=612
  _TSAVEREQUEST._serialized_start=614
  _TSAVEREQUEST._serialized_end=655
  _TKEYREQUEST._serialized_start=657
  _TKEYREQUEST._serialized_end=683
  _REGISTRY._serialized_start=686
  _REGISTRY._serialized_end=938
  _NODE._serialized_start=941
  _NODE._serialized_end=1183
  _CONNECT._serialized_start=1185
  _CONNECT._serialized_end=1238
# @@protoc_insertion_point(module_scope)
