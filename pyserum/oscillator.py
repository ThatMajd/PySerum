"""
Oscillator modules for PySerum.

Serum has 5 oscillators:
- Oscillator 0, 1, 2: Regular wavetable oscillators
- Oscillator 3: Noise oscillator  
- Oscillator 4: Sub oscillator
"""

from __future__ import annotations
from typing import Any

from .module import SerumModule
from .parameter import ParameterDescriptor, StringParameterDescriptor


class WTOsc(SerumModule):
    """
    Wavetable oscillator internal parameters (WTOsc0/1/2).
    
    These are the wavetable-specific parameters like position and warp.
    """
    
    MODULE_TYPE = "WTOsc"
    
    # Parameters from notes.md - WTOsc section
    # ID 0: Warp 1
    warp = ParameterDescriptor("warp", param_id=0, json_name="kParamWarp", default=0.0)
    # ID 3: Warp 2
    warp2 = ParameterDescriptor("warp2", param_id=3, json_name="kParamWarp2", default=0.0)
    # ID 6: WT Position
    wt_pos = ParameterDescriptor("wt_pos", param_id=6, json_name="kParamTablePos", default=0.0)
    # ID 8: Initial Phase
    phase = ParameterDescriptor("phase", param_id=8, json_name="kParamInitialPhase", default=0.0)
    # ID 9: Random Phase
    rand_phase = ParameterDescriptor("rand_phase", param_id=9, json_name="kParamRandomPhase", default=0.0)
    
    # String parameters (not automatable)
    warp_mode = StringParameterDescriptor("kParamWarpMenu", default="kNone")
    warp2_mode = StringParameterDescriptor("kParamWarpMenu2", default="kNone")
    
    def __init__(self, index: int = 0):
        super().__init__(index)
        # Wavetable file info
        self.wavetable_path = "S2 Tables/Default Shapes.wav"
        self.num_channels = 1
        self.num_frames = 18432
        self.sample_rate = 44100
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        return {
            "relativePathToWT": self.wavetable_path,
            "numChannels": self.num_channels,
            "numFrames": self.num_frames,
            "sampleRate": self.sample_rate,
            "flex": {},
            "plainParams": self.to_plain_params(),
        }
    
    @classmethod
    def from_dict(cls, index: int, data: dict[str, Any]) -> WTOsc:
        """Create from JSON dictionary."""
        instance = cls(index)
        instance.wavetable_path = data.get("relativePathToWT", "S2 Tables/Default Shapes.wav")
        instance.num_channels = data.get("numChannels", 1)
        instance.num_frames = data.get("numFrames", 18432)
        instance.sample_rate = data.get("sampleRate", 44100)
        
        plain = data.get("plainParams", {})
        instance.load_plain_params(plain)
        
        return instance


class Oscillator(SerumModule):
    """
    Regular oscillator (Oscillator 0, 1, or 2).
    
    These are wavetable oscillators with the familiar Serum controls.
    Uses user-friendly names from notes.md Serum UI column.
    """
    
    MODULE_TYPE = "Oscillator"
    
    # Enable (not automatable, but we track it)
    enable = ParameterDescriptor("enable", param_id=0, json_name="kParamEnable", default=0.0)
    
    # Parameters from notes.md - Oscillator section
    # ID 1: Level
    level = ParameterDescriptor("level", param_id=1, json_name="kParamVolume", default=0.0)
    # ID 2: Pan
    pan = ParameterDescriptor("pan", param_id=2, json_name="kParamPan", default=0.0)
    # ID 3: Octave
    octave = ParameterDescriptor("octave", param_id=3, json_name="kParamOctave", default=0.0)
    # ID 4: Pitch (semitones)
    pitch = ParameterDescriptor("pitch", param_id=4, json_name="kParamPitch", default=0.0)
    # ID 5: Fine
    fine = ParameterDescriptor("fine", param_id=5, json_name="kParamFine", default=0.0)
    # ID 6: Coarse Pitch
    coarse = ParameterDescriptor("coarse", param_id=6, json_name="kParamCoarsePit", default=0.0)
    # ID 26: Detune
    detune = ParameterDescriptor("detune", param_id=26, json_name="kParamDetune", default=0.0)
    # ID 27: Detune Width
    detune_width = ParameterDescriptor("detune_width", param_id=27, json_name="kParamDetuneWid", default=0.0)
    # Unison (not in notes.md but exists)
    unison = ParameterDescriptor("unison", param_id=28, json_name="kParamUnison", default=1.0)
    
    def __init__(self, index: int = 0):
        if index not in (0, 1, 2):
            raise ValueError(f"Regular oscillator index must be 0, 1, or 2, got {index}")
        super().__init__(index)
        self.wt_osc = WTOsc(index)
    
    @property
    def enabled(self) -> bool:
        """Check if oscillator is enabled."""
        return self.enable.value == 1.0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        idx = self.index
        return {
            f"GranularOsc{idx}": {"plainParams": "default"},
            f"MultiSampleOsc{idx}": {"plainParams": "default"},
            f"SampleOsc{idx}": {"plainParams": "default"},
            f"SpectralOsc{idx}": {"plainParams": "default"},
            f"WTOsc{idx}": self.wt_osc.to_dict(),
            "plainParams": self.to_plain_params(),
        }
    
    @classmethod
    def from_dict(cls, index: int, data: dict[str, Any]) -> Oscillator:
        """Create from JSON dictionary."""
        instance = cls(index)
        
        # Load main oscillator params
        plain = data.get("plainParams", {})
        instance.load_plain_params(plain)
        
        # Load WTOsc params
        wt_data = data.get(f"WTOsc{index}", {})
        if wt_data:
            instance.wt_osc = WTOsc.from_dict(index, wt_data)
        
        return instance


