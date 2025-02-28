import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, modbus
from esphome.const import (
    CONF_ACTIVE_POWER,
    CONF_APPARENT_POWER,
    CONF_CURRENT,
    CONF_EXPORT_ACTIVE_ENERGY,
    CONF_EXPORT_REACTIVE_ENERGY,
    CONF_FREQUENCY,
    CONF_ID,
    CONF_IMPORT_ACTIVE_ENERGY,
    CONF_IMPORT_REACTIVE_ENERGY,
    CONF_POWER_FACTOR,
    CONF_REACTIVE_POWER,
    CONF_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_EMPTY,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_POWER_FACTOR,
    DEVICE_CLASS_VOLTAGE,
    ICON_CURRENT_AC,
    ICON_EMPTY,
    LAST_RESET_TYPE_AUTO,
    STATE_CLASS_MEASUREMENT,
    UNIT_AMPERE,
    UNIT_EMPTY,
    UNIT_HERTZ,
    UNIT_VOLT,
    UNIT_VOLT_AMPS,
    UNIT_VOLT_AMPS_REACTIVE,
    UNIT_WATT,
)

AUTO_LOAD = ["modbus"]
CODEOWNERS = ["@sourabhjaiswal"]

CONF_TOTAL_ACTIVE_ENERGY = "total_active_energy"
CONF_TOTAL_REACTIVE_ENERGY = "total_reactive_energy"
CONF_APPARENT_ENERGY = "apparent_energy"
CONF_MAXIMUM_DEMAND_ACTIVE_POWER = "maximum_demand_active_power"
CONF_MAXIMUM_DEMAND_REACTIVE_POWER = "maximum_demand_reactive_power"
CONF_MAXIMUM_DEMAND_APPARENT_POWER = "maximum_demand_apparent_power"

UNIT_KILOWATT_HOURS = "kWh"
UNIT_KILOVOLT_AMPS_HOURS = "kVAh"
UNIT_KILOVOLT_AMPS_REACTIVE_HOURS = "kVARh"

selec_meter_ns = cg.esphome_ns.namespace("selec_meter")
SelecMeter = selec_meter_ns.class_(
    "SelecMeter", cg.PollingComponent, modbus.ModbusDevice
)

