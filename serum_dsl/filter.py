"""
Filter module for Serum DSL.

Serum has 2 voice filters: VoiceFilter0 and VoiceFilter1
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class VoiceFilter:
    """
    Voice filter (VoiceFilter0 or VoiceFilter1).
    
    Parameters use exact JSON names.
    """
    
    index: int  # 0 or 1
    
    # Filter parameters
    kParamEnable: float = 0.0
    kParamType: str = "kNone"  # String param - filter type (e.g., "H18", "LadderMg")
    kParamFreq: float = 0.0  # Cutoff frequency (0.0 to 1.0)
    kParamReso: float = 0.0
    kParamDrive: float = 0.0
    kParamWet: float = 100.0
    kParamVar: float = 0.0
    kParamStereo: float = 0.0
    kParamLevelOut: float = 1.0
    kParamKeyTrack: float = 0.0  # Key tracking (0.0 or 1.0)
    
    def __post_init__(self):
        if self.index not in (0, 1):
            raise ValueError(f"Filter index must be 0 or 1, got {self.index}")
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        params = {}
        
        if self.kParamEnable != 0.0:
            params["kParamEnable"] = self.kParamEnable
        if self.kParamType != "kNone":
            params["kParamType"] = self.kParamType
        if self.kParamFreq != 0.0:
            params["kParamFreq"] = self.kParamFreq
        if self.kParamReso != 0.0:
            params["kParamReso"] = self.kParamReso
        if self.kParamDrive != 0.0:
            params["kParamDrive"] = self.kParamDrive
        if self.kParamWet != 100.0:
            params["kParamWet"] = self.kParamWet
        if self.kParamVar != 0.0:
            params["kParamVar"] = self.kParamVar
        if self.kParamStereo != 0.0:
            params["kParamStereo"] = self.kParamStereo
        if self.kParamLevelOut != 1.0:
            params["kParamLevelOut"] = self.kParamLevelOut
        if self.kParamKeyTrack != 0.0:
            params["kParamKeyTrack"] = self.kParamKeyTrack
            
        return {"plainParams": params if params else "default"}
    
    @classmethod
    def from_dict(cls, index: int, data: dict[str, Any]) -> "VoiceFilter":
        """Create from JSON dictionary."""
        plain = data.get("plainParams", {})
        if plain == "default":
            plain = {}
            
        return cls(
            index=index,
            kParamEnable=plain.get("kParamEnable", 0.0),
            kParamType=plain.get("kParamType", "kNone"),
            kParamFreq=plain.get("kParamFreq", 0.0),
            kParamReso=plain.get("kParamReso", 0.0),
            kParamDrive=plain.get("kParamDrive", 0.0),
            kParamWet=plain.get("kParamWet", 100.0),
            kParamVar=plain.get("kParamVar", 0.0),
            kParamStereo=plain.get("kParamStereo", 0.0),
            kParamLevelOut=plain.get("kParamLevelOut", 1.0),
            kParamKeyTrack=plain.get("kParamKeyTrack", 0.0),
        )


# Alias for backwards compatibility
Filter = VoiceFilter
