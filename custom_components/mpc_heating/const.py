"""Constants for the MPC Heating integration."""

from __future__ import annotations

DOMAIN = "mpc_heating"
COORDINATOR = "coordinator"
UPDATE_INTERVAL_MINUTES = 5

CONF_TARGET_FLOW_ENTITY = "target_flow_entity"
CONF_OUTLET_TEMP_ENTITY = "outlet_temp_entity"
CONF_OVERHEAT_ENTITY = "overheat_entity"
CONF_INDOOR_TEMP_ENTITY = "indoor_temp_entity"
CONF_OUTDOOR_TEMP_ENTITY = "outdoor_temp_entity"
CONF_CARNOT_EFFICIENCY_ENTITY = "carnot_efficiency_entity"
CONF_SUGGESTED_FLOW_ENTITY = "suggested_flow_entity"
CONF_DEBUG_TEXT_ENTITY = "debug_text_entity"
CONF_THREE_WAY_VALVE_ENTITY = "three_way_valve_entity"

SOURCE_ENTITY_KEYS: dict[str, str] = {
    "target_flow": CONF_TARGET_FLOW_ENTITY,
    "outlet_temp": CONF_OUTLET_TEMP_ENTITY,
    "overheat": CONF_OVERHEAT_ENTITY,
    "indoor_temp": CONF_INDOOR_TEMP_ENTITY,
    "outdoor_temp": CONF_OUTDOOR_TEMP_ENTITY,
    "carnot_efficiency": CONF_CARNOT_EFFICIENCY_ENTITY,
    "suggested_flow": CONF_SUGGESTED_FLOW_ENTITY,
    "debug_text": CONF_DEBUG_TEXT_ENTITY,
    "three_way_valve": CONF_THREE_WAY_VALVE_ENTITY,
}
