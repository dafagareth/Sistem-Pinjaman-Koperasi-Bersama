"""
Unit tests untuk services (PinjamanService, StatistikPinjaman)
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decimal import Decimal
from services.pinjaman_service import PinjamanService, StatistikPinjaman
from models.pinjaman import Pinjaman, Anggota, JenisPinjaman


class TestPinjamanServiceValidation(unittest.TestCase):
    """Test validasi di PinjamanService"""
    
    def test_validasi_nomor_anggota_4_digit(self):
        """Test validasi nomor anggota harus 4 digit"""
        service = PinjamanService(repository=None)  # Mock repository
        
        # Test nomor anggota kurang dari 4 digit
        with self.assertRaises(ValueError) as context:
            service._validasi_input("123", "Budi", "A", 1000000, 12)
        self.assertIn("4 digit", str(context.exception))
        
        # Test nomor anggota lebih dari 4 digit
        with self.assertRaises(ValueError) as context:
            service._validasi_input("12345", "Budi", "A", 1000000, 12)
        self.assertIn("4 digit", str(context.exception))
    
    def test_validasi_nomor_anggota_harus_numeric(self):
        """Test validasi nomor anggota harus numeric"""
        service = PinjamanService(repository=None)
        
        with self.assertRaises(ValueError) as context:
            service._validasi_input("ABC1", "Budi", "A", 1000000, 12)
        self.assertIn("angka", str(context.exception))
    
    def test_validasi_jumlah_minimum(self):
        """Test validasi jumlah minimum"""
        service = PinjamanService(repository=None)
        
        with self.assertRaises(ValueError) as context:
            service._validasi_input("1001", "Budi", "A", 50000, 12)
        self.assertIn("100,000", str(context.exception))
    
    def test_validasi_lama_maksimum(self):
        """Test validasi lama maksimum"""
        service = PinjamanService(repository=None)
        
        with self.assertRaises(ValueError) as context:
            service._validasi_input("1001", "Budi", "A", 1000000, 150)
        self.assertIn("120 bulan", str(context.exception))


class TestStatistikPinjaman(unittest.TestCase):
    """Test StatistikPinjaman"""
    
    def setUp(self):
        """Setup data untuk testing"""
        anggota1 = Anggota("1001", "User 1")
        anggota2 = Anggota("1002", "User 2")
        
        self.pinjaman_list = [
            Pinjaman(anggota1, JenisPinjaman.KONSUMTIF, Decimal("10000000"), 12),
            Pinjaman(anggota2, JenisPinjaman.MODAL, Decimal("5000000"), 24)
        ]
        self.stats = StatistikPinjaman(self.pinjaman_list)
    
    def test_total_data(self):
        """Test total data"""
        self.assertEqual(self.stats.total_data, 2)
    
    def test_total_pinjaman(self):
        """Test total pinjaman"""
        expected = Decimal("10000000") + Decimal("5000000")
        self.assertEqual(self.stats.total_pinjaman, expected)
    
    def test_jumlah_konsumtif_modal(self):
        """Test jumlah per jenis"""
        self.assertEqual(self.stats.jumlah_konsumtif, 1)
        self.assertEqual(self.stats.jumlah_modal, 1)
    
    def test_total_bunga(self):
        """Test total bunga"""
        # Pinjaman 1: 125,000 * 12 = 1,500,000
        # Pinjaman 2: ~41,667 * 24 = 1,000,000
        # Total: ~2,500,000
        self.assertGreater(self.stats.total_bunga, Decimal("2400000"))
        self.assertLess(self.stats.total_bunga, Decimal("2600000"))
    
    def test_statistik_empty_list(self):
        """Test statistik dengan list kosong"""
        stats = StatistikPinjaman([])
        self.assertEqual(stats.total_data, 0)
        self.assertEqual(stats.total_pinjaman, Decimal("0"))
        self.assertEqual(stats.rata_rata_pinjaman, Decimal("0"))


if __name__ == '__main__':
    unittest.main()
