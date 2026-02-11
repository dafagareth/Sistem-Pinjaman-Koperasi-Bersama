"""
Unit tests untuk models (Pinjaman, Anggota, JenisPinjaman)
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decimal import Decimal
from models.pinjaman import Pinjaman, Anggota, JenisPinjaman


class TestJenisPinjaman(unittest.TestCase):
    """Test JenisPinjaman enum"""
    
    def test_dari_kode_konsumtif(self):
        """Test factory method untuk kode A"""
        jenis = JenisPinjaman.dari_kode("A")
        self.assertEqual(jenis, JenisPinjaman.KONSUMTIF)
        self.assertEqual(jenis.nama, "Konsumtif")
        self.assertEqual(jenis.tingkat_bunga, 15)
    
    def test_dari_kode_modal(self):
        """Test factory method untuk kode B"""
        jenis = JenisPinjaman.dari_kode("B")
        self.assertEqual(jenis, JenisPinjaman.MODAL)
        self.assertEqual(jenis.nama, "Modal")
        self.assertEqual(jenis.tingkat_bunga, 10)
    
    def test_dari_kode_invalid(self):
        """Test factory method dengan kode invalid"""
        with self.assertRaises(ValueError):
            JenisPinjaman.dari_kode("X")


class TestAnggota(unittest.TestCase):
    """Test Anggota dataclass"""
    
    def test_anggota_valid(self):
        """Test membuat anggota valid"""
        anggota = Anggota(nomor="1001", nama="Budi Santoso")
        self.assertEqual(anggota.nomor, "1001")
        self.assertEqual(anggota.nama, "Budi Santoso")
    
    def test_anggota_nomor_kosong(self):
        """Test anggota dengan nomor kosong"""
        with self.assertRaises(ValueError):
            Anggota(nomor="", nama="Budi")
    
    def test_anggota_nama_kosong(self):
        """Test anggota dengan nama kosong"""
        with self.assertRaises(ValueError):
            Anggota(nomor="1001", nama="")


class TestPinjaman(unittest.TestCase):
    """Test Pinjaman dataclass dan perhitungan"""
    
    def setUp(self):
        """Setup data untuk testing"""
        self.anggota = Anggota(nomor="1001", nama="Test User")
        self.jenis_konsumtif = JenisPinjaman.KONSUMTIF
        self.jenis_modal = JenisPinjaman.MODAL
    
    def test_pinjaman_konsumtif_perhitungan(self):
        """Test perhitungan pinjaman konsumtif"""
        pinjaman = Pinjaman(
            anggota=self.anggota,
            jenis=self.jenis_konsumtif,
            jumlah=Decimal("10000000"),
            lama_bulan=12
        )
        
        # Bunga: 15% per tahun = 1.25% per bulan
        # Bunga per bulan: 10,000,000 * 1.25% = 125,000
        # Pokok per bulan: 10,000,000 / 12 = 833,333.33
        # Angsuran: 125,000 + 833,333.33 = 958,333.33
        
        expected_bunga = Decimal("125000")
        expected_pokok = Decimal("10000000") / Decimal("12")
        expected_angsuran = expected_bunga + expected_pokok
        
        self.assertAlmostEqual(float(pinjaman.bunga_per_bulan), float(expected_bunga), places=2)
        self.assertAlmostEqual(float(pinjaman.pokok_per_bulan), float(expected_pokok), places=2)
        self.assertAlmostEqual(float(pinjaman.angsuran), float(expected_angsuran), places=2)
    
    def test_pinjaman_modal_perhitungan(self):
        """Test perhitungan pinjaman modal"""
        pinjaman = Pinjaman(
            anggota=self.anggota,
            jenis=self.jenis_modal,
            jumlah=Decimal("5000000"),
            lama_bulan=24
        )
        
        # Bunga: 10% per tahun = 0.833% per bulan
        # Bunga per bulan: 5,000,000 * 0.833% = 41,666.67
        # Pokok per bulan: 5,000,000 / 24 = 208,333.33
        # Angsuran: 41,666.67 + 208,333.33 = 250,000
        
        expected_bunga = Decimal("5000000") * Decimal("10") / Decimal("100") / Decimal("12")
        expected_pokok = Decimal("5000000") / Decimal("24")
        expected_angsuran = expected_bunga + expected_pokok
        
        self.assertAlmostEqual(float(pinjaman.bunga_per_bulan), float(expected_bunga), places=2)
        self.assertAlmostEqual(float(pinjaman.pokok_per_bulan), float(expected_pokok), places=2)
        self.assertAlmostEqual(float(pinjaman.angsuran), float(expected_angsuran), places=2)
    
    def test_total_bunga(self):
        """Test perhitungan total bunga"""
        pinjaman = Pinjaman(
            anggota=self.anggota,
            jenis=self.jenis_konsumtif,
            jumlah=Decimal("10000000"),
            lama_bulan=12
        )
        
        # Total bunga = 125,000 * 12 = 1,500,000
        expected_total_bunga = Decimal("125000") * Decimal("12")
        self.assertAlmostEqual(float(pinjaman.total_bunga), float(expected_total_bunga), places=2)
    
    def test_total_bayar(self):
        """Test perhitungan total bayar"""
        pinjaman = Pinjaman(
            anggota=self.anggota,
            jenis=self.jenis_konsumtif,
            jumlah=Decimal("10000000"),
            lama_bulan=12
        )
        
        # Total bayar = 10,000,000 + 1,500,000 = 11,500,000
        expected_total_bayar = Decimal("10000000") + (Decimal("125000") * Decimal("12"))
        self.assertAlmostEqual(float(pinjaman.total_bayar), float(expected_total_bayar), places=2)
    
    def test_jumlah_negatif(self):
        """Test pinjaman dengan jumlah negatif"""
        with self.assertRaises(ValueError):
            Pinjaman(
                anggota=self.anggota,
                jenis=self.jenis_konsumtif,
                jumlah=Decimal("-1000"),
                lama_bulan=12
            )
    
    def test_lama_bulan_negatif(self):
        """Test pinjaman dengan lama negatif"""
        with self.assertRaises(ValueError):
            Pinjaman(
                anggota=self.anggota,
                jenis=self.jenis_konsumtif,
                jumlah=Decimal("1000000"),
                lama_bulan=-12
            )


if __name__ == '__main__':
    unittest.main()
