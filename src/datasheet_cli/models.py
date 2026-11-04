"""Core data models representing components, pins, nets, and reference schematics."""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PinType(str, Enum):
    POWER_IN = "power_in"
    POWER_OUT = "power_out"
    INPUT = "input"
    OUTPUT = "output"
    BIDIRECTIONAL = "bidirectional"
    PASSIVE = "passive"
    UNSPECIFIED = "unspecified"


class Pin(BaseModel):
    number: str
    name: str
    pin_type: PinType = PinType.UNSPECIFIED
    description: Optional[str] = None


class Component(BaseModel):
    reference: str  # e.g., "U1", "R1", "C1", "L1"
    part_number: Optional[str] = None
    value: Optional[str] = None  # e.g., "10k", "4.7uH", "100nF"
    footprint: Optional[str] = None  # e.g., "Package_TO_SOT_SMD:SOT-23-6"
    pins: List[Pin] = Field(default_factory=list)


class Net(BaseModel):
    name: str  # e.g., "VIN", "VOUT", "GND", "SW", "BOOT"
    connections: List[str] = Field(default_factory=list)  # e.g., ["U1:1", "C1:1"]


class DesignEquation(BaseModel):
    target_component: str  # e.g., "R_FB_TOP", "L1", "C_OUT"
    formula: str  # e.g., "VOUT = VREF * (1 + R1/R2)"
    description: Optional[str] = None
    variables: Dict[str, float] = Field(default_factory=dict)


class ReferenceCircuit(BaseModel):
    title: str
    source_part_number: str
    source_page: Optional[int] = None
    components: List[Component] = Field(default_factory=list)
    nets: List[Net] = Field(default_factory=list)
    equations: List[DesignEquation] = Field(default_factory=list)
