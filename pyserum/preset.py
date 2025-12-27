"""
Main Serum Preset class for PySerum.

Provides the high-level API for creating, loading, and saving presets.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Optional

from .oscillator import Oscillator, NoiseOscillator, SubOscillator
from .filter import VoiceFilter
from .mod_matrix import ModMatrix
from .mod_source import ModSource
from .parameter import SerumParameter

# Default template path (relative to this file)
_DEFAULT_TEMPLATE = Path(__file__).parent.parent / "presets" / "off.json"


class SerumPreset:
    """
    Main Serum preset class.
    
    Provides a Pythonic interface to Serum2 preset JSON files with
    user-friendly parameter names and automation support.
    
    Example:
        >>> preset = SerumPreset.new()
        >>> preset.name = "My Preset"
        >>> preset.Oscillator0.enable = True
        >>> preset.Oscillator0.level = 0.8
        >>> preset.VoiceFilter0.cutoff = 0.5
        >>> preset.add_modulation(ModSource.LFO1, preset.Oscillator0.level, amount=50)
        >>> preset.save("my_preset.json")
    """
    
    def __init__(self):
        # Metadata
        self._name = ""
        self._author = ""
        self._description = ""
        
        # Oscillators
        self.Oscillator0 = Oscillator(index=0)
        self.Oscillator1 = Oscillator(index=1)
        self.Oscillator2 = Oscillator(index=2)
        self.Oscillator3 = NoiseOscillator()
        self.Oscillator4 = SubOscillator()
        
        # Filters
        self.VoiceFilter0 = VoiceFilter(index=0)
        self.VoiceFilter1 = VoiceFilter(index=1)
        
        # Modulation matrix
        self.mod_matrix = ModMatrix()
        
        # Raw data for fields we don't handle yet
        self._raw_data: dict[str, Any] = {}
    
    # Metadata properties with friendly names
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = value
    
    @property
    def author(self) -> str:
        return self._author
    
    @author.setter
    def author(self, value: str) -> None:
        self._author = value
    
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str) -> None:
        self._description = value
    
    def add_modulation(
        self,
        source: ModSource,
        dest: SerumParameter,
        amount: float = 50.0,
        bipolar: bool = False,
    ) -> None:
        """
        Add a modulation routing.
        
        Args:
            source: The modulation source (e.g., ModSource.LFO1)
            dest: The destination parameter (e.g., preset.Oscillator0.level)
            amount: Modulation amount (0-100, or -100 to 100 if bipolar)
            bipolar: Whether modulation is bipolar
        
        Example:
            >>> preset.add_modulation(
            ...     source=ModSource.LFO1,
            ...     dest=preset.Oscillator0.level,
            ...     amount=50.0,
            ...     bipolar=False
            ... )
        """
        self.mod_matrix.add(source, dest, amount, bipolar)
    
    @classmethod
    def new(cls, template_path: Optional[str | Path] = None) -> SerumPreset:
        """
        Create a new preset from a template.
        
        Uses off.json as the default template to ensure all required
        fields are present for a valid Serum preset.
        
        Args:
            template_path: Optional path to a custom template JSON file.
        
        Returns:
            A new SerumPreset with all required fields initialized.
        """
        if template_path is None:
            template_path = _DEFAULT_TEMPLATE
        
        preset = cls.load(template_path)
        # Reset metadata for a new preset
        preset.name = ""
        preset.author = ""
        preset.description = ""
        # Clear modulations
        preset.mod_matrix.clear()
        
        return preset
    
    @classmethod
    def load(cls, path: str | Path) -> SerumPreset:
        """Load a preset from a JSON file."""
        path = Path(path)
        with open(path, "r") as f:
            raw = json.load(f)
        return cls.from_dict(raw)
    
    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> SerumPreset:
        """Create a preset from a raw JSON dictionary."""
        preset = cls()
        preset._raw_data = raw
        
        data = raw.get("data", {})
        metadata = raw.get("metadata", {})
        
        # Load metadata
        preset.name = metadata.get("presetName", data.get("presetName", ""))
        preset.author = metadata.get("presetAuthor", data.get("presetAuthor", ""))
        preset.description = metadata.get("presetDescription", data.get("presetDescription", ""))
        
        # Load oscillators
        preset.Oscillator0 = Oscillator.from_dict(0, data.get("Oscillator0", {}))
        preset.Oscillator1 = Oscillator.from_dict(1, data.get("Oscillator1", {}))
        preset.Oscillator2 = Oscillator.from_dict(2, data.get("Oscillator2", {}))
        preset.Oscillator3 = NoiseOscillator.from_dict(data.get("Oscillator3", {}))
        preset.Oscillator4 = SubOscillator.from_dict(data.get("Oscillator4", {}))
        
        # Load filters
        preset.VoiceFilter0 = VoiceFilter.from_dict(0, data.get("VoiceFilter0", {}))
        preset.VoiceFilter1 = VoiceFilter.from_dict(1, data.get("VoiceFilter1", {}))
        
        # Load modulation matrix
        preset.mod_matrix.load_from_data(data)
        
        return preset
    
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
        result["metadata"]["presetName"] = self.name
        result["metadata"]["presetAuthor"] = self.author
        result["metadata"]["presetDescription"] = self.description
        
        # Also update data section (Serum stores it in both places)
        result["data"]["presetName"] = self.name
        result["data"]["presetAuthor"] = self.author
        result["data"]["presetDescription"] = self.description
        
        # Update oscillators
        result["data"]["Oscillator0"] = self.Oscillator0.to_dict()
        result["data"]["Oscillator1"] = self.Oscillator1.to_dict()
        result["data"]["Oscillator2"] = self.Oscillator2.to_dict()
        result["data"]["Oscillator3"] = self.Oscillator3.to_dict()
        result["data"]["Oscillator4"] = self.Oscillator4.to_dict()
        
        # Update filters
        result["data"]["VoiceFilter0"] = self.VoiceFilter0.to_dict()
        result["data"]["VoiceFilter1"] = self.VoiceFilter1.to_dict()
        
        # Update modulation matrix
        result["data"].update(self.mod_matrix.to_dict())
        
        return result
    
    def save(self, path: str | Path) -> None:
        """Save the preset to a JSON file."""
        path = Path(path)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def __repr__(self) -> str:
        return (
            f"SerumPreset(name={self.name!r}, "
            f"Oscillator0={self.Oscillator0.enabled}, "
            f"Oscillator1={self.Oscillator1.enabled}, "
            f"Oscillator2={self.Oscillator2.enabled}, "
            f"Oscillator3={self.Oscillator3.enabled}, "
            f"Oscillator4={self.Oscillator4.enabled}, "
            f"VoiceFilter0={self.VoiceFilter0.enabled}, "
            f"VoiceFilter1={self.VoiceFilter1.enabled})"
        )
