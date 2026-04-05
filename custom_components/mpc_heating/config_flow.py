"""Config flow for MPC Heating."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    CONF_CARNOT_EFFICIENCY_ENTITY,
    CONF_DEBUG_TEXT_ENTITY,
    CONF_INDOOR_TEMP_ENTITY,
    CONF_OUTDOOR_TEMP_ENTITY,
    CONF_OUTLET_TEMP_ENTITY,
    CONF_OVERHEAT_ENTITY,
    CONF_SUGGESTED_FLOW_ENTITY,
    CONF_TARGET_FLOW_ENTITY,
    CONF_THREE_WAY_VALVE_ENTITY,
    DOMAIN,
)


class MPCHeatingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MPC Heating."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="MPC Heating", data=user_input)

        entity_selector = selector.EntitySelector(selector.EntitySelectorConfig())

        schema = vol.Schema(
            {
                vol.Required(CONF_TARGET_FLOW_ENTITY): entity_selector,
                vol.Required(CONF_OUTLET_TEMP_ENTITY): entity_selector,
                vol.Required(CONF_OVERHEAT_ENTITY): entity_selector,
                vol.Required(CONF_INDOOR_TEMP_ENTITY): entity_selector,
                vol.Required(CONF_OUTDOOR_TEMP_ENTITY): entity_selector,
                vol.Required(CONF_CARNOT_EFFICIENCY_ENTITY): entity_selector,
                vol.Required(CONF_SUGGESTED_FLOW_ENTITY): entity_selector,
                vol.Required(CONF_DEBUG_TEXT_ENTITY): entity_selector,
                vol.Required(CONF_THREE_WAY_VALVE_ENTITY): entity_selector,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema)
