"""
Main Serum Preset class that ties everything together.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from .oscillator import Oscillator, NoiseOscillator, SubOscillator
from .filter import VoiceFilter

# Default template path (relative to this file)
_DEFAULT_TEMPLATE = Path(__file__).parent.parent / "presets" / "off.json"


@dataclass
class SerumPreset:
    """
    Main Serum preset class.
    
    Provides a Pythonic interface to Serum preset JSON files.
    """
    
    # Metadata
    presetName: str = ""
    presetAuthor: str = ""
    presetDescription: str = ""
    
    # Oscillators
    Oscillator0: Oscillator = field(default_factory=lambda: Oscillator(index=0))
    Oscillator1: Oscillator = field(default_factory=lambda: Oscillator(index=1))
    Oscillator2: Oscillator = field(default_factory=lambda: Oscillator(index=2))
    Oscillator3: NoiseOscillator = field(default_factory=NoiseOscillator)
    Oscillator4: SubOscillator = field(default_factory=SubOscillator)
    
    # Filters
    VoiceFilter0: VoiceFilter = field(default_factory=lambda: VoiceFilter(index=0))
    VoiceFilter1: VoiceFilter = field(default_factory=lambda: VoiceFilter(index=1))
    
    # Store the raw data for fields we don't handle yet
    _raw_data: dict[str, Any] = field(default_factory=dict, repr=False)
    
    @classmethod
    def new(cls, template_path: Optional[str | Path] = None) -> "SerumPreset":
        """
        Create a new preset from a template.
        
        Uses off.json as the default template to ensure all required
        fields are present for a valid Serum preset.
        
        Args:
            template_path: Optional path to a custom template JSON file.
                          If None, uses the default off.json template.
        
        Returns:
            A new SerumPreset with all required fields initialized.
        """
        if template_path is None:
            template_path = _DEFAULT_TEMPLATE
        
        preset = cls.load(template_path)
        # Reset metadata for a new preset
        preset.presetName = ""
        preset.presetAuthor = ""
        preset.presetDescription = ""
        return preset
    
    @classmethod
    def load(cls, path: str | Path) -> "SerumPreset":
        """Load a preset from a JSON file."""
        path = Path(path)
        with open(path, "r") as f:
            raw = json.load(f)
        return cls.from_dict(raw)
    
    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "SerumPreset":
        """Create a preset from a raw JSON dictionary."""
        data = raw.get("data", {})
        metadata = raw.get("metadata", {})
        
        return cls(
            presetName=metadata.get("presetName", data.get("presetName", "")),
            presetAuthor=metadata.get("presetAuthor", data.get("presetAuthor", "")),
            presetDescription=metadata.get("presetDescription", data.get("presetDescription", "")),
            
            # Oscillators
            Oscillator0=Oscillator.from_dict(0, data.get("Oscillator0", {})),
            Oscillator1=Oscillator.from_dict(1, data.get("Oscillator1", {})),
            Oscillator2=Oscillator.from_dict(2, data.get("Oscillator2", {})),
            Oscillator3=NoiseOscillator.from_dict(data.get("Oscillator3", {})),
            Oscillator4=SubOscillator.from_dict(data.get("Oscillator4", {})),
            
            # Filters
            VoiceFilter0=VoiceFilter.from_dict(0, data.get("VoiceFilter0", {})),
            VoiceFilter1=VoiceFilter.from_dict(1, data.get("VoiceFilter1", {})),
            
            _raw_data=raw,
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to a JSON-compatible dictionary."""
        # Start with raw data to preserve unhandled fields
        result = dict(self._raw_data) if self._raw_data else {}
        
        # Ensure structure exists
        if "data" not in result:
            result["data"] = {}
        if "metadata" not in result:
            result["metadata"] = {}
        
        # Update metadata
        result["metadata"]["presetName"] = self.presetName
        result["metadata"]["presetAuthor"] = self.presetAuthor
        result["metadata"]["presetDescription"] = self.presetDescription
        
        # Also update data section (Serum stores it in both places)
        result["data"]["presetName"] = self.presetName
        result["data"]["presetAuthor"] = self.presetAuthor
        result["data"]["presetDescription"] = self.presetDescription
        
        # Update oscillators
        result["data"]["Oscillator0"] = self.Oscillator0.to_dict()
        result["data"]["Oscillator1"] = self.Oscillator1.to_dict()
        result["data"]["Oscillator2"] = self.Oscillator2.to_dict()
        result["data"]["Oscillator3"] = self.Oscillator3.to_dict()
        result["data"]["Oscillator4"] = self.Oscillator4.to_dict()
        
        # Update filters
        result["data"]["VoiceFilter0"] = self.VoiceFilter0.to_dict()
        result["data"]["VoiceFilter1"] = self.VoiceFilter1.to_dict()
        
        return result
    
    def save(self, path: str | Path) -> None:
        """Save the preset to a JSON file."""
        path = Path(path)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def __repr__(self) -> str:
        return (
            f"SerumPreset(presetName={self.presetName!r}, "
            f"Oscillator0={self.Oscillator0.enabled}, "
            f"Oscillator1={self.Oscillator1.enabled}, "
            f"Oscillator2={self.Oscillator2.enabled}, "
            f"Oscillator3={self.Oscillator3.kParamEnable == 1.0}, "
            f"Oscillator4={self.Oscillator4.kParamEnable == 1.0}, "
            f"VoiceFilter0={self.VoiceFilter0.kParamEnable == 1.0}, "
            f"VoiceFilter1={self.VoiceFilter1.kParamEnable == 1.0})"
        )
