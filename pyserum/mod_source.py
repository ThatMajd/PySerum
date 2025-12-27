"""
Modulation sources for automation in PySerum.

Defines the ModSource enum that maps friendly names to Serum's internal
source ID format [type_id, index].
"""

from enum import Enum
from typing import List


class ModSource(Enum):
    """
    Modulation sources available in Serum2.
    
    Each value is a tuple of (source_type_id, aux_index).
    Based on the automation sources table in notes.md.
    """
    
    # Note: The format is [type_id, aux_id] as stored in JSON
    
    # Basic controllers
    MOD_WHEEL = [1, 0]
    
    # Envelopes (Env1-4)
    ENV1 = [2, 0]
    ENV2 = [3, 0]
    ENV3 = [4, 0]
    ENV4 = [5, 0]
    
    # LFOs (LFO1-10) - Based on notes.md IDs 6-15
    LFO1 = [6, 0]
    LFO2 = [7, 0]
    LFO3 = [8, 0]
    LFO4 = [9, 0]
    LFO5 = [10, 0]
    LFO6 = [11, 0]
    LFO7 = [12, 0]
    LFO8 = [13, 0]
    LFO9 = [14, 0]
    LFO10 = [15, 0]
    
    # Macros
    # TODO check if these are correct
    MACRO1 = [16, 0]
    MACRO2 = [16, 1]
    MACRO3 = [16, 2]
    MACRO4 = [16, 3]
    MACRO5 = [16, 4]
    MACRO6 = [16, 5]
    MACRO7 = [16, 6]
    MACRO8 = [16, 7]
    
    @property
    def source_id(self) -> List[int]:
        """Get the raw source ID array for JSON serialization."""
        return list(self.value)
