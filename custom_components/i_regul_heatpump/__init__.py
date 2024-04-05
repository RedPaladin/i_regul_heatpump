"""i-regul Heat Pump component."""

from datetime import timedelta

import voluptuous as vol

from homeassistant.const import CONF_ID, CONF_PASSWORD, CONF_SCAN_INTERVAL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, discovery
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import HeatPumpApi
from .const import _LOGGER, DOMAIN

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_ID): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=300): cv.positive_int,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the component."""

    hass.data.setdefault(DOMAIN, {})

    api = HeatPumpApi(config[DOMAIN][CONF_ID], config[DOMAIN][CONF_PASSWORD])
    hass.data[DOMAIN]["api"] = api

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=api.async_update,
        update_interval=timedelta(seconds=config[DOMAIN][CONF_SCAN_INTERVAL]),
    )
    hass.data[DOMAIN]["coordinator"] = coordinator

    for platform in PLATFORMS:
        hass.async_create_task(
            discovery.async_load_platform(hass, platform, DOMAIN, {}, config)
        )

    return True