SENSORS = {
    CONF_TOTAL_ACTIVE_ENERGY: sensor.sensor_schema(
        UNIT_KILOWATT_HOURS,
        ICON_EMPTY,
        2,
        DEVICE_CLASS_ENERGY,
        STATE_CLASS_MEASUREMENT,
        LAST_RESET_TYPE_AUTO,
    ),
    CONF_IMPORT_ACTIVE_ENERGY: sensor.sensor_schema(
        UNIT_KILOWATT_HOURS,
        ICON_EMPTY,
        2,
        DEVICE_CLASS_ENERGY,
        STATE_CLASS_MEASUREMENT,
        LAST_RESET_TYPE_AUTO,
    ),
    CONF_EXPORT_ACTIVE_ENERGY: sensor.sensor_schema(
        UNIT_KILOWATT_HOURS,
        ICON_EMPTY,
        2,
        DEVICE_CLASS_ENERGY,
        STATE_CLASS_MEASUREMENT,
        LAST_RESET_TYPE_AUTO,
    ),
    CONF_TOTAL_REACTIVE_ENERGY: sensor.sensor_schema(
        UNIT_KILOVOLT_AMPS_REACTIVE_HOURS,
        ICON_EMPTY,
        2,
        DEVICE_CLASS_ENERGY,
        STATE_CLASS_MEASUREMENT,
        LAST_RESET_TYPE_AUTO,
    ),
    CONF_IMPORT_REACTIVE_ENERGY: sensor.sensor_schema(
        UNIT_KILOVOLT_AMPS_REACTIVE_HOURS,
        ICON_EMPTY,
        2,
        DEVICE_CLASS_ENERGY,
        STATE_CLASS_MEASUREMENT,
        LAST_RESET_TYPE_AUTO,
    ),
    CONF_EXPORT_REACTIVE_ENERGY: sensor.sensor_schema(
        UNIT_KILOVOLT_AMPS_REACTIVE_HOURS,
        ICON_EMPTY,
        2,
        DEVICE_CLASS_ENERGY,
        STATE_CLASS_MEASUREMENT,
        LAST_RESET_TYPE_AUTO,
    ),
    CONF_APPARENT_ENERGY: sensor.sensor_schema(
        UNIT_KILOVOLT_AMPS_HOURS,
        ICON_EMPTY,
        2,
        DEVICE_CLASS_ENERGY,
        STATE_CLASS_MEASUREMENT,
        LAST_RESET_TYPE_AUTO,
    ),
    CONF_ACTIVE_POWER: sensor.sensor_schema(
        UNIT_WATT, ICON_EMPTY, 3, DEVICE_CLASS_POWER, STATE_CLASS_MEASUREMENT
    ),
    CONF_REACTIVE_POWER: sensor.sensor_schema(
        UNIT_VOLT_AMPS_REACTIVE,
        ICON_EMPTY,
        3,
        DEVICE_CLASS_POWER,
        STATE_CLASS_MEASUREMENT,
    ),
    CONF_APPARENT_POWER: sensor.sensor_schema(
        UNIT_VOLT_AMPS, ICON_EMPTY, 3, DEVICE_CLASS_POWER, STATE_CLASS_MEASUREMENT
    ),
    CONF_VOLTAGE: sensor.sensor_schema(
        UNIT_VOLT, ICON_EMPTY, 2, DEVICE_CLASS_VOLTAGE, STATE_CLASS_MEASUREMENT
    ),
    CONF_CURRENT: sensor.sensor_schema(
        UNIT_AMPERE, ICON_EMPTY, 3, DEVICE_CLASS_CURRENT, STATE_CLASS_MEASUREMENT
    ),
    CONF_POWER_FACTOR: sensor.sensor_schema(
        UNIT_EMPTY, ICON_EMPTY, 3, DEVICE_CLASS_POWER_FACTOR, STATE_CLASS_MEASUREMENT
    ),
    CONF_FREQUENCY: sensor.sensor_schema(
        UNIT_HERTZ, ICON_CURRENT_AC, 2, DEVICE_CLASS_EMPTY, STATE_CLASS_MEASUREMENT
    ),
    CONF_MAXIMUM_DEMAND_ACTIVE_POWER: sensor.sensor_schema(
        UNIT_WATT, ICON_EMPTY, 3, DEVICE_CLASS_POWER, STATE_CLASS_MEASUREMENT
    ),
    CONF_MAXIMUM_DEMAND_REACTIVE_POWER: sensor.sensor_schema(
        UNIT_VOLT_AMPS_REACTIVE,
        ICON_EMPTY,
        3,
        DEVICE_CLASS_POWER,
        STATE_CLASS_MEASUREMENT,
    ),
    CONF_MAXIMUM_DEMAND_APPARENT_POWER: sensor.sensor_schema(
        UNIT_VOLT_AMPS, ICON_EMPTY, 3, DEVICE_CLASS_POWER, STATE_CLASS_MEASUREMENT
    ),
}

CONFIG_SCHEMA = (
    cv.Schema({cv.GenerateID(): cv.declare_id(SelecMeter)})
    .extend(
        {cv.Optional(sensor_name): schema for sensor_name, schema in SENSORS.items()}
    )
    .extend(cv.polling_component_schema("10s"))
    .extend(modbus.modbus_device_schema(0x01))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await modbus.register_modbus_device(var, config)
    for name in SENSORS:
        if name in config:
            sens = await sensor.new_sensor(config[name])
            cg.add(getattr(var, f"set_{name}_sensor")(sens))
