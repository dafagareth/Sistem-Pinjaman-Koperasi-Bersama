"""
View layer untuk presentation logic
Mengikuti MVC pattern - View bertanggung jawab untuk UI/presentation
"""
from typing import List, Optional
from decimal import Decimal
from models.pinjaman import Pinjaman, JenisPinjaman
from services.pinjaman_service import StatistikPinjaman


class ConsoleView:
    """
    View untuk console interface
    Bertanggung jawab untuk:
    - Menampilkan data ke user
    - Formatting output
    - UI presentation
    
    Tidak bertanggung jawab untuk:
    - Business logic
    - Data validation
    - Data access
    """
    
    # ANSI Color Codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    
    def __init__(self, use_colors: bool = True):
        """
        Initialize view
        
        Args:
            use_colors: Enable/disable ANSI colors
        """
        self.use_colors = use_colors
        if not use_colors:
            # Disable colors
            self.RESET = self.BOLD = self.RED = self.GREEN = ""
            self.YELLOW = self.BLUE = self.MAGENTA = self.CYAN = self.WHITE = ""
    
    def clear_screen(self) -> None:
        """Clear terminal screen"""
        import os
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def tampilkan_header(self, judul: str) -> None:
        """
        Tampilkan header aplikasi
        
        Args:
            judul: Teks judul
        """
        print(f'\n{self.CYAN}{self.BOLD}')
        print("  " + "-" * 65)
        print(f"  {judul.center(65)}")
        print("  " + "-" * 65)
        print(f'{self.RESET}\n')
    
    def tampilkan_menu_utama(self) -> None:
        """Tampilkan menu utama"""
        print(f'{self.GREEN}{self.BOLD}  {"-" * 49}{self.RESET}')
        print(f'{self.GREEN}{self.BOLD}  {self.WHITE}{"MENU UTAMA".center(49)}{self.GREEN}{self.RESET}')
        print(f'{self.GREEN}{self.BOLD}  {"-" * 49}{self.RESET}')
        print(f'{self.GREEN}  {self.YELLOW}[1]{self.WHITE} Entry Data Pinjaman{" " * 27}{self.GREEN}{self.RESET}')
        print(f'{self.GREEN}  {self.YELLOW}[2]{self.WHITE} Laporan Data Pinjaman{" " * 24}{self.GREEN}{self.RESET}')
        print(f'{self.GREEN}  {self.RED}[3]{self.WHITE} Exit{" " * 41}{self.GREEN}{self.RESET}')
        print(f'{self.GREEN}{self.BOLD}  {"-" * 49}{self.RESET}')
    
    def tampilkan_pilihan_jenis(self) -> None:
        """Tampilkan pilihan jenis pinjaman"""
        print(f'\n{self.GREEN}  {"-" * 49}{self.RESET}')
        print(f'{self.GREEN}  {self.YELLOW}Jenis Pinjaman{" " * 35}{self.GREEN}{self.RESET}')
        print(f'{self.GREEN}  {"-" * 49}{self.RESET}')
        print(f'{self.WHITE}  [A] Konsumtif (Bunga 15% per tahun){self.RESET}')
        print(f'{self.WHITE}  [B] Modal (Bunga 10% per tahun){self.RESET}')
    
    def tampilkan_ringkasan_pinjaman(self, pinjaman: Pinjaman) -> None:
        """
        Tampilkan ringkasan data pinjaman
        
        Args:
            pinjaman: Object Pinjaman yang akan ditampilkan
        """
        print(f'\n{self.BLUE}{self.BOLD}  {"-" * 49}{self.RESET}')
        print(f'{self.BLUE}{self.BOLD}  {self.WHITE}{"RINGKASAN DATA PINJAMAN".center(49)}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}{self.BOLD}  {"-" * 49}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}No. Anggota      : {self.YELLOW}{pinjaman.anggota.nomor}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Nama Anggota     : {self.YELLOW}{pinjaman.anggota.nama}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Kode Pinjaman    : {self.YELLOW}{pinjaman.jenis.kode}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Jenis Pinjaman   : {self.YELLOW}{pinjaman.jenis.nama}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Tingkat Bunga    : {self.YELLOW}{pinjaman.jenis.tingkat_bunga}% per tahun{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Jumlah Pinjaman  : {self.YELLOW}Rp {float(pinjaman.jumlah):,.0f}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Lama Pinjaman    : {self.YELLOW}{pinjaman.lama_bulan} bulan{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Jumlah Angsuran  : {self.YELLOW}Rp {float(pinjaman.angsuran):,.0f}/bln{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}{self.BOLD}  {"-" * 49}{self.RESET}')
    
    def tampilkan_tabel_laporan(self, pinjaman_list: List[Pinjaman]) -> None:
        """
        Tampilkan tabel laporan pinjaman
        
        Args:
            pinjaman_list: List of Pinjaman objects
        """
        # Header
        print(f'\n{self.GREEN}{self.BOLD}  {"-" * 100}{self.RESET}')
        print(f'{self.GREEN}{self.BOLD}  No | Nama Anggota    | Kode |   Jenis    | Bunga |   Pinjaman    | Lama  |   Angsuran     {self.RESET}')
        print(f'{self.GREEN}{self.BOLD}     |                 |      |  Pinjaman  |   %   |      (Rp)     | Bulan |     (Rp)       {self.RESET}')
        print(f'{self.GREEN}{self.BOLD}  {"-" * 100}{self.RESET}')
        
        # Data rows
        for idx, p in enumerate(pinjaman_list, 1):
            # Tentukan warna berdasarkan jenis
            if p.jenis == JenisPinjaman.KONSUMTIF:
                kode_color = self.YELLOW
                jenis_color = self.YELLOW
            else:
                kode_color = self.MAGENTA
                jenis_color = self.MAGENTA
            
            # Alternate row colors
            row_color = self.CYAN if idx % 2 == 0 else self.WHITE
            
            print(f'{self.GREEN}  {row_color}{idx:<3}{self.GREEN}| {row_color}{p.anggota.nama[:15]:<15}{self.GREEN} | {kode_color}{p.jenis.kode:^4}{self.GREEN} | {jenis_color}{p.jenis.nama[:10]:<10}{self.GREEN} |{row_color} {p.jenis.tingkat_bunga:>3}%  {self.GREEN}|{row_color} {float(p.jumlah):>13,.0f} {self.GREEN}|{row_color} {p.lama_bulan:>4}  {self.GREEN}|{row_color} {float(p.angsuran):>14,.0f} {self.GREEN}{self.RESET}')
        
        # Footer
        print(f'{self.GREEN}{self.BOLD}  {"-" * 100}{self.RESET}')
    
    def tampilkan_statistik(self, stats: StatistikPinjaman) -> None:
        """
        Tampilkan statistik pinjaman
        
        Args:
            stats: StatistikPinjaman object
        """
        print(f'\n{self.BLUE}{self.BOLD}  {"-" * 86}{self.RESET}')
        print(f'{self.BLUE}{self.BOLD}  {self.WHITE}{"RINGKASAN DATA".center(86)}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}{self.BOLD}  {"-" * 86}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Total Data Pinjaman       : {self.YELLOW}{stats.total_data:>3} data{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Total Pinjaman Keseluruhan: {self.YELLOW}Rp {float(stats.total_pinjaman):>15,.0f}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Total Bunga Keseluruhan   : {self.YELLOW}Rp {float(stats.total_bunga):>15,.0f}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Total Bayar Keseluruhan   : {self.YELLOW}Rp {float(stats.total_bayar_keseluruhan):>15,.0f}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Rata-rata Pinjaman        : {self.YELLOW}Rp {float(stats.rata_rata_pinjaman):>15,.0f}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Total Angsuran per Bulan  : {self.YELLOW}Rp {float(stats.total_angsuran):>15,.0f}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}  {self.WHITE}Rata-rata Angsuran        : {self.YELLOW}Rp {float(stats.rata_rata_angsuran):>15,.0f}{self.BLUE}{self.RESET}')
        print(f'{self.BLUE}{self.BOLD}  {"-" * 86}{self.RESET}')
        
        # Keterangan
        print(f'\n{self.MAGENTA}  {"-" * 60}{self.RESET}')
        print(f'{self.MAGENTA}  {self.CYAN}Keterangan:{self.MAGENTA}{self.RESET}')
        print(f'{self.MAGENTA}  {self.YELLOW}[A] = Pinjaman Konsumtif (Bunga 15% per tahun){self.MAGENTA}{self.RESET}')
        print(f'{self.MAGENTA}  {self.MAGENTA}[B] = Pinjaman Modal (Bunga 10% per tahun){self.MAGENTA}{self.RESET}')
        print(f'{self.MAGENTA}  {"-" * 60}{self.RESET}')
    
    def tampilkan_sukses(self, pesan: str) -> None:
        """Tampilkan pesan sukses"""
        print(f'\n{self.GREEN}  ✓ {pesan}{self.RESET}')
    
    def tampilkan_error(self, pesan: str) -> None:
        """Tampilkan pesan error"""
        print(f'\n{self.RED}  ✗ {pesan}{self.RESET}')
    
    def tampilkan_info(self, pesan: str) -> None:
        """Tampilkan pesan info"""
        print(f'\n{self.CYAN}  ℹ {pesan}{self.RESET}')
    
    def tampilkan_exit(self) -> None:
        """Tampilkan pesan exit"""
        print(f'\n{self.MAGENTA}{self.BOLD}')
        print("  " + "-" * 49)
        print(f"  {"TERIMA KASIH TELAH MENGGUNAKAN".center(49)}")
        print(f"  {"SISTEM PINJAMAN KOPERASI BERSAMA".center(49)}")
        print(f"  {"Program Selesai".center(49)}")
        print("  " + "-" * 49)
        print(f'{self.RESET}\n')
    
    def prompt(self, pesan: str) -> str:
        """
        Tampilkan prompt dan ambil input
        
        Args:
            pesan: Teks prompt
            
        Returns:
            Input dari user
        """
        return input(f'{self.CYAN}  ➤ {pesan}: {self.RESET}')
    
    def confirm(self, pesan: str) -> bool:
        """
        Tampilkan konfirmasi ya/tidak
        
        Args:
            pesan: Teks konfirmasi
            
        Returns:
            True jika yes, False jika no
        """
        jawaban = input(f'{self.CYAN}  ➤ {pesan} [Y/T]: {self.RESET}').upper()
        return jawaban == 'Y'
    
    def pause(self) -> None:
        """Pause untuk user press enter"""
        input(f'\n{self.CYAN}Press Enter to Continue...{self.RESET}')
