"""
Service layer untuk business logic pinjaman
Mengikuti Service Pattern dan Single Responsibility Principle
"""
from typing import List, Dict, Optional
from decimal import Decimal
from models.pinjaman import Pinjaman, Anggota, JenisPinjaman
from repositories.pinjaman_repository import PinjamanRepositoryInterface


class StatistikPinjaman:
    """Data class untuk statistik pinjaman"""
    
    def __init__(self, pinjaman_list: List[Pinjaman]):
        self.pinjaman_list = pinjaman_list
        self._total_pinjaman: Optional[Decimal] = None
        self._total_angsuran: Optional[Decimal] = None
        self._jumlah_konsumtif: Optional[int] = None
        self._jumlah_modal: Optional[int] = None
    
    @property
    def total_data(self) -> int:
        """Total jumlah data pinjaman"""
        return len(self.pinjaman_list)
    
    @property
    def total_pinjaman(self) -> Decimal:
        """Total nilai semua pinjaman"""
        if self._total_pinjaman is None:
            self._total_pinjaman = sum(
                (p.jumlah for p in self.pinjaman_list),
                Decimal('0')
            )
        return self._total_pinjaman
    
    @property
    def total_angsuran(self) -> Decimal:
        """Total angsuran per bulan dari semua pinjaman"""
        if self._total_angsuran is None:
            self._total_angsuran = sum(
                (p.angsuran for p in self.pinjaman_list),
                Decimal('0')
            )
        return self._total_angsuran
    
    @property
    def rata_rata_pinjaman(self) -> Decimal:
        """Rata-rata nilai pinjaman"""
        if self.total_data == 0:
            return Decimal('0')
        return self.total_pinjaman / Decimal(str(self.total_data))
    
    @property
    def rata_rata_angsuran(self) -> Decimal:
        """Rata-rata angsuran per bulan"""
        if self.total_data == 0:
            return Decimal('0')
        return self.total_angsuran / Decimal(str(self.total_data))
    
    @property
    def jumlah_konsumtif(self) -> int:
        """Jumlah pinjaman konsumtif"""
        if self._jumlah_konsumtif is None:
            self._jumlah_konsumtif = sum(
                1 for p in self.pinjaman_list 
                if p.jenis == JenisPinjaman.KONSUMTIF
            )
        return self._jumlah_konsumtif
    
    @property
    def jumlah_modal(self) -> int:
        """Jumlah pinjaman modal"""
        if self._jumlah_modal is None:
            self._jumlah_modal = sum(
                1 for p in self.pinjaman_list 
                if p.jenis == JenisPinjaman.MODAL
            )
        return self._jumlah_modal
    
    @property
    def persentase_konsumtif(self) -> float:
        """Persentase pinjaman konsumtif"""
        if self.total_data == 0:
            return 0.0
        return (self.jumlah_konsumtif / self.total_data) * 100
    
    @property
    def persentase_modal(self) -> float:
        """Persentase pinjaman modal"""
        if self.total_data == 0:
            return 0.0
        return (self.jumlah_modal / self.total_data) * 100
    
    @property
    def total_bunga(self) -> Decimal:
        """Total bunga dari semua pinjaman"""
        return sum((p.total_bunga for p in self.pinjaman_list), Decimal('0'))
    
    @property
    def total_bayar_keseluruhan(self) -> Decimal:
        """Total yang harus dibayar keseluruhan (pokok + bunga)"""
        return sum((p.total_bayar for p in self.pinjaman_list), Decimal('0'))
    
    def to_dict(self) -> Dict:
        """Convert statistik ke dictionary"""
        return {
            'total_data': self.total_data,
            'total_pinjaman': float(self.total_pinjaman),
            'total_angsuran': float(self.total_angsuran),
            'rata_rata_pinjaman': float(self.rata_rata_pinjaman),
            'rata_rata_angsuran': float(self.rata_rata_angsuran),
            'jumlah_konsumtif': self.jumlah_konsumtif,
            'jumlah_modal': self.jumlah_modal,
            'persentase_konsumtif': self.persentase_konsumtif,
            'persentase_modal': self.persentase_modal,
            'total_bunga': float(self.total_bunga),
            'total_bayar_keseluruhan': float(self.total_bayar_keseluruhan)
        }


