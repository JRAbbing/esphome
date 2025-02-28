import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation, pins
from esphome.components import sensor
from esphome.const import (
    CONF_ID,
    CONF_INTERNAL_FILTER,
    CONF_PIN,
    CONF_NUMBER,
    CONF_TIMEOUT,
    CONF_TOTAL,
    CONF_VALUE,
    ICON_PULSE,
    LAST_RESET_TYPE_AUTO,
    STATE_CLASS_MEASUREMENT,
    UNIT_PULSES,
    UNIT_PULSES_PER_MINUTE,
    DEVICE_CLASS_EMPTY,
)
from esphome.core import CORE

CODEOWNERS = ["@stevebaxter"]

pulse_meter_ns = cg.esphome_ns.namespace("pulse_meter")

PulseMeterSensor = pulse_meter_ns.class_(
    "PulseMeterSensor", sensor.Sensor, cg.Component
)

SetTotalPulsesAction = pulse_meter_ns.class_("SetTotalPulsesAction", automation.Action)


def validate_internal_filter(value):
    return cv.positive_time_period_microseconds(value)


def validate_timeout(value):
    value = cv.positive_time_period_microseconds(value)
    if value.total_minutes > 70:
        raise cv.Invalid("Maximum timeout is 70 minutes")
    return value


def validate_pulse_meter_pin(value):
    value = pins.internal_gpio_input_pin_schema(value)
    if CORE.is_esp8266 and value[CONF_NUMBER] >= 16:
        raise cv.Invalid(
            "Pins GPIO16 and GPIO17 cannot be used as pulse counters on ESP8266."
        )
    return value


CONFIG_SCHEMA = sensor.sensor_schema(
    UNIT_PULSES_PER_MINUTE, ICON_PULSE, 2, DEVICE_CLASS_EMPTY, STATE_CLASS_MEASUREMENT
).extend(
    {
        cv.GenerateID(): cv.declare_id(PulseMeterSensor),
        cv.Required(CONF_PIN): validate_pulse_meter_pin,
        cv.Optional(CONF_INTERNAL_FILTER, default="13us"): validate_internal_filter,
        cv.Optional(CONF_TIMEOUT, default="5min"): validate_timeout,
        cv.Optional(CONF_TOTAL): sensor.sensor_schema(
            UNIT_PULSES,
            ICON_PULSE,
            0,
            DEVICE_CLASS_EMPTY,
            STATE_CLASS_MEASUREMENT,
            LAST_RESET_TYPE_AUTO,
        ),
    }
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await sensor.register_sensor(var, config)

    pin = await cg.gpio_pin_expression(config[CONF_PIN])
    cg.add(var.set_pin(pin))
    cg.add(var.set_filter_us(config[CONF_INTERNAL_FILTER]))
    cg.add(var.set_timeout_us(config[CONF_TIMEOUT]))

    if CONF_TOTAL in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL])
        cg.add(var.set_total_sensor(sens))


@automation.register_action(
    "pulse_meter.set_total_pulses",
    SetTotalPulsesAction,
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.use_id(PulseMeterSensor),
            cv.Required(CONF_VALUE): cv.templatable(cv.uint32_t),
        }
    ),
)
async def set_total_action_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config[CONF_VALUE], args, int)
    cg.add(var.set_total_pulses(template_))
    return var
