"""Sensor platform for MPC Heating."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import COORDINATOR, DOMAIN
from .coordinator import MPCHeatingCoordinator, SourceSnapshot


@dataclass(frozen=True, kw_only=True)
class MPCHeatingSensorDescription(SensorEntityDescription):
    """Description of an MPC Heating sensor."""

    source_key: str


SENSOR_DESCRIPTIONS: tuple[MPCHeatingSensorDescription, ...] = (
    MPCHeatingSensorDescription(
        key="target_flow",
        name="Pumpun pyynti",
        icon="mdi:thermometer-chevron-up",
        source_key="target_flow",
    ),
    MPCHeatingSensorDescription(
        key="outlet_temp",
        name="Todellinen meno",
        icon="mdi:thermometer",
        source_key="outlet_temp",
    ),
    MPCHeatingSensorDescription(
        key="overheat",
        name="Overheat",
        icon="mdi:thermometer-alert",
        source_key="overheat",
    ),
    MPCHeatingSensorDescription(
        key="indoor_temp",
        name="Sisälämpö",
        icon="mdi:home-thermometer",
        source_key="indoor_temp",
    ),
    MPCHeatingSensorDescription(
        key="outdoor_temp",
        name="Ulkolämpö",
        icon="mdi:snowflake-thermometer",
        source_key="outdoor_temp",
    ),
    MPCHeatingSensorDescription(
        key="carnot_efficiency",
        name="Carnot hyötysuhde",
        icon="mdi:gauge",
        source_key="carnot_efficiency",
    ),
    MPCHeatingSensorDescription(
        key="suggested_flow",
        name="MPC ehdotettu menovesi",
        icon="mdi:chart-line",
        source_key="suggested_flow",
    ),
    MPCHeatingSensorDescription(
        key="debug_text",
        name="Debug teksti",
        icon="mdi:text-box-search-outline",
        source_key="debug_text",
    ),
    MPCHeatingSensorDescription(
        key="three_way_valve",
        name="3-tieventtiilin tila",
        icon="mdi:valve",
        source_key="three_way_valve",
    ),
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: dict,
    async_add_entities: AddEntitiesCallback,
    discovery_info: dict | None = None,
) -> None:
    """Set up MPC Heating sensors."""
    coordinator: MPCHeatingCoordinator = hass.data[DOMAIN][COORDINATOR]

    async_add_entities(
        MPCHeatingSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
    )


class MPCHeatingSensor(CoordinatorEntity[MPCHeatingCoordinator], SensorEntity):
    """Representation of an MPC Heating sensor."""

    entity_description: MPCHeatingSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MPCHeatingCoordinator,
        description: MPCHeatingSensorDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{description.key}"
        self._attr_name = description.name

    @property
    def available(self) -> bool:
        """Return availability."""
        snapshot = self._snapshot
        return super().available and snapshot is not None and snapshot.available

    @property
    def native_value(self) -> str | float | int | None:
        """Return the sensor state."""
        snapshot = self._snapshot
        if snapshot is None:
            return None
        return snapshot.native_value

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return unit from the mirrored source entity."""
        snapshot = self._snapshot
        if snapshot is None:
            return None
        return snapshot.unit

    @property
    def icon(self) -> str | None:
        """Return icon."""
        snapshot = self._snapshot
        if snapshot and snapshot.icon:
            return snapshot.icon
        return self.entity_description.icon

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        """Return extra state attributes."""
        snapshot = self._snapshot
        if snapshot is None:
            return {}

        return {
            "source_entity_id": snapshot.entity_id,
            "source_state": snapshot.state,
        }

    @property
    def _snapshot(self) -> SourceSnapshot | None:
        """Return the current source snapshot."""
        return self.coordinator.data.get(self.entity_description.source_key)
