"""
Backward compatibility layer for API changes.
"""

import warnings
from typing import Any, Dict, TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')


class BackwardCompatibleResponse(Generic[T]):
    """Wrapper to provide backward compatibility for API responses."""
    
    def __init__(self, response: T):
        self._response = response
        
    @property
    def success(self) -> bool:
        """Always return True for backward compatibility."""
        warnings.warn(
            "The 'success' field is deprecated and will be removed in a future version. "
            "The API no longer returns this field.",
            DeprecationWarning,
            stacklevel=2
        )
        return True
        
    @property 
    def message(self) -> str:
        """Return empty string for backward compatibility."""
        warnings.warn(
            "The 'message' field is deprecated and will be removed in a future version. "
            "The API no longer returns this field.",
            DeprecationWarning,
            stacklevel=2
        )
        return ""
        
    def __getattr__(self, name: str) -> Any:
        """Delegate all other attributes to the wrapped response."""
        return getattr(self._response, name)
    
    def __repr__(self) -> str:
        return f"BackwardCompatibleResponse({repr(self._response)})"
    
    def __str__(self) -> str:
        return str(self._response)