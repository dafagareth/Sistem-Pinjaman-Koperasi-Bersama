"""
Repository untuk akses data pinjaman
Mengikuti Repository Pattern untuk abstraksi data access
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal
import csv
import logging
import fcntl
from models.pinjaman import Pinjaman, Anggota, JenisPinjaman


class PinjamanRepositoryInterface(ABC):
    """Interface untuk PinjamanRepository (Dependency Inversion Principle)"""
    
    @abstractmethod
    def simpan(self, pinjaman: Pinjaman) -> bool:
        """Simpan pinjaman baru"""
        pass
    
    @abstractmethod
    def ambil_semua(self) -> List[Pinjaman]:
        """Ambil semua data pinjaman"""
        pass
    
    @abstractmethod
    def ambil_berdasarkan_anggota(self, nomor_anggota: str) -> List[Pinjaman]:
        """Ambil pinjaman berdasarkan nomor anggota"""
        pass
    
    @abstractmethod
    def hapus_semua(self) -> bool:
        """Hapus semua data (untuk testing)"""
        pass


class PinjamanFileRepository(PinjamanRepositoryInterface):
    """
    Implementasi repository menggunakan CSV file sebagai storage
    Mengikuti Single Responsibility Principle
    """
    
    CSV_HEADERS = ['nomor_anggota', 'nama_anggota', 'kode_pinjaman', 'jumlah_pinjaman', 'lama_bulan']
    
    def __init__(self, filepath: str = "pinjaman.csv"):
        """
        Initialize repository dengan file path
        
        Args:
            filepath: Path ke file penyimpanan data (CSV format)
        """
        self.filepath = filepath
        self.logger = logging.getLogger(__name__)
        self._cache: Optional[List[Pinjaman]] = None
    
    
    def simpan(self, pinjaman: Pinjaman) -> bool:
        """
        Simpan pinjaman ke CSV file dengan file locking
        
        Args:
            pinjaman: Object Pinjaman yang akan disimpan
            
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            # Check if file exists to determine if we need to write headers
            file_exists = False
            try:
                with open(self.filepath, 'r', encoding='utf-8'):
                    file_exists = True
            except FileNotFoundError:
                pass
            
            with open(self.filepath, 'a', encoding='utf-8', newline='') as f:
                # Lock file untuk thread safety
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                
                try:
                    writer = csv.DictWriter(f, fieldnames=self.CSV_HEADERS)
                    
                    # Write header jika file baru
                    if not file_exists:
                        writer.writeheader()
                    
                    # Write data
                    writer.writerow({
                        'nomor_anggota': pinjaman.anggota.nomor,
                        'nama_anggota': pinjaman.anggota.nama,
                        'kode_pinjaman': pinjaman.jenis.kode,
                        'jumlah_pinjaman': str(int(pinjaman.jumlah)),
                        'lama_bulan': str(pinjaman.lama_bulan)
                    })
                    
                    # Invalidate cache
                    self._cache = None
                    
                finally:
                    # Unlock file
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            
            self.logger.info(f"Data pinjaman berhasil disimpan: {pinjaman.anggota.nomor}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error menyimpan data: {e}")
            raise IOError(f"Gagal menyimpan data ke file: {e}")
    
    
    def ambil_semua(self) -> List[Pinjaman]:
        """
        Ambil semua data pinjaman dari CSV file dengan caching
        
        Returns:
            List of Pinjaman objects
        """
        # Return from cache if available
        if self._cache is not None:
            return self._cache
        
        pinjaman_list = []
        
        try:
            with open(self.filepath, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    try:
                        pinjaman = self._from_csv_row(row)
                        pinjaman_list.append(pinjaman)
                    except Exception as e:
                        # Skip corrupted lines
                        self.logger.warning(f"Skipping corrupted row: {e}")
                        continue
                        
        except FileNotFoundError:
            # File belum ada, return empty list
            self.logger.info("File data belum ada, mengembalikan list kosong")
            return []
        except Exception as e:
            self.logger.error(f"Error membaca data: {e}")
            raise IOError(f"Gagal membaca data dari file: {e}")
        
        # Cache the result
        self._cache = pinjaman_list
        return pinjaman_list
    
    def ambil_berdasarkan_anggota(self, nomor_anggota: str) -> List[Pinjaman]:
        """
        Ambil pinjaman berdasarkan nomor anggota
        
        Args:
            nomor_anggota: Nomor anggota yang dicari
            
        Returns:
            List of Pinjaman milik anggota tersebut
        """
        semua_pinjaman = self.ambil_semua()
        return [p for p in semua_pinjaman if p.anggota.nomor == nomor_anggota]
    
    
    def hapus_semua(self) -> bool:
        """
        Hapus semua data (untuk testing/reset) dengan cache invalidation
        
        Returns:
            True jika berhasil
        """
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write('')
            
            # Invalidate cache
            self._cache = None
            
            self.logger.info("Semua data berhasil dihapus")
            return True
        except Exception as e:
            self.logger.error(f"Error menghapus data: {e}")
            raise IOError(f"Gagal menghapus data: {e}")
    
    
    def _from_csv_row(self, row: dict) -> Pinjaman:
        """
        Convert CSV row (dict) menjadi Pinjaman object
        
        Args:
            row: Dictionary dari CSV DictReader
            
        Returns:
            Pinjaman object
            
        Raises:
            ValueError: Jika format data tidak valid
        """
        try:
            # Extract data
            no_anggota = row['nomor_anggota'].strip()
            nama = row['nama_anggota'].strip()
            kode = row['kode_pinjaman'].strip()
            jumlah = Decimal(row['jumlah_pinjaman'].strip())
            lama = int(row['lama_bulan'].strip())
            
            # Buat objects
            anggota = Anggota(nomor=no_anggota, nama=nama)
            jenis = JenisPinjaman.dari_kode(kode)
            
            return Pinjaman(
                anggota=anggota,
                jenis=jenis,
                jumlah=jumlah,
                lama_bulan=lama
            )
        except KeyError as e:
            raise ValueError(f"Missing required field in CSV: {e}")
        except Exception as e:
            raise ValueError(f"Invalid data format: {e}")
