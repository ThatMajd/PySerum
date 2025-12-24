"""
Oscillator modules for Serum DSL.

Serum has 5 oscillators:
- Oscillator 0, 1, 2: Regular wavetable oscillators (identical type)
- Oscillator 3: Noise oscillator
- Oscillator 4: Sub oscillator
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WTOsc:
    """Wavetable oscillator parameters (WTOsc0/1/2)."""
    
    # Wavetable path
    relativePathToWT: str = "S2 Tables/Default Shapes.wav"
    
    # Wave parameters
    kParamTablePos: float = 0.0
    kParamInitialPhase: float = 0.0
    kParamRandomPhase: float = 0.0
    
    # Warp parameters
    kParamWarp: float = 0.0
    kParamWarpMenu: str = "kNone"  # String param - handled later
    kParamWarp2: float = 0.0
    kParamWarpMenu2: str = "kNone"  # String param - handled later
    kParamWarpVar2: float = 0.0
    
    # Sample info (read-only from file)
    numChannels: int = 1
    numFrames: int = 18432
    sampleRate: int = 44100
    
    def to_dict(self, index: int) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        result = {
            "relativePathToWT": self.relativePathToWT,
            "numChannels": self.numChannels,
            "numFrames": self.numFrames,
            "sampleRate": self.sampleRate,
            "flex": {},
            "plainParams": {}
        }
        
        # Only add non-default values to plainParams
        params = {}
        if self.kParamTablePos != 0.0:
            params["kParamTablePos"] = self.kParamTablePos
        if self.kParamInitialPhase != 0.0:
            params["kParamInitialPhase"] = self.kParamInitialPhase
        if self.kParamRandomPhase != 0.0:
            params["kParamRandomPhase"] = self.kParamRandomPhase
        if self.kParamWarp != 0.0:
            params["kParamWarp"] = self.kParamWarp
        if self.kParamWarpMenu != "kNone":
            params["kParamWarpMenu"] = self.kParamWarpMenu
        if self.kParamWarp2 != 0.0:
            params["kParamWarp2"] = self.kParamWarp2
        if self.kParamWarpMenu2 != "kNone":
            params["kParamWarpMenu2"] = self.kParamWarpMenu2
        if self.kParamWarpVar2 != 0.0:
            params["kParamWarpVar2"] = self.kParamWarpVar2
            
        result["plainParams"] = params if params else "default"
        return result
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WTOsc":
        """Create from JSON dictionary."""
        plain = data.get("plainParams", {})
        if plain == "default":
            plain = {}
            
        return cls(
            relativePathToWT=data.get("relativePathToWT", "S2 Tables/Default Shapes.wav"),
            kParamTablePos=plain.get("kParamTablePos", 0.0),
            kParamInitialPhase=plain.get("kParamInitialPhase", 0.0),
            kParamRandomPhase=plain.get("kParamRandomPhase", 0.0),
            kParamWarp=plain.get("kParamWarp", 0.0),
            kParamWarpMenu=plain.get("kParamWarpMenu", "kNone"),
            kParamWarp2=plain.get("kParamWarp2", 0.0),
            kParamWarpMenu2=plain.get("kParamWarpMenu2", "kNone"),
            kParamWarpVar2=plain.get("kParamWarpVar2", 0.0),
            numChannels=data.get("numChannels", 1),
            numFrames=data.get("numFrames", 18432),
            sampleRate=data.get("sampleRate", 44100),
        )


@dataclass
class Oscillator:
    """
    Regular oscillator (Oscillator 0, 1, or 2).
    
    These are wavetable oscillators with multiple modes:
    WTOsc, GranularOsc, SampleOsc, SpectralOsc, MultiSampleOsc
    """
    
    index: int  # 0, 1, or 2
    
    # Common oscillator parameters (plainParams)
    kParamEnable: float = 0.0  # 1.0 = enabled, 0.0 = disabled
    kParamVolume: float = 0.0
    kParamPan: float = 0.0
    kParamDetune: float = 0.0
    kParamDetuneWid: float = 0.0
    kParamUnison: float = 1.0
    kParamCoarsePit: float = 0.0
    kParamFine: float = 0.0
    kParamOctave: float = 0.0
    kParamPitch: float = 0.0
    
    # Wavetable oscillator params (primary mode)
    WTOsc: WTOsc = field(default_factory=WTOsc)
    
    def __post_init__(self):
        if self.index not in (0, 1, 2):
            raise ValueError(f"Regular oscillator index must be 0, 1, or 2, got {self.index}")
    
    @property
    def enabled(self) -> bool:
        """Check if oscillator is enabled."""
        return self.kParamEnable == 1.0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        result = {
            f"GranularOsc{self.index}": {"plainParams": "default"},
            f"MultiSampleOsc{self.index}": {"plainParams": "default"},
            f"SampleOsc{self.index}": {"plainParams": "default"},
            f"SpectralOsc{self.index}": {"plainParams": "default"},
            f"WTOsc{self.index}": self.WTOsc.to_dict(self.index),
        }
        
        # Build plainParams
        params = {}
        if self.kParamEnable != 0.0:
            params["kParamEnable"] = self.kParamEnable
        if self.kParamVolume != 0.0:
            params["kParamVolume"] = self.kParamVolume
        if self.kParamPan != 0.0:
            params["kParamPan"] = self.kParamPan
        if self.kParamDetune != 0.0:
            params["kParamDetune"] = self.kParamDetune
        if self.kParamDetuneWid != 0.0:
            params["kParamDetuneWid"] = self.kParamDetuneWid
        if self.kParamUnison != 1.0:
            params["kParamUnison"] = self.kParamUnison
        if self.kParamCoarsePit != 0.0:
            params["kParamCoarsePit"] = self.kParamCoarsePit
        if self.kParamFine != 0.0:
            params["kParamFine"] = self.kParamFine
        if self.kParamOctave != 0.0:
            params["kParamOctave"] = self.kParamOctave
        if self.kParamPitch != 0.0:
            params["kParamPitch"] = self.kParamPitch
            
        result["plainParams"] = params if params else "default"
        return result
    
    @classmethod
    def from_dict(cls, index: int, data: dict[str, Any]) -> "Oscillator":
        """Create from JSON dictionary."""
        plain = data.get("plainParams", {})
        if plain == "default":
            plain = {}
        
        wt_data = data.get(f"WTOsc{index}", {})
        
        return cls(
            index=index,
            kParamEnable=plain.get("kParamEnable", 0.0),
            kParamVolume=plain.get("kParamVolume", 0.0),
            kParamPan=plain.get("kParamPan", 0.0),
            kParamDetune=plain.get("kParamDetune", 0.0),
            kParamDetuneWid=plain.get("kParamDetuneWid", 0.0),
            kParamUnison=plain.get("kParamUnison", 1.0),
            kParamCoarsePit=plain.get("kParamCoarsePit", 0.0),
            kParamFine=plain.get("kParamFine", 0.0),
            kParamOctave=plain.get("kParamOctave", 0.0),
            kParamPitch=plain.get("kParamPitch", 0.0),
            WTOsc=WTOsc.from_dict(wt_data) if wt_data else WTOsc(),
        )


@dataclass
class NoiseOsc:
    """Noise oscillator internal parameters (NoiseOsc3)."""
    
    # Sample path
    relativePathToNoiseSample: str = ""
    
    # Parameters
    kParamColor: float = 0.0
    kParamFine: float = 0.0
    kParamInitialPhase: float = 0.0
    kParamRandomPhase: float = 0.0
    kParamOneShot: float = 0.0
    
    # Sample info
    detuneFactor: float = 1.0
    numChannels: int = 1
    numFrames: int = 0
    sampleRate: int = 44100
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        result = {
            "detuneFactor": self.detuneFactor,
            "numChannels": self.numChannels,
            "numFrames": self.numFrames,
            "sampleRate": self.sampleRate,
        }
        
        if self.relativePathToNoiseSample:
            result["relativePathToNoiseSample"] = self.relativePathToNoiseSample
        
        params = {}
        if self.kParamColor != 0.0:
            params["kParamColor"] = self.kParamColor
        if self.kParamFine != 0.0:
            params["kParamFine"] = self.kParamFine
        if self.kParamInitialPhase != 0.0:
            params["kParamInitialPhase"] = self.kParamInitialPhase
        if self.kParamRandomPhase != 0.0:
            params["kParamRandomPhase"] = self.kParamRandomPhase
        if self.kParamOneShot != 0.0:
            params["kParamOneShot"] = self.kParamOneShot
            
        result["plainParams"] = params if params else "default"
        return result
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NoiseOsc":
        """Create from JSON dictionary."""
        plain = data.get("plainParams", {})
        if plain == "default":
            plain = {}
            
        return cls(
            relativePathToNoiseSample=data.get("relativePathToNoiseSample", ""),
            kParamColor=plain.get("kParamColor", 0.0),
            kParamFine=plain.get("kParamFine", 0.0),
            kParamInitialPhase=plain.get("kParamInitialPhase", 0.0),
            kParamRandomPhase=plain.get("kParamRandomPhase", 0.0),
            kParamOneShot=plain.get("kParamOneShot", 0.0),
            detuneFactor=data.get("detuneFactor", 1.0),
            numChannels=data.get("numChannels", 1),
            numFrames=data.get("numFrames", 0),
            sampleRate=data.get("sampleRate", 44100),
        )


@dataclass
class NoiseOscillator:
    """
    Noise oscillator (Oscillator 3).
    
    Different from regular oscillators - uses noise samples instead of wavetables.
    """
    
    # Common oscillator parameters
    kParamEnable: float = 0.0
    kParamVolume: float = 0.0
    kParamPan: float = 0.0
    
    # Noise-specific params
    NoiseOsc3: NoiseOsc = field(default_factory=NoiseOsc)
    
    @property
    def index(self) -> int:
        return 3
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        result = {
            "NoiseOsc3": self.NoiseOsc3.to_dict(),
        }
        
        params = {}
        if self.kParamEnable != 0.0:
            params["kParamEnable"] = self.kParamEnable
        if self.kParamVolume != 0.0:
            params["kParamVolume"] = self.kParamVolume
        if self.kParamPan != 0.0:
            params["kParamPan"] = self.kParamPan
            
        result["plainParams"] = params if params else "default"
        return result
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NoiseOscillator":
        """Create from JSON dictionary."""
        plain = data.get("plainParams", {})
        if plain == "default":
            plain = {}
        
        noise_data = data.get("NoiseOsc3", {})
        
        return cls(
            kParamEnable=plain.get("kParamEnable", 0.0),
            kParamVolume=plain.get("kParamVolume", 0.0),
            kParamPan=plain.get("kParamPan", 0.0),
            NoiseOsc3=NoiseOsc.from_dict(noise_data) if noise_data else NoiseOsc(),
        )


@dataclass
class SubOsc:
    """Sub oscillator internal parameters (SubOsc4)."""
    
    kParamShape: str = "kSine"  # String param - handled later
    kParamInitialPhase: float = 0.0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        params = {}
        if self.kParamShape != "kSine":
            params["kParamShape"] = self.kParamShape
        if self.kParamInitialPhase != 0.0:
            params["kParamInitialPhase"] = self.kParamInitialPhase
            
        return {"plainParams": params if params else "default"}
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SubOsc":
        """Create from JSON dictionary."""
        plain = data.get("plainParams", {})
        if plain == "default":
            plain = {}
            
        return cls(
            kParamShape=plain.get("kParamShape", "kSine"),
            kParamInitialPhase=plain.get("kParamInitialPhase", 0.0),
        )


@dataclass
class SubOscillator:
    """
    Sub oscillator (Oscillator 4).
    
    Different from regular oscillators - simple waveform generator
    with octave control, meant for bass reinforcement.
    """
    
    # Common oscillator parameters
    kParamEnable: float = 0.0
    kParamVolume: float = 0.0
    kParamPan: float = 0.0
    kParamCoarsePit: float = 0.0
    kParamOctave: float = 0.0
    
    # Sub oscillator params
    SubOsc4: SubOsc = field(default_factory=SubOsc)
    
    @property
    def index(self) -> int:
        return 4
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        result = {
            "SubOsc4": self.SubOsc4.to_dict(),
        }
        
        params = {}
        if self.kParamEnable != 0.0:
            params["kParamEnable"] = self.kParamEnable
        if self.kParamVolume != 0.0:
            params["kParamVolume"] = self.kParamVolume
        if self.kParamPan != 0.0:
            params["kParamPan"] = self.kParamPan
        if self.kParamCoarsePit != 0.0:
            params["kParamCoarsePit"] = self.kParamCoarsePit
        if self.kParamOctave != 0.0:
            params["kParamOctave"] = self.kParamOctave
            
        result["plainParams"] = params if params else "default"
        return result
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SubOscillator":
        """Create from JSON dictionary."""
        plain = data.get("plainParams", {})
        if plain == "default":
            plain = {}
        
        sub_data = data.get("SubOsc4", {})
        
        return cls(
            kParamEnable=plain.get("kParamEnable", 0.0),
            kParamVolume=plain.get("kParamVolume", 0.0),
            kParamPan=plain.get("kParamPan", 0.0),
            kParamCoarsePit=plain.get("kParamCoarsePit", 0.0),
            kParamOctave=plain.get("kParamOctave", 0.0),
            SubOsc4=SubOsc.from_dict(sub_data) if sub_data else SubOsc(),
        )
