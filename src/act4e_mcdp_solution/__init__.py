import coloredlogs

coloredlogs.install(level="DEBUG")

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from .solver_dp import *
from .solver_mcdp import *
