"""
Base module class for PySerum components.

All Serum modules (Oscillators, Filters, etc.) inherit from SerumModule
to gain automatic parameter registration and serialization.
"""

from __future__ import annotations
from typing import Any, Iterator

from .parameter import ParameterDescriptor, StringParameterDescriptor, SerumParameter


class SerumModule:
    """
    Base class for all Serum modules.
    
    Provides:
    - Automatic parameter discovery via descriptors
    - Serialization to/from JSON dictionaries
    - Parameter ID lookup for automation
    """
    
    # Override in subclasses
    MODULE_TYPE: str = ""  # e.g., "Oscillator", "Filter"
    
    def __init__(self, index: int = 0):
        self._index = index
        # Initialize all parameters by accessing them
        self._init_parameters()
    
    def _init_parameters(self) -> None:
        """Initialize all parameter descriptors."""
        for name in dir(type(self)):
            attr = getattr(type(self), name, None)
            if isinstance(attr, ParameterDescriptor):
                # Access to trigger creation
                getattr(self, name)
    
    @property
    def index(self) -> int:
        return self._index
    
    def _iter_parameters(self) -> Iterator[tuple[str, SerumParameter]]:
        """Iterate over all SerumParameter instances on this module."""
        for name in dir(type(self)):
            attr = getattr(type(self), name, None)
            if isinstance(attr, ParameterDescriptor):
                param = getattr(self, name)
                if isinstance(param, SerumParameter):
                    yield name, param
    
    def _iter_string_params(self) -> Iterator[tuple[str, str, str]]:
        """Iterate over all string parameters (name, json_name, value)."""
        for name in dir(type(self)):
            descriptor = getattr(type(self), name, None)
            if isinstance(descriptor, StringParameterDescriptor):
                value = getattr(self, name)
                yield name, descriptor.json_name, value
    
    def get_param_by_name(self, name: str) -> SerumParameter | None:
        """Get a parameter by its Python attribute name."""
        attr = getattr(type(self), name, None)
        if isinstance(attr, ParameterDescriptor):
            return getattr(self, name)
        return None
    
    def to_plain_params(self) -> dict[str, Any] | str:
        """
        Convert parameters to the plainParams JSON format.
        
        Returns "default" if all values are at their defaults.
        """
        params: dict[str, Any] = {}
        
        # Add numeric parameters
        for name, param in self._iter_parameters():
            if param.value != param.default:
                params[param.json_name] = param.value
        
        # Add string parameters
        for name, json_name, value in self._iter_string_params():
            descriptor = getattr(type(self), name)
            if value != descriptor.default:
                params[json_name] = value
        
        return params if params else "default"
    
    def load_plain_params(self, plain: dict[str, Any] | str) -> None:
        """Load parameters from a plainParams dictionary."""
        if plain == "default" or not plain:
            return
        
        # Load numeric parameters
        for name, param in self._iter_parameters():
            if param.json_name in plain:
                param.value = plain[param.json_name]
        
        # Load string parameters
        for name, json_name, _ in self._iter_string_params():
            if json_name in plain:
                setattr(self, name, plain[json_name])
