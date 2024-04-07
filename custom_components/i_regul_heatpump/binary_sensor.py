"""Platform for sensor integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import HeatPumpApiBinarySensors
from .const import DOMAIN


@dataclass(frozen=True, kw_only=True)
class HeatPumpBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a Heat Pump Binary Sensor."""

    api_sensor_index: str


BINARY_SENSOR_TYPES: tuple[HeatPumpBinarySensorEntityDescription, ...] = (
    HeatPumpBinarySensorEntityDescription(
        key="ecs_recirculation",
        translation_key="ecs_recirculation",
        api_sensor_index=HeatPumpApiBinarySensors.BINARY_SENSOR_ECS_RECIRCULATION_IDX,
    ),
    HeatPumpBinarySensorEntityDescription(
        key="ecs_producing",
        translation_key="ecs_producing",
        api_sensor_index=HeatPumpApiBinarySensors.BINARY_SENSOR_ECS_PRODUCING_IDX,
    ),
    HeatPumpBinarySensorEntityDescription(
        key="appoint_ecs_producing",
        translation_key="appoint_ecs_producing",
        api_sensor_index=HeatPumpApiBinarySensors.BINARY_SENSOR_APPOINT_ECS_PRODUCING_IDX,
    ),
    HeatPumpBinarySensorEntityDescription(
        key="additional_heating",
        translation_key="additional_heating",
        api_sensor_index=HeatPumpApiBinarySensors.BINARY_SENSOR_ADDITIONAL_HEATING_IDX,
    ),
    HeatPumpBinarySensorEntityDescription(
        key="compressor",
        translation_key="compressor",
        api_sensor_index=HeatPumpApiBinarySensors.BINARY_SENSOR_COMPRESSOR_IDX,
    ),
    HeatPumpBinarySensorEntityDescription(
        key="regulator",
        translation_key="regulator",
        api_sensor_index=HeatPumpApiBinarySensors.BINARY_SENSOR_REGULATOR_IDX,
    ),
    HeatPumpBinarySensorEntityDescription(
        key="captor",
        translation_key="captor",
        api_sensor_index=HeatPumpApiBinarySensors.BINARY_SENSOR_CAPTOR_IDX,
    ),
    HeatPumpBinarySensorEntityDescription(
        key="technical_circulator",
        translation_key="technical_circulator",
        api_sensor_index=HeatPumpApiBinarySensors.BINARY_TECHNICAL_CIRCULATOR_IDX,
    ),
    HeatPumpBinarySensorEntityDescription(
        key="buffer_tank_circulator",
        translation_key="buffer_tank_circulator",
        api_sensor_index=HeatPumpApiBinarySensors.BINARY_BUFFER_TANK_CIRCULATOR_IDX,
    ),
    HeatPumpBinarySensorEntityDescription(
        key="reversing_valve",
        translation_key="reversing_valve",
        api_sensor_index=HeatPumpApiBinarySensors.BINARY_REVERSING_VALVE_IDX,
    ),
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return

    api = hass.data[DOMAIN]["api"]
    coordinator = hass.data[DOMAIN]["coordinator"]

    entities = [
        HeatPumpBinarySensor(coordinator, api, description)
        for description in BINARY_SENSOR_TYPES
    ]
    async_add_entities(entities, True)

    return True


class HeatPumpBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Heat Pump Binary Sensor."""

    _attr_has_entity_name = True
    entity_description: HeatPumpBinarySensorEntityDescription

    def __init__(
        self, coordinator, api, description: HeatPumpBinarySensorEntityDescription
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description
        # self._attr_device_info = api.device_info
        self.entity_id = f"binary_sensor.{DOMAIN}_{description.key}"
        self._attr_unique_id = f"{DOMAIN}-{description.key}"
        self._api = api
        super().__init__(coordinator)

    @property
    def available(self) -> bool:
        """Check whether data is available."""
        return self._api.data_available(self.entity_description.api_sensor_index)

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self._api.get_value(self.entity_description.api_sensor_index) != 0.0
