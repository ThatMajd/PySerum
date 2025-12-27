"""
Core parameter system for PySerum.

This module provides the SerumParameter descriptor that allows parameters
to be accessed as simple values while carrying metadata (ID, JSON name) 
for automation and serialization.
"""

from __future__ import annotations
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .module import SerumModule


class SerumParameter:
    """
    A smart parameter that carries metadata for automation.
    
    This object holds:
    - The current value
    - The parameter ID (for automation)
    - The JSON key name (for serialization)
    - A reference to its parent module
    
    It also supports basic arithmetic operations so it can be used
    somewhat like a float in expressions.
    """
    
    def __init__(
        self,
        name: str,
        param_id: int,
        json_name: str,
        value: float,
        default: float,
        parent: SerumModule | None = None,
    ):
        self.name = name
        self.param_id = param_id
        self.json_name = json_name
        self._value = value
        self.default = default
        self.parent = parent
    
    @property
    def value(self) -> float:
        return self._value
    
    @value.setter
    def value(self, val: float) -> None:
        self._value = float(val)
    
    def __repr__(self) -> str:
        return f"SerumParameter({self.name}={self._value}, id={self.param_id})"
    
    def __str__(self) -> str:
        return str(self._value)
    
    # Arithmetic operations - allow using the parameter in expressions
    def __float__(self) -> float:
        return self._value
    
    def __int__(self) -> int:
        return int(self._value)
    
    def __add__(self, other: float) -> float:
        return self._value + float(other)
    
    def __radd__(self, other: float) -> float:
        return float(other) + self._value
    
    def __sub__(self, other: float) -> float:
        return self._value - float(other)
    
    def __rsub__(self, other: float) -> float:
        return float(other) - self._value
    
    def __mul__(self, other: float) -> float:
        return self._value * float(other)
    
    def __rmul__(self, other: float) -> float:
        return float(other) * self._value
    
    def __truediv__(self, other: float) -> float:
        return self._value / float(other)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, SerumParameter):
            return self._value == other._value
        return self._value == other
    
    def __lt__(self, other: float) -> bool:
        return self._value < float(other)
    
    def __le__(self, other: float) -> bool:
        return self._value <= float(other)
    
    def __gt__(self, other: float) -> bool:
        return self._value > float(other)
    
    def __ge__(self, other: float) -> bool:
        return self._value >= float(other)


class ParameterDescriptor:
    """
    A descriptor that manages SerumParameter instances on module classes.
    
    When accessed on an instance, returns the SerumParameter object.
    When assigned to, updates the parameter's value rather than replacing it.
    """
    
    def __init__(
        self,
        name: str,
        param_id: int,
        json_name: str,
        default: float = 0.0
    ):
        self.name = name
        self.param_id = param_id
        self.json_name = json_name
        self.default = default
        self._storage_name = f"_param_{name}"
    
    def __set_name__(self, owner: type, name: str) -> None:
        # Called when the descriptor is assigned to a class attribute
        self.name = name
        self._storage_name = f"_param_{name}"
    
    def __get__(self, instance: Any, owner: type) -> SerumParameter | ParameterDescriptor:
        if instance is None:
            # Class-level access, return the descriptor itself
            return self
        
        # Instance-level access, return the SerumParameter object
        if not hasattr(instance, self._storage_name):
            # Create the parameter on first access
            param = SerumParameter(
                name=self.name,
                param_id=self.param_id,
                json_name=self.json_name,
                value=self.default,
                default=self.default,
                parent=instance,
            )
            setattr(instance, self._storage_name, param)
        
        return getattr(instance, self._storage_name)
    
    def __set__(self, instance: Any, value: float | SerumParameter) -> None:
        # Get or create the parameter object
        param = self.__get__(instance, type(instance))
        
        if isinstance(value, SerumParameter):
            # Copying from another parameter
            param.value = value.value
        else:
            # Setting a numeric value
            param.value = float(value)


class StringParameterDescriptor:
    """
    A descriptor for string parameters (like filter type, warp mode).
    
    These don't need the full SerumParameter machinery since they
    can't be automation destinations.
    """
    
    def __init__(self, json_name: str, default: str = ""):
        self.json_name = json_name
        self.default = default
        self._storage_name = ""
    
    def __set_name__(self, owner: type, name: str) -> None:
        self._storage_name = f"_str_{name}"
    
    def __get__(self, instance: Any, owner: type) -> str | StringParameterDescriptor:
        if instance is None:
            return self
        
        if not hasattr(instance, self._storage_name):
            setattr(instance, self._storage_name, self.default)
        
        return getattr(instance, self._storage_name)
    
    def __set__(self, instance: Any, value: str) -> None:
        setattr(instance, self._storage_name, str(value))
