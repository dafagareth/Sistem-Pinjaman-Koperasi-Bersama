"""
Repositories package untuk data access layer
"""
from .pinjaman_repository import PinjamanRepositoryInterface, PinjamanFileRepository

__all__ = ['PinjamanRepositoryInterface', 'PinjamanFileRepository']
