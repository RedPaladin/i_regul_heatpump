"""Constants for i-regul heat pump."""

from datetime import timedelta
import logging

DOMAIN = "i_regul_heatpump"

SCAN_INTERVAL = timedelta(seconds=30)

SERVER_HOST = "i-regul.fr"
SERVER_PORT = 443

VERSION = "0.0.0"

_LOGGER = logging.getLogger(DOMAIN)
