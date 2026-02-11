"""
Controller layer untuk orchestration
Mengikuti MVC pattern - Controller bertanggung jawab untuk:
- Mengatur alur aplikasi
- Koordinasi antara Model, View, dan Service
- Handling user input
- Error handling
"""
from typing import Optional
from models.pinjaman import Pinjaman
from services.pinjaman_service import PinjamanService
from views.console_view import ConsoleView


class PinjamanController:
    """
    Controller untuk mengatur flow aplikasi pinjaman
    
    Responsibilities:
    - Mengatur menu dan navigasi
    - Koordinasi antara Service dan View
    - Input handling dan validation
    - Error handling dan user feedback
    """
    
    def __init__(self, service: PinjamanService, view: ConsoleView):
        """
        Initialize controller
        
        Args:
            service: PinjamanService instance
            view: ConsoleView instance
        """
        self.service = service
        self.view = view
    
    def jalankan(self) -> None:
        """Main application loop"""
        self.view.clear_screen()
        
        while True:
            self._tampilkan_menu()
            
            try:
                pilihan = self.view.prompt("Pilih menu [1-3]")
                
                if pilihan == '1':
                    self._handle_entry_data()
                elif pilihan == '2':
                    self._handle_laporan()
                elif pilihan == '3':
                    self._handle_exit()
                    break
                else:
                    self.view.tampilkan_error("Pilihan tidak valid! Silakan pilih 1-3.")
                    self.view.pause()
                    self.view.clear_screen()
                    
            except KeyboardInterrupt:
                print("\n")
                self._handle_exit()
                break
            except Exception as e:
                self.view.tampilkan_error(f"Error tidak terduga: {str(e)}")
                self.view.pause()
                self.view.clear_screen()
    
    def _tampilkan_menu(self) -> None:
        """Tampilkan menu utama"""
        self.view.tampilkan_header("SISTEM PINJAMAN KOPERASI BERSAMA")
        self.view.tampilkan_menu_utama()
        print()
    
    def _handle_entry_data(self) -> None:
        """Handle menu entry data pinjaman"""
        self.view.clear_screen()
        
        lanjut = True
        while lanjut:
            try:
                self.view.tampilkan_header("ENTRY DATA PINJAMAN KOPERASI")
                
                # Input data
                pinjaman = self._input_data_pinjaman()
                
                if pinjaman is None:
                    # User membatalkan
                    break
                
                # Tampilkan ringkasan
                self.view.tampilkan_ringkasan_pinjaman(pinjaman)
                print()
                
                # Konfirmasi simpan
                if self.view.confirm("Simpan data ini?"):
                    if self.service.simpan_pinjaman(pinjaman):
                        self.view.tampilkan_sukses("Data berhasil disimpan!")
                    else:
                        self.view.tampilkan_error("Gagal menyimpan data!")
                else:
                    self.view.tampilkan_info("Data dibatalkan")
                
                # Tanya lanjut
                print()
                lanjut = self.view.confirm("Masih ada data yang akan diinputkan?")
                
                if lanjut:
                    self.view.clear_screen()
                    
            except ValueError as e:
                self.view.tampilkan_error(str(e))
                self.view.pause()
                self.view.clear_screen()
            except KeyboardInterrupt:
                print("\n")
                break
        
        self.view.pause()
        self.view.clear_screen()
    
    def _input_data_pinjaman(self) -> Optional[Pinjaman]:
        """
        Input data pinjaman dari user
        
        Returns:
            Pinjaman object atau None jika dibatalkan
            
        Raises:
            ValueError: Jika input tidak valid
        """
        # Input nomor anggota
        nomor_anggota = self.view.prompt("No. Anggota [4 digit]").strip()
        if not nomor_anggota:
            raise ValueError("Nomor anggota tidak boleh kosong")
        
        # Input nama
        nama_anggota = self.view.prompt("Nama Anggota").strip()
        if not nama_anggota:
            raise ValueError("Nama anggota tidak boleh kosong")
        
        # Input kode jenis
        self.view.tampilkan_pilihan_jenis()
        kode_jenis = self.view.prompt("Kode Pinjaman [A/B]").strip().upper()
        
        if kode_jenis not in ['A', 'B']:
            raise ValueError("Kode pinjaman harus A atau B")
        
        # Tampilkan jenis yang dipilih
        if kode_jenis == 'A':
            self.view.tampilkan_sukses("Jenis: Konsumtif - Bunga 15%")
        else:
            self.view.tampilkan_sukses("Jenis: Modal - Bunga 10%")
        
        print()
        
        # Input jumlah pinjaman
        while True:
            try:
                jumlah_str = self.view.prompt("Jumlah Pinjaman [Rp]").strip()
                jumlah = float(jumlah_str)
                break
            except ValueError:
                self.view.tampilkan_error("Masukkan angka yang valid!")
        
        # Input lama pinjaman
        while True:
            try:
                lama_str = self.view.prompt("Lama Pinjaman [Bulan]").strip()
                lama = int(lama_str)
                break
            except ValueError:
                self.view.tampilkan_error("Masukkan angka yang valid!")
        
        # Buat pinjaman (akan throw ValueError jika tidak valid)
        pinjaman = self.service.buat_pinjaman(
            nomor_anggota=nomor_anggota,
            nama_anggota=nama_anggota,
            kode_jenis=kode_jenis,
            jumlah=jumlah,
            lama_bulan=lama
        )
        
        return pinjaman
    
    def _handle_laporan(self) -> None:
        """Handle menu laporan"""
        self.view.clear_screen()
        
        try:
            self.view.tampilkan_header("LAPORAN DATA PINJAMAN KOPERASI BERSAMA")
            
            # Ambil data
            pinjaman_list = self.service.ambil_semua_pinjaman()
            
            if not pinjaman_list:
                self.view.tampilkan_info("Belum ada data untuk ditampilkan.")
                self.view.tampilkan_info("Silakan entry data terlebih dahulu.")
            else:
                # Tampilkan tabel
                self.view.tampilkan_tabel_laporan(pinjaman_list)
                
                # Tampilkan statistik
                stats = self.service.hitung_statistik()
                self.view.tampilkan_statistik(stats)
            
        except Exception as e:
            self.view.tampilkan_error(f"Error saat menampilkan laporan: {str(e)}")
        
        self.view.pause()
        self.view.clear_screen()
    
    def _handle_exit(self) -> None:
        """Handle menu exit"""
        self.view.clear_screen()
        self.view.tampilkan_exit()
