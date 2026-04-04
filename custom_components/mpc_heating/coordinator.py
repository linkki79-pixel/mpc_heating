from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class MPCHeatingCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name="mpc_heating",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        try:
            def get_float(entity):
                s = self.hass.states.get(entity)
                if not s or s.state in ("unknown", "unavailable"):
                    return 0.0
                return float(s.state)

            target = get_float("sensor.panasonic_heat_pump_main_z1_water_target_temp")
            actual = get_float("sensor.panasonic_heat_pump_main_main_outlet_temp")

            return {
                "target": target,
                "actual": actual,
                "overheat": max(0.0, actual - target),
            }

        except Exception as e:
            _LOGGER.error(f"MPC update failed: {e}")
            return {}
