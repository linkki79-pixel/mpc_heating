"""The MPC Heating integration."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import async_load_platform

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
    COORDINATOR,
    DOMAIN,
)
from .coordinator import MPCHeatingCoordinator

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_TARGET_FLOW_ENTITY): cv.entity_id,
                vol.Required(CONF_OUTLET_TEMP_ENTITY): cv.entity_id,
                vol.Required(CONF_OVERHEAT_ENTITY): cv.entity_id,
                vol.Required(CONF_INDOOR_TEMP_ENTITY): cv.entity_id,
                vol.Required(CONF_OUTDOOR_TEMP_ENTITY): cv.entity_id,
                vol.Required(CONF_CARNOT_EFFICIENCY_ENTITY): cv.entity_id,
                vol.Required(CONF_SUGGESTED_FLOW_ENTITY): cv.entity_id,
                vol.Required(CONF_DEBUG_TEXT_ENTITY): cv.entity_id,
                vol.Required(CONF_THREE_WAY_VALVE_ENTITY): cv.entity_id,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up MPC Heating from YAML."""
    conf = config.get(DOMAIN)
    if conf is None:
        return True

    coordinator = MPCHeatingCoordinator(hass=hass, source_config=conf)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][COORDINATOR] = coordinator

    hass.async_create_task(
        async_load_platform(hass, Platform.SENSOR, DOMAIN, {}, config)
    )

    _LOGGER.info("MPC Heating initialized in read-only mode")
    return True
