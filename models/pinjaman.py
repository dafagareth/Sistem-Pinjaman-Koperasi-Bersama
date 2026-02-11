"""
Model untuk entitas Pinjaman
Menggunakan dataclass untuk immutability dan type safety
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from decimal import Decimal


class JenisPinjaman(Enum):
    """Enum untuk jenis pinjaman"""
    KONSUMTIF = ("A", "Konsumtif", 15)  # (kode, nama, bunga%)
    MODAL = ("B", "Modal", 10)
    
    def __init__(self, kode: str, nama: str, bunga: int):
        self.kode = kode
        self.nama = nama
        self.tingkat_bunga = bunga
    
    @classmethod
    def dari_kode(cls, kode: str) -> 'JenisPinjaman':
        """Factory method untuk membuat JenisPinjaman dari kode"""
        for jenis in cls:
            if jenis.kode == kode.upper():
                return jenis
        raise ValueError(f"Kode pinjaman tidak valid: {kode}")


@dataclass
class Anggota:
    """Model untuk data anggota koperasi"""
    nomor: str
    nama: str
    
    def __post_init__(self):
        """Validasi data anggota"""
        if not self.nomor or len(self.nomor.strip()) == 0:
            raise ValueError("Nomor anggota tidak boleh kosong")
        if not self.nama or len(self.nama.strip()) == 0:
            raise ValueError("Nama anggota tidak boleh kosong")
        
        # Normalize data
        self.nomor = self.nomor.strip()
        self.nama = self.nama.strip()


@dataclass
class Pinjaman:
    """
    Model untuk entitas pinjaman koperasi
    
    Attributes:
        anggota: Data anggota peminjam
        jenis: Jenis pinjaman (Konsumtif/Modal)
        jumlah: Jumlah pinjaman dalam Rupiah
        lama_bulan: Lama pinjaman dalam bulan
    """
    anggota: Anggota
    jenis: JenisPinjaman
    jumlah: Decimal
    lama_bulan: int
    _angsuran: Optional[Decimal] = field(default=None, init=False, repr=False)
    
    def __post_init__(self):
        """Validasi data pinjaman"""
        # Note: jumlah should already be Decimal when object is created
        # Validation is done here, but no mutation of fields
        if self.jumlah <= 0:
            raise ValueError("Jumlah pinjaman harus lebih dari 0")
        if self.lama_bulan <= 0:
            raise ValueError("Lama pinjaman harus lebih dari 0")
    
    @property
    def bunga_per_bulan(self) -> Decimal:
        """Hitung bunga per bulan"""
        tingkat_bunga_desimal = Decimal(str(self.jenis.tingkat_bunga)) / Decimal('100')
        return (tingkat_bunga_desimal / Decimal('12')) * self.jumlah
    
    @property
    def pokok_per_bulan(self) -> Decimal:
        """Hitung pokok per bulan"""
        return self.jumlah / Decimal(str(self.lama_bulan))
    
    @property
    def angsuran(self) -> Decimal:
        """
        Hitung jumlah angsuran per bulan
        Formula: (Bunga/12 × Pinjaman) + (Pinjaman/Lama)
        """
        if self._angsuran is None:
            object.__setattr__(self, '_angsuran', self.bunga_per_bulan + self.pokok_per_bulan)
        return self._angsuran
    
    @property
    def total_bunga(self) -> Decimal:
        """Total bunga yang harus dibayar"""
        return self.bunga_per_bulan * Decimal(str(self.lama_bulan))
    
    @property
    def total_bayar(self) -> Decimal:
        """Total yang harus dibayar (pokok + bunga)"""
        return self.jumlah + self.total_bunga
    
    def to_dict(self) -> dict:
        """Convert pinjaman to dictionary"""
        return {
            'nomor_anggota': self.anggota.nomor,
            'nama_anggota': self.anggota.nama,
            'kode_pinjaman': self.jenis.kode,
            'jenis_pinjaman': self.jenis.nama,
            'tingkat_bunga': self.jenis.tingkat_bunga,
            'jumlah_pinjaman': float(self.jumlah),
            'lama_bulan': self.lama_bulan,
            'angsuran': float(self.angsuran)
        }
    
    @classmethod
    def dari_dict(cls, data: dict) -> 'Pinjaman':
        """Factory method untuk membuat Pinjaman dari dictionary"""
        anggota = Anggota(
            nomor=data['nomor_anggota'],
            nama=data['nama_anggota']
        )
        jenis = JenisPinjaman.dari_kode(data['kode_pinjaman'])
        
        return cls(
            anggota=anggota,
            jenis=jenis,
            jumlah=Decimal(str(data['jumlah_pinjaman'])),
            lama_bulan=int(data['lama_bulan'])
        )
    
    def __str__(self) -> str:
        """String representation untuk debugging"""
        return (f"Pinjaman({self.anggota.nama}, {self.jenis.nama}, "
                f"Rp{self.jumlah:,.0f}, {self.lama_bulan} bulan)")
    
    def __repr__(self) -> str:
        return self.__str__()
