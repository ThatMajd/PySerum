"""
Filter module for PySerum.

Serum has 2 voice filters: VoiceFilter0 and VoiceFilter1
"""

from __future__ import annotations
from typing import Any

from .module import SerumModule
from .parameter import ParameterDescriptor, StringParameterDescriptor


class VoiceFilter(SerumModule):
    """
    Voice filter (VoiceFilter0 or VoiceFilter1).
    
    Uses user-friendly names from notes.md Serum UI column.
    """
    
    MODULE_TYPE = "VoiceFilter"
    
    # Enable
    enable = ParameterDescriptor("enable", param_id=0, json_name="kParamEnable", default=0.0)
    
    # Parameters from notes.md - VoiceFilter section
    # ID 1: Wet
    wet = ParameterDescriptor("wet", param_id=1, json_name="kParamWet", default=100.0)
    # ID 3: Freq (Cutoff)
    cutoff = ParameterDescriptor("cutoff", param_id=3, json_name="kParamFreq", default=0.0)
    # ID 4: Res (Resonance)
    resonance = ParameterDescriptor("resonance", param_id=4, json_name="kParamReso", default=0.0)
    # ID 5: Drive
    drive = ParameterDescriptor("drive", param_id=5, json_name="kParamDrive", default=0.0)
    # ID 6: Var (varies per filter type)
    var = ParameterDescriptor("var", param_id=6, json_name="kParamVar", default=0.0)
    # ID 7: Pan (Stereo)
    pan = ParameterDescriptor("pan", param_id=7, json_name="kParamStereo", default=0.0)
    # ID 8: Level (Output)
    level = ParameterDescriptor("level", param_id=8, json_name="kParamLevelOut", default=1.0)
    
    # Key tracking (not in notes.md table but exists)
    key_track = ParameterDescriptor("key_track", param_id=9, json_name="kParamKeyTrack", default=0.0)
    
    # String parameters
    type = StringParameterDescriptor("kParamType", default="kNone")
    
    def __init__(self, index: int = 0):
        if index not in (0, 1):
            raise ValueError(f"Filter index must be 0 or 1, got {index}")
        super().__init__(index)
    
    @property
    def enabled(self) -> bool:
        return self.enable.value == 1.0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        return {"plainParams": self.to_plain_params()}
    
    @classmethod
    def from_dict(cls, index: int, data: dict[str, Any]) -> VoiceFilter:
        """Create from JSON dictionary."""
        instance = cls(index)
        plain = data.get("plainParams", {})
        instance.load_plain_params(plain)
        return instance
