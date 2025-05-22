"""Definition of the Heat Pump API."""

import asyncio
from enum import StrEnum
import re

from .const import _LOGGER, SERVER_HOST, SERVER_PORT


class HeatPumpApiSensors(StrEnum):
    """List the different supported sensors."""

    # Temperature sensors [T°]
    SENSOR_OUTSIDE_TEMP_IDX = "A@3&valeur"
    SENSOR_ECS_TEMP_IDX = "A@1&valeur"
    SENSOR_ECS_RECIRCULATION_TEMP_IDX = "A@23&valeur"

    # Heating flow sensor [l/m]
    SENSOR_HEATING_FLOW_RATE_IDX = "A@21&valeur"

    # Energy consumption sensors [KWh]
    SENSOR_OTHERS_ENERGY_CONSUMPTION_IDX = "M@20&valeur"
    SENSOR_HEATING_ENERGY_CONSUMPTION_IDX = "M@21&valeur"
    SENSOR_COOLING_ENERGY_CONSUMPTION_IDX = "M@22&valeur"
    SENSOR_ECS_ENERGY_CONSUMPTION_IDX = "M@23&valeur"
    SENSOR_DEFROST_ENERGY_CONSUMPTION_IDX = "M@25&valeur"
    SENSOR_TOTAL_ENERGY_CONSUMPTION_IDX = "M@26&valeur"
    SENSOR_COUNTER_ENERGY_CONSUMPTION_IDX = "M@27&valeur"


class HeatPumpApiBinarySensors(StrEnum):
    """List the different supported binary sensors."""

    BINARY_SENSOR_ECS_PRODUCING_IDX = "O@1&valeur"  # Production ECS
    BINARY_SENSOR_APPOINT_ECS_PRODUCING_IDX = "O@7&valeur"  # Appoint ECS
    # BINARY_SENSOR_EXTERNAL_FUNCTION_IDX = "O@25&valeur"  # Chauffage ? NOT INTERESING
    BINARY_SENSOR_ECS_RECIRCULATION_IDX = "O@5&valeur"  # Circulation ECS

    BINARY_SENSOR_ADDITIONAL_HEATING_IDX = "O@101&valeur"  # Appoint chauffage

    BINARY_SENSOR_COMPRESSOR_IDX = "O@3&valeur"  # Compresseur
    BINARY_SENSOR_REGULATOR_IDX = "O@4&valeur"  # Détenteur
    BINARY_SENSOR_CAPTOR_IDX = "O@8&valeur"  # Capteur

    # BINARY_SENSOR_HEATING_COOLING_PRODUCTION_IDX = "O@26&valeur"  # Prod chaud/froid. NOT INTERESING
    # BINARY_SENSOR_HEATING_COOLING_SUPPLYING_IDX = "O@6&valeur"  # Distri chaud/froid. NOT INTERESING

    BINARY_TECHNICAL_CIRCULATOR_IDX = "O@100&valeur"  # Circulateur technique
    BINARY_BUFFER_TANK_CIRCULATOR_IDX = "O@60&valeur"  # Circulateur ballon tampon
    BINARY_REVERSING_VALVE_IDX = "O@10&valeur"  # Vanne inversion


REQUEST_ID = 10


class HeatPumpApiAuthException(Exception):
    """Error to indicate that an error occured when fetching the data from the heat pump."""


class HeatPumpApiRequestException(Exception):
    """Error to indicate that an error occured when fetching the data from the heat pump."""


class HeatPumpApi:
    """The class Heat Pump API."""

    def __init__(self, id, password) -> None:
        """Construct the API class."""
        self._id = id
        self._password = password

        self._regex = re.compile(r"#(\w+@\d+&\w+)\[(.*?)\]")
        self._data_dict = {}

    def _decode_data(self, data) -> None:
        for match in self._regex.finditer(data):
            if match.lastindex != 2:
                _LOGGER.warning("Something went wrong parsing data")
                return

            identifier, value = match.groups()

            self._data_dict[identifier] = value

    async def _fetch_data(self) -> None:
        message = f"cdraminfo{self._id}{self._password}{{{REQUEST_ID}#}}"

        writer = None
        try:
            reader, writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)

            _LOGGER.debug("Sending: %s", message)
            writer.write(message.encode())
            await writer.drain()

            data = await reader.readuntil(b"\r")

            if not data.endswith(b"\r"):
                _LOGGER.debug(
                    "Data doesn't end with line feed, some data may be missing"
                )

            if data.startswith(b"PWD}"):
                raise HeatPumpApiAuthException("Invalid credentials")

            _LOGGER.debug("Data received : %s", data.decode())

            self._decode_data(data.decode())

        finally:
            if writer is not None:
                writer.close()
                await writer.wait_closed()

    async def async_update(self):
        """Update the data from the cloud."""
        _LOGGER.debug("HeatPumpApi: async_update() called")

        await self._fetch_data()

    def data_available(self, idx) -> bool:
        """Get whether data from given index is available."""
        result = self._data_dict.get(idx) is not None
        _LOGGER.debug(
            "HeatPumpApi: data_available(%s) called (result: %s)", idx, result
        )
        return result

    def get_value(self, idx) -> float:
        """Get the value for the given index."""
        value = float(self._data_dict.get(idx))
        _LOGGER.debug("HeatPumpApi: get_value(%s) called (value: %s)", idx, value)
        return value
