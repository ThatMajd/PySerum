"""
PySerum - A Pythonic DSL for Serum2 preset generation.

This package provides a user-friendly interface to create and modify
Serum2 synthesizer presets programmatically.
"""

from .preset import SerumPreset
from .mod_source import ModSource
from .oscillator import Oscillator, NoiseOscillator, SubOscillator
from .filter import VoiceFilter

__all__ = [
    "SerumPreset",
    "ModSource",
    "Oscillator",
    "NoiseOscillator",
    "SubOscillator",
    "VoiceFilter",
]

__version__ = "0.2.0"
