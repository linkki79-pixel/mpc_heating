from homeassistant.helpers.entity import Entity


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    from .coordinator import MPCHeatingCoordinator

    coordinator = MPCHeatingCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        MPCSensor(coordinator, "target", "MPC Flow Target"),
        MPCSensor(coordinator, "actual", "MPC Flow Actual"),
        MPCSensor(coordinator, "overheat", "MPC Overheat"),
    ])


class MPCSensor(Entity):
    def __init__(self, coordinator, key, name):
        self.coordinator = coordinator
        self._key = key
        self._attr_name = name

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    @property
    def state(self):
        return self.coordinator.data.get(self._key)