class NoiseOsc(SerumModule):
    """
    Noise oscillator internal parameters (NoiseOsc3).
    """
    
    MODULE_TYPE = "NoiseOsc"
    
    # Parameters from notes.md - NoiseOsc section
    # ID 0: Pitch (Color)
    pitch = ParameterDescriptor("pitch", param_id=0, json_name="kParamColor", default=0.0)
    # ID 1: Fine
    fine = ParameterDescriptor("fine", param_id=1, json_name="kParamFine", default=0.0)
    # ID 2: Start (Initial Phase)
    start = ParameterDescriptor("start", param_id=2, json_name="kParamInitialPhase", default=0.0)
    # ID 3: Random Phase
    rand = ParameterDescriptor("rand", param_id=3, json_name="kParamRandomPhase", default=0.0)
    
    def __init__(self, index: int = 3):
        super().__init__(index)
        self.sample_path = ""
        self.detune_factor = 1.0
        self.num_channels = 1
        self.num_frames = 0
        self.sample_rate = 44100
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        result = {
            "detuneFactor": self.detune_factor,
            "numChannels": self.num_channels,
            "numFrames": self.num_frames,
            "sampleRate": self.sample_rate,
            "plainParams": self.to_plain_params(),
        }
        if self.sample_path:
            result["relativePathToNoiseSample"] = self.sample_path
        return result
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> NoiseOsc:
        """Create from JSON dictionary."""
        instance = cls()
        instance.sample_path = data.get("relativePathToNoiseSample", "")
        instance.detune_factor = data.get("detuneFactor", 1.0)
        instance.num_channels = data.get("numChannels", 1)
        instance.num_frames = data.get("numFrames", 0)
        instance.sample_rate = data.get("sampleRate", 44100)
        
        plain = data.get("plainParams", {})
        instance.load_plain_params(plain)
        
        return instance


class NoiseOscillator(SerumModule):
    """
    Noise oscillator (Oscillator 3).
    
    Different from regular oscillators - uses noise samples instead of wavetables.
    """
    
    MODULE_TYPE = "Oscillator"  # For automation routing
    
    # Enable
    enable = ParameterDescriptor("enable", param_id=0, json_name="kParamEnable", default=0.0)
    
    # Parameters from notes.md - Oscillator section (noise variant)
    # ID 1: Level
    level = ParameterDescriptor("level", param_id=1, json_name="kParamVolume", default=0.0)
    # ID 2: Pan
    pan = ParameterDescriptor("pan", param_id=2, json_name="kParamPan", default=0.0)
    
    def __init__(self):
        super().__init__(index=3)
        self.noise_osc = NoiseOsc()
    
    @property
    def enabled(self) -> bool:
        return self.enable.value == 1.0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        return {
            "NoiseOsc3": self.noise_osc.to_dict(),
            "plainParams": self.to_plain_params(),
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> NoiseOscillator:
        """Create from JSON dictionary."""
        instance = cls()
        
        plain = data.get("plainParams", {})
        instance.load_plain_params(plain)
        
        noise_data = data.get("NoiseOsc3", {})
        if noise_data:
            instance.noise_osc = NoiseOsc.from_dict(noise_data)
        
        return instance


class SubOsc(SerumModule):
    """
    Sub oscillator internal parameters (SubOsc4).
    """
    
    MODULE_TYPE = "SubOsc"
    
    # Parameters from notes.md - SubOsc section
    # ID 2: Initial Phase
    phase = ParameterDescriptor("phase", param_id=2, json_name="kParamInitialPhase", default=0.0)
    
    # String parameters
    shape = StringParameterDescriptor("kParamShape", default="kSine")
    
    def __init__(self, index: int = 4):
        super().__init__(index)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        return {"plainParams": self.to_plain_params()}
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SubOsc:
        """Create from JSON dictionary."""
        instance = cls()
        plain = data.get("plainParams", {})
        instance.load_plain_params(plain)
        return instance


class SubOscillator(SerumModule):
    """
    Sub oscillator (Oscillator 4).
    
    Simple waveform generator with octave control for bass reinforcement.
    """
    
    MODULE_TYPE = "Oscillator"  # For automation routing
    
    # Enable
    enable = ParameterDescriptor("enable", param_id=0, json_name="kParamEnable", default=0.0)
    
    # Parameters from notes.md - Oscillator section (sub variant)
    # ID 1: Level
    level = ParameterDescriptor("level", param_id=1, json_name="kParamVolume", default=0.0)
    # ID 2: Pan
    pan = ParameterDescriptor("pan", param_id=2, json_name="kParamPan", default=0.0)
    # ID 3: Octave
    octave = ParameterDescriptor("octave", param_id=3, json_name="kParamOctave", default=0.0)
    # ID 6: Coarse
    coarse = ParameterDescriptor("coarse", param_id=6, json_name="kParamCoarsePit", default=0.0)
    
    def __init__(self):
        super().__init__(index=4)
        self.sub_osc = SubOsc()
    
    @property
    def enabled(self) -> bool:
        return self.enable.value == 1.0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        return {
            "SubOsc4": self.sub_osc.to_dict(),
            "plainParams": self.to_plain_params(),
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SubOscillator:
        """Create from JSON dictionary."""
        instance = cls()
        
        plain = data.get("plainParams", {})
        instance.load_plain_params(plain)
        
        sub_data = data.get("SubOsc4", {})
        if sub_data:
            instance.sub_osc = SubOsc.from_dict(sub_data)
        
        return instance