class PinjamanService:
    """
    Service untuk mengelola business logic pinjaman
    
    Responsibilities:
    - Validasi business rules
    - Orchestrasi operasi pinjaman
    - Perhitungan statistik
    - Koordinasi dengan repository
    """
    
    def __init__(self, repository: PinjamanRepositoryInterface):
        """
        Initialize service dengan repository
        
        Args:
            repository: Implementation of PinjamanRepositoryInterface
        """
        self.repository = repository
    
    def buat_pinjaman(
        self,
        nomor_anggota: str,
        nama_anggota: str,
        kode_jenis: str,
        jumlah: float,
        lama_bulan: int
    ) -> Pinjaman:
        """
        Buat pinjaman baru dengan validasi
        
        Args:
            nomor_anggota: Nomor identitas anggota
            nama_anggota: Nama lengkap anggota
            kode_jenis: Kode jenis pinjaman (A/B)
            jumlah: Jumlah pinjaman dalam Rupiah
            lama_bulan: Lama pinjaman dalam bulan
            
        Returns:
            Pinjaman object yang sudah dibuat
            
        Raises:
            ValueError: Jika data tidak valid
        """
        # Validasi business rules
        self._validasi_input(nomor_anggota, nama_anggota, kode_jenis, jumlah, lama_bulan)
        
        # Buat objects
        anggota = Anggota(nomor=nomor_anggota, nama=nama_anggota)
        jenis = JenisPinjaman.dari_kode(kode_jenis)
        
        pinjaman = Pinjaman(
            anggota=anggota,
            jenis=jenis,
            jumlah=Decimal(str(jumlah)),
            lama_bulan=lama_bulan
        )
        
        return pinjaman
    
    def simpan_pinjaman(self, pinjaman: Pinjaman) -> bool:
        """
        Simpan pinjaman ke repository
        
        Args:
            pinjaman: Object Pinjaman yang akan disimpan
            
        Returns:
            True jika berhasil, False jika gagal
        """
        return self.repository.simpan(pinjaman)
    
    def ambil_semua_pinjaman(self) -> List[Pinjaman]:
        """
        Ambil semua data pinjaman
        
        Returns:
            List of Pinjaman objects
        """
        return self.repository.ambil_semua()
    
    def ambil_pinjaman_anggota(self, nomor_anggota: str) -> List[Pinjaman]:
        """
        Ambil semua pinjaman milik seorang anggota
        
        Args:
            nomor_anggota: Nomor anggota yang dicari
            
        Returns:
            List of Pinjaman milik anggota tersebut
        """
        return self.repository.ambil_berdasarkan_anggota(nomor_anggota)
    
    def hitung_statistik(self) -> StatistikPinjaman:
        """
        Hitung statistik dari semua pinjaman
        
        Returns:
            StatistikPinjaman object
        """
        pinjaman_list = self.ambil_semua_pinjaman()
        return StatistikPinjaman(pinjaman_list)
    
    def ambil_pinjaman_terbaru(self, jumlah: int = 5) -> List[Pinjaman]:
        """
        Ambil N pinjaman terbaru
        
        Args:
            jumlah: Jumlah data yang diambil (default: 5)
            
        Returns:
            List of Pinjaman terbaru
        """
        semua_pinjaman = self.ambil_semua_pinjaman()
        return semua_pinjaman[-jumlah:] if len(semua_pinjaman) >= jumlah else semua_pinjaman
    
    def reset_data(self) -> bool:
        """
        Hapus semua data pinjaman (untuk testing/reset)
        
        Returns:
            True jika berhasil
        """
        return self.repository.hapus_semua()
    
    def _validasi_input(
        self,
        nomor_anggota: str,
        nama_anggota: str,
        kode_jenis: str,
        jumlah: float,
        lama_bulan: int
    ) -> None:
        """
        Validasi input data pinjaman
        
        Raises:
            ValueError: Jika ada data yang tidak valid
        """
        # Validasi nomor anggota
        if not nomor_anggota or len(nomor_anggota.strip()) == 0:
            raise ValueError("Nomor anggota tidak boleh kosong")
        
        # Validasi nomor anggota harus 4 digit numeric
        nomor_anggota = nomor_anggota.strip()
        if not nomor_anggota.isdigit():
            raise ValueError("Nomor anggota harus berupa angka")
        if len(nomor_anggota) != 4:
            raise ValueError("Nomor anggota harus 4 digit (contoh: 1001)")
        
        # Validasi nama
        if not nama_anggota or len(nama_anggota.strip()) == 0:
            raise ValueError("Nama anggota tidak boleh kosong")
        
        # Validasi kode jenis
        kode_jenis = kode_jenis.strip().upper()
        if kode_jenis not in ['A', 'B']:
            raise ValueError("Kode jenis harus A (Konsumtif) atau B (Modal)")
        
        # Validasi jumlah
        if jumlah <= 0:
            raise ValueError("Jumlah pinjaman harus lebih dari 0")
        
        # Validasi lama
        if lama_bulan <= 0:
            raise ValueError("Lama pinjaman harus lebih dari 0 bulan")
        
        # Business rule: Maximum loan period
        if lama_bulan > 120:  # 10 tahun
            raise ValueError("Lama pinjaman maksimal 120 bulan (10 tahun)")
        
        # Business rule: Minimum loan amount
        if jumlah < 100000:  # 100 ribu
            raise ValueError("Jumlah pinjaman minimal Rp 100,000")

