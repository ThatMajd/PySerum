"""
Modulation matrix for PySerum.

Manages the ModSlot array (0-63) for automation routing.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from .mod_source import ModSource
from .parameter import SerumParameter

if TYPE_CHECKING:
    from .module import SerumModule


@dataclass
class ModSlot:
    """
    A single modulation slot.
    
    Represents one routing in the mod matrix:
    Source -> Destination Parameter with Amount and settings.
    """
    
    index: int
    source: list[int] = field(default_factory=lambda: [0, 0])
    dest_module_type: str = ""
    dest_module_id: int = 0
    dest_param_name: str = ""
    dest_param_id: int = 0
    amount: float = 0.0
    bipolar: bool = False
    
    def is_active(self) -> bool:
        """Check if this slot has an active modulation."""
        return self.source != [0, 0] and self.dest_module_type != ""
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible dictionary."""
        if not self.is_active():
            return {"plainParams": "default"}
        
        result: dict[str, Any] = {
            "source": self.source,
            "destModuleTypeString": self.dest_module_type,
            "destModuleID": self.dest_module_id,
            "destModuleParamName": self.dest_param_name,
            "destModuleParamID": self.dest_param_id,
        }
        
        params: dict[str, Any] = {}
        if self.amount != 0.0:
            params["kParamAmount"] = self.amount
        if self.bipolar:
            params["kParamBipolar"] = 1.0
        
        result["plainParams"] = params if params else "default"
        return result
    
    @classmethod
    def from_dict(cls, index: int, data: dict[str, Any]) -> ModSlot:
        """Create from JSON dictionary."""
        plain = data.get("plainParams", {})
        if plain == "default":
            plain = {}
        
        return cls(
            index=index,
            source=data.get("source", [0, 0]),
            dest_module_type=data.get("destModuleTypeString", ""),
            dest_module_id=data.get("destModuleID", 0),
            dest_param_name=data.get("destModuleParamName", ""),
            dest_param_id=data.get("destModuleParamID", 0),
            amount=plain.get("kParamAmount", 0.0),
            bipolar=plain.get("kParamBipolar", 0.0) == 1.0,
        )


class ModMatrix:
    """
    Modulation matrix manager.
    
    Provides high-level API for adding modulations and manages
    the underlying ModSlot array.
    """
    
    MAX_SLOTS = 64
    
    def __init__(self):
        self.slots: list[ModSlot] = [ModSlot(i) for i in range(self.MAX_SLOTS)]
    
    def add(
        self,
        source: ModSource,
        dest: SerumParameter,
        amount: float = 50.0,
        bipolar: bool = False,
    ) -> ModSlot:
        """
        Add a modulation routing.
        
        Args:
            source: The modulation source (LFO, Envelope, Macro, etc.)
            dest: The destination parameter (must be a SerumParameter)
            amount: Modulation amount (0-100, or -100 to 100 if bipolar)
            bipolar: Whether modulation is bipolar
        
        Returns:
            The ModSlot that was created.
        
        Raises:
            ValueError: If no free slots are available or dest is invalid.
        """
        # Find the first free slot
        slot = self._find_free_slot()
        if slot is None:
            raise ValueError("No free modulation slots available (max 64)")
        
        # Validate destination
        if not isinstance(dest, SerumParameter):
            raise TypeError(
                f"dest must be a SerumParameter, got {type(dest).__name__}. "
                "Use syntax like: preset.Oscillator0.level"
            )
        
        if dest.parent is None:
            raise ValueError("Parameter has no parent module")
        
        # Extract destination info from the parameter
        parent = dest.parent
        
        slot.source = source.source_id
        slot.dest_module_type = parent.MODULE_TYPE
        slot.dest_module_id = parent.index
        slot.dest_param_name = dest.json_name
        slot.dest_param_id = dest.param_id
        slot.amount = amount
        slot.bipolar = bipolar
        
        return slot
    
    def _find_free_slot(self) -> ModSlot | None:
        """Find the first inactive slot."""
        for slot in self.slots:
            if not slot.is_active():
                return slot
        return None
    
    def clear(self) -> None:
        """Clear all modulation slots."""
        self.slots = [ModSlot(i) for i in range(self.MAX_SLOTS)]
    
    def to_dict(self) -> dict[str, dict[str, Any]]:
        """Convert all slots to JSON-compatible dictionary."""
        return {f"ModSlot{i}": slot.to_dict() for i, slot in enumerate(self.slots)}
    
    def load_from_data(self, data: dict[str, Any]) -> None:
        """Load slots from preset data dictionary."""
        for i in range(self.MAX_SLOTS):
            key = f"ModSlot{i}"
            if key in data:
                self.slots[i] = ModSlot.from_dict(i, data[key])
