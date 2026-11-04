from datasheet_cli.models import Component, Pin, PinType, Net, ReferenceCircuit


def test_reference_circuit_creation():
    u1 = Component(
        reference="U1",
        part_number="TPS54302",
        footprint="Package_TO_SOT_SMD:SOT-23-6",
        pins=[
            Pin(number="1", name="GND", pin_type=PinType.POWER_IN),
            Pin(number="2", name="SW", pin_type=PinType.OUTPUT),
            Pin(number="3", name="VIN", pin_type=PinType.POWER_IN),
            Pin(number="4", name="FB", pin_type=PinType.INPUT),
            Pin(number="5", name="EN", pin_type=PinType.INPUT),
            Pin(number="6", name="BOOT", pin_type=PinType.PASSIVE),
        ],
    )
    c_in = Component(
        reference="C1",
        value="10uF",
        footprint="Capacitor_SMD:C_1206",
        pins=[
            Pin(number="1", name="1", pin_type=PinType.PASSIVE),
            Pin(number="2", name="2", pin_type=PinType.PASSIVE),
        ],
    )
    net_vin = Net(name="VIN", connections=["U1:3", "C1:1"])

    circuit = ReferenceCircuit(
        title="TPS54302 12V to 3.3V Step-Down Converter",
        source_part_number="TPS54302",
        source_page=16,
        components=[u1, c_in],
        nets=[net_vin],
    )

    assert circuit.source_part_number == "TPS54302"
    assert len(circuit.components) == 2
    assert len(circuit.nets) == 1
    assert circuit.nets[0].name == "VIN"
