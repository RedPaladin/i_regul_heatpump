"""Platform for sensor integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfVolumeFlowRate,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import HeatPumpApiSensors
from .const import DOMAIN


@dataclass(frozen=True, kw_only=True)
class HeatPumpEntityDescription(SensorEntityDescription):
    """Describes a Heat Pump Sensor."""

    api_sensor_index: str


SENSOR_TYPES: tuple[HeatPumpEntityDescription, ...] = (
    HeatPumpEntityDescription(
        key="external_temperature",
        translation_key="external_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        api_sensor_index=HeatPumpApiSensors.SENSOR_OUTSIDE_TEMP_IDX,
    ),
    HeatPumpEntityDescription(
        key="ecs_temperature",
        translation_key="ecs_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        api_sensor_index=HeatPumpApiSensors.SENSOR_ECS_TEMP_IDX,
    ),
    HeatPumpEntityDescription(
        key="ecs_recirculation_temperature",
        translation_key="ecs_recirculation_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        api_sensor_index=HeatPumpApiSensors.SENSOR_ECS_RECIRCULATION_TEMP_IDX,
    ),
    HeatPumpEntityDescription(
        key="heating_flow_rate",
        translation_key="heating_flow_rate",
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfVolumeFlowRate.LITERS_PER_MINUTE,
        api_sensor_index=HeatPumpApiSensors.SENSOR_HEATING_FLOW_RATE_IDX,
    ),
    HeatPumpEntityDescription(
        key="others_energy_consumption",
        translation_key="others_energy_consumption",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        api_sensor_index=HeatPumpApiSensors.SENSOR_OTHERS_ENERGY_CONSUMPTION_IDX,
        suggested_display_precision=2,
        force_update=True,
    ),
    HeatPumpEntityDescription(
        key="heating_energy_consumption",
        translation_key="heating_energy_consumption",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        api_sensor_index=HeatPumpApiSensors.SENSOR_HEATING_ENERGY_CONSUMPTION_IDX,
        suggested_display_precision=2,
        force_update=True,
    ),
    HeatPumpEntityDescription(
        key="cooling_energy_consumption",
        translation_key="cooling_energy_consumption",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        api_sensor_index=HeatPumpApiSensors.SENSOR_COOLING_ENERGY_CONSUMPTION_IDX,
        suggested_display_precision=2,
        force_update=True,
    ),
    HeatPumpEntityDescription(
        key="ecs_energy_consumption",
        translation_key="ecs_energy_consumption",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        api_sensor_index=HeatPumpApiSensors.SENSOR_ECS_ENERGY_CONSUMPTION_IDX,
        suggested_display_precision=2,
        force_update=True,
    ),
    HeatPumpEntityDescription(
        key="defrost_energy_consumption",
        translation_key="defrost_energy_consumption",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        api_sensor_index=HeatPumpApiSensors.SENSOR_DEFROST_ENERGY_CONSUMPTION_IDX,
        suggested_display_precision=2,
        force_update=True,
    ),
    HeatPumpEntityDescription(
        key="total_energy_consumption",
        translation_key="total_energy_consumption",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        api_sensor_index=HeatPumpApiSensors.SENSOR_TOTAL_ENERGY_CONSUMPTION_IDX,
        suggested_display_precision=2,
        force_update=True,
    ),
    HeatPumpEntityDescription(
        key="counter_energy_consumption",
        translation_key="counter_energy_consumption",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        api_sensor_index=HeatPumpApiSensors.SENSOR_COUNTER_ENERGY_CONSUMPTION_IDX,
        suggested_display_precision=2,
        force_update=True,
    ),
    HeatPumpEntityDescription(
        key="produced_power",
        translation_key="produced_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        api_sensor_index=HeatPumpApiSensors.SENSOR_PRODUCED_POWER_IDX,
        suggested_display_precision=2,
    ),
    HeatPumpEntityDescription(
        key="absorbed_power",
        translation_key="absorbed_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        api_sensor_index=HeatPumpApiSensors.SENSOR_ABSORBED_POWER_IDX,
        suggested_display_precision=2,
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
        HeatPumpSensor(coordinator, api, description) for description in SENSOR_TYPES
    ]
    async_add_entities(entities, True)

    return True


class HeatPumpSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Heat Pump Sensor."""

    _attr_has_entity_name = True
    entity_description: HeatPumpEntityDescription

    def __init__(
        self, coordinator, api, description: HeatPumpEntityDescription
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description
        # self._attr_device_info = api.device_info
        self.entity_id = f"sensor.{DOMAIN}_{description.key}"
        self._attr_unique_id = f"{DOMAIN}-{description.key}"
        self._api = api
        super().__init__(coordinator)

    @property
    def available(self) -> bool:
        """Check whether data is available."""
        return self._api.data_available(self.entity_description.api_sensor_index)

    @property
    def native_value(self) -> float:
        """Return the state of the sensor."""
        return self._api.get_value(self.entity_description.api_sensor_index)
