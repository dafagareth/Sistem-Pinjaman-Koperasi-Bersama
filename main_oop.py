"""
Main entry point untuk aplikasi Sistem Pinjaman Koperasi
Menggunakan Dependency Injection untuk loose coupling
"""
from repositories.pinjaman_repository import PinjamanFileRepository
from services.pinjaman_service import PinjamanService
from views.console_view import ConsoleView
from controllers.pinjaman_controller import PinjamanController


def main():
    """
    Main function - Application entry point
    
    Menggunakan Dependency Injection untuk:
    - Loose coupling antar komponen
    - Testability (mudah di-mock)
    - Flexibility (mudah diganti implementasinya)
    """
    
    # Dependency Injection - Buat semua dependencies
    
    # 1. Repository (Data Access Layer)
    repository = PinjamanFileRepository(filepath="pinjaman.csv")
    
    # 2. Service (Business Logic Layer)
    service = PinjamanService(repository=repository)
    
    # 3. View (Presentation Layer)
    view = ConsoleView(use_colors=True)
    
    # 4. Controller (Application Flow Control)
    controller = PinjamanController(service=service, view=view)
    
    # Jalankan aplikasi
    controller.jalankan()


if __name__ == "__main__":
    main()
