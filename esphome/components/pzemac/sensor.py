import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, modbus
from esphome.const import (
    CONF_CURRENT,
    CONF_ENERGY,
    CONF_ID,
    CONF_POWER,
    CONF_VOLTAGE,
    CONF_FREQUENCY,
    CONF_POWER_FACTOR,
    DEVICE_CLASS_EMPTY,
    DEVICE_CLASS_POWER_FACTOR,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_ENERGY,
    ICON_EMPTY,
    ICON_CURRENT_AC,
    LAST_RESET_TYPE_AUTO,
    STATE_CLASS_MEASUREMENT,
    UNIT_HERTZ,
    UNIT_VOLT,
    UNIT_AMPERE,
    UNIT_WATT,
    UNIT_EMPTY,
    UNIT_WATT_HOURS,
)

AUTO_LOAD = ["modbus"]

pzemac_ns = cg.esphome_ns.namespace("pzemac")
PZEMAC = pzemac_ns.class_("PZEMAC", cg.PollingComponent, modbus.ModbusDevice)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(PZEMAC),
            cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                UNIT_VOLT, ICON_EMPTY, 1, DEVICE_CLASS_VOLTAGE, STATE_CLASS_MEASUREMENT
            ),
            cv.Optional(CONF_CURRENT): sensor.sensor_schema(
                UNIT_AMPERE,
                ICON_EMPTY,
                3,
                DEVICE_CLASS_CURRENT,
                STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_POWER): sensor.sensor_schema(
                UNIT_WATT, ICON_EMPTY, 2, DEVICE_CLASS_POWER, STATE_CLASS_MEASUREMENT
            ),
            cv.Optional(CONF_ENERGY): sensor.sensor_schema(
                UNIT_WATT_HOURS,
                ICON_EMPTY,
                0,
                DEVICE_CLASS_ENERGY,
                STATE_CLASS_MEASUREMENT,
                LAST_RESET_TYPE_AUTO,
            ),
            cv.Optional(CONF_FREQUENCY): sensor.sensor_schema(
                UNIT_HERTZ,
                ICON_CURRENT_AC,
                1,
                DEVICE_CLASS_EMPTY,
                STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_POWER_FACTOR): sensor.sensor_schema(
                UNIT_EMPTY,
                ICON_EMPTY,
                2,
                DEVICE_CLASS_POWER_FACTOR,
                STATE_CLASS_MEASUREMENT,
            ),
        }
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(modbus.modbus_device_schema(0x01))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await modbus.register_modbus_device(var, config)

    if CONF_VOLTAGE in config:
        conf = config[CONF_VOLTAGE]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_voltage_sensor(sens))
    if CONF_CURRENT in config:
        conf = config[CONF_CURRENT]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_current_sensor(sens))
    if CONF_POWER in config:
        conf = config[CONF_POWER]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_power_sensor(sens))
    if CONF_ENERGY in config:
        conf = config[CONF_ENERGY]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_energy_sensor(sens))
    if CONF_FREQUENCY in config:
        conf = config[CONF_FREQUENCY]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_frequency_sensor(sens))
    if CONF_POWER_FACTOR in config:
        conf = config[CONF_POWER_FACTOR]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_power_factor_sensor(sens))
