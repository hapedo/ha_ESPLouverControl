from __future__ import annotations

import voluptuous as vol
from typing import Any
import logging
from .louver import Louver
from .mqtt_client import MqttClient
from .log import Log

# These constants are relevant to the type of entity we are using.
# See below for how they are used.
from homeassistant.components.cover import (
    PLATFORM_SCHEMA,
    SUPPORT_CLOSE,
    SUPPORT_OPEN,
    SUPPORT_STOP,
    SUPPORT_OPEN_TILT,
    SUPPORT_CLOSE_TILT,
    CoverEntity
)
from homeassistant.components.sensor import SensorEntity
# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME, CONF_HOST, CONF_PASSWORD, CONF_USERNAME, TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import homeassistant.helpers.config_validation as cv

DOMAIN = "louver"
CONF_CLIENTID_LIST = "client_id_list"
CONF_BROKER_IP = "broker_ip"
CONF_BROKER_PORT = "broker_port"
CONF_BROKER_USERNAME = "broker_username"
CONF_BROKER_PASSWORD = "broker_password"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_CLIENTID_LIST): cv.ensure_list,
        vol.Optional(CONF_BROKER_IP, default="localhost"): cv.string,
        vol.Optional(CONF_BROKER_PORT, default=1883): cv.port,
        vol.Optional(CONF_BROKER_USERNAME, default=""): cv.string,
        vol.Optional(CONF_BROKER_PASSWORD, default=""): cv.string,
    }
)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:

    # Add all entities to HA
    entities = []
    entities.append(LouverEntity(hass, config[CONF_NAME], config[CONF_CLIENTID_LIST], config[CONF_BROKER_IP], config[CONF_BROKER_PORT], config[CONF_BROKER_USERNAME], config[CONF_BROKER_PASSWORD]))
    #entities.append(ExampleSensor())
    add_entities(entities)

# This entire class could be written to extend a base class to ensure common attributes
# are kept identical/in sync. It's broken apart here between the Cover and Sensors to
# be explicit about what is returned, and the comments outline where the overlap is.
class LouverEntity(CoverEntity):
    """Representation of a dummy Cover."""

    supported_features = SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP | SUPPORT_OPEN_TILT

    def __init__(self, hass : HomeAssistant, name : str, clientIdList : List[str], brokerIp : str, brokerPort : int, brokerUsername : str, brokerPassword : str) -> None:
        """Initialize the sensor."""
        Log.configure(name)
        self.__louvers =[]
        self.__hass = hass
        uniqueId = ""
        for clientId in clientIdList:
            self.__louvers.append(Louver(clientId, brokerIp, brokerPort, brokerUsername, brokerPassword))
            uniqueId = uniqueId + clientId
        self._attr_unique_id = f"{uniqueId}_louver"
        self._attr_name = name

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "name": self.name
        }

    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        isAvailable = True
        for louver in self.__louvers:
            isAvailable = isAvailable & louver.isAvailable()
        Log.error(self._attr_name, "Available = {}".format(isAvailable))
        return isAvailable

    @property
    def is_closed(self) -> bool:
        """Return if the cover is closed, same as position 0."""
        isClosed = True
        for louver in self.__louvers:
            isClosed = isClosed & (louver.getPosition() == 0)
        return isClosed

    @property
    def is_closing(self) -> bool:
        """Return if the cover is closing or not."""
        isClosing = False
        for louver in self.__louvers:
            isClosing = isClosing | louver.isClosing()
        return isClosing

    @property
    def is_opening(self) -> bool:
        """Return if the cover is opening or not."""
        isOpening = False
        for louver in self.__louvers:
            isOpening = isOpening | louver.isOpening()
        return isOpening

    @property
    def current_cover_position(self) -> int:
        position = 0
        for louver in self.__louvers:
            position = position + louver.getPosition()
        position = position / len(self.__louvers)
        return position

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the cover."""
        for louver in self.__louvers:
            louver.open()

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the cover."""
        for louver in self.__louvers:
            louver.close()

    async def async_stop_cover(self, **kwargs):
        """Stop the cover."""
        for louver in self.__louvers:
            louver.stop()

    async def async_open_cover_tilt(self, **kwargs):
        """Open the cover tilt."""      
        for louver in self.__louvers:
            louver.closeAndOpenLamellas()

class ExampleSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Example Temperature'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self.hass.data[DOMAIN]['temperature']