"""
definitions from RFC 8724 [1] and corresponding data models.

[1] "SCHC: Generic Framework for Static Context Header Compression and Fragmentation" , A. Minaburo et al.
"""

from enum import Enum
from dataclasses import dataclass
from typing import  Dict, List, Tuple, Union

Value = Union[int, bytes]

@dataclass
class Pattern:
    pattern: bytes
    length: int

ReverseMapping = Dict[int, Value]
Mapping = Dict[Value, int]


class MatchMapping:
    def __init__(self, index_length: int, forward_mapping: Mapping):
        self.index_length: int = index_length
        self.forward: Mapping = forward_mapping
        self.reverse: ReverseMapping = {v: k for k, v in self.forward.items()}

TargetValue = Union[Value, Pattern, MatchMapping]

class DirectionIndicator(str, Enum):
    UP = 'Up'
    DOWN = 'Dw'
    BIDIRECTIONAL = 'Bi'


class MatchingOperator(str, Enum):
    EQUAL = 'equal'
    IGNORE = 'ignore'
    MSB = 'MSB'
    MATCH_MAPPING = 'match-mapping'

class CompressionDecompressionAction(str, Enum):
    NOT_SENT = 'not-sent'
    LSB = 'least-significant-bits'
    MAPPING_SENT = 'mapping-sent'
    VALUE_SENT = 'value-sent'


@dataclass
class FieldDescriptor:
    id: str
    length: int
    position: int
    value: Value


@dataclass
class HeaderDescriptor:
    id: str
    length: int
    fields: List[FieldDescriptor]


@dataclass
class PacketDescriptor:
    direction: DirectionIndicator
    headers: List[HeaderDescriptor]


@dataclass
class FieldResidue:
    residue: bytes
    length: int

@dataclass
class RuleFieldDescriptor:
    id: str
    length: int
    position: int
    direction: DirectionIndicator
    target_value: TargetValue
    matching_operator: MatchingOperator
    compression_decompression_action: CompressionDecompressionAction

@dataclass
class RuleDescriptor:
    id: int
    field_descriptors: List[RuleFieldDescriptor]
