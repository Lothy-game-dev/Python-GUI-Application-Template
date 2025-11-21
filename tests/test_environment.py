from unittest.mock import patch
import sys


def frozen_config():
    """
    Directly set `sys.frozen` to True. This avoids the need for patching.
    """
    sys.frozen = True


def reset_frozen_config():
    """
    Remove the `frozen` attribute from `sys` after the test.
    """
    if hasattr(sys, "frozen"):
        del sys.frozen
