"""Coordinator for MPC Heating."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, SOURCE_ENTITY_KEYS, UPDATE_INTERVAL_MINUTES

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class SourceSnapshot:
    """Snapshot of a source entity."""

    entity_id: str
    available: bool
    state: str | None
    native_value: str | float | int | None
    unit: str | None
    icon: str | None


class MPCHeatingCoordinator(DataUpdateCoordinator[dict[str, SourceSnapshot]]):
    """Coordinator to mirror selected source entities."""

    def __init__(self, hass: HomeAssistant, source_config: dict[str, str]) -> None:
        """Initialize the coordinator."""
        self._source_config = source_config

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=UPDATE_INTERVAL_MINUTES),
        )

    async def _async_update_data(self) -> dict[str, SourceSnapshot]:
        """Fetch data from Home Assistant state machine."""
        data: dict[str, SourceSnapshot] = {}

        for key, config_key in SOURCE_ENTITY_KEYS.items():
            entity_id = self._source_config[config_key]
            state_obj = self.hass.states.get(entity_id)
            data[key] = self._snapshot_from_state(entity_id, state_obj)

        return data

    @staticmethod
    def _snapshot_from_state(entity_id: str, state_obj: State | None) -> SourceSnapshot:
        """Build a snapshot from a Home Assistant state."""
        if state_obj is None:
            return SourceSnapshot(
                entity_id=entity_id,
                available=False,
                state=None,
                native_value=None,
                unit=None,
                icon=None,
            )

        state_str = state_obj.state
        if state_str in ("unknown", "unavailable"):
            return SourceSnapshot(
                entity_id=entity_id,
                available=False,
                state=state_str,
                native_value=None,
                unit=state_obj.attributes.get("unit_of_measurement"),
                icon=state_obj.attributes.get("icon"),
            )

        return SourceSnapshot(
            entity_id=entity_id,
            available=True,
            state=state_str,
            native_value=MPCHeatingCoordinator._coerce_value(state_str),
            unit=state_obj.attributes.get("unit_of_measurement"),
            icon=state_obj.attributes.get("icon"),
        )

    @staticmethod
    def _coerce_value(value: str) -> str | float | int:
        """Convert numeric strings to numbers, otherwise keep as string."""
        try:
            number = float(value)
        except ValueError:
            return value

        if number.is_integer():
            return int(number)

        return number
