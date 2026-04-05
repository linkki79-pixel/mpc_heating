"""The MPC Heating integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import MPCHeatingCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up MPC Heating."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MPC Heating from a config entry."""
    coordinator = MPCHeatingCoordinator(hass=hass, config_entry=entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
