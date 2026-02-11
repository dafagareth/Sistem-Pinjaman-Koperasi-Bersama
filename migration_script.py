"""
Migration script untuk convert data dari format lama (pinjaman.txt) ke CSV (pinjaman.csv)
"""
import os
import sys
import csv
from decimal import Decimal

def migrate_old_to_csv(old_file="pinjaman.txt", new_file="pinjaman.csv", backup=True):
    """
    Migrate data dari format lama ke CSV
    
    Args:
        old_file: Path ke file lama
        new_file: Path ke file CSV baru
        backup: Buat backup dari file lama
    """
    if not os.path.exists(old_file):
        print(f"File {old_file} tidak ditemukan. Tidak ada yang di-migrate.")
        return
    
    # Backup file lama
    if backup:
        backup_file = old_file + ".backup"
        import shutil
        shutil.copy(old_file, backup_file)
        print(f"Backup dibuat: {backup_file}")
    
    # Read old format
    records = []
    DELIMITER = "|"
    
    try:
        with open(old_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    parts = line.split(DELIMITER)
                    if len(parts) < 8:
                        print(f"Warning: Line {line_num} format invalid, skipping")
                        continue
                    
                    record = {
                        'nomor_anggota': parts[1].strip(),
                        'nama_anggota': parts[2].strip(),
                        'kode_pinjaman': parts[3].strip(),
                        'jumlah_pinjaman': parts[6].strip(),
                        'lama_bulan': parts[7].strip()
                    }
                    records.append(record)
                    
                except Exception as e:
                    print(f"Warning: Error parsing line {line_num}: {e}")
                    continue
        
        print(f"Berhasil membaca {len(records)} records dari {old_file}")
        
    except Exception as e:
        print(f"Error membaca file lama: {e}")
        return
    
    # Write to CSV
    try:
        with open(new_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['nomor_anggota', 'nama_anggota', 'kode_pinjaman', 'jumlah_pinjaman', 'lama_bulan'])
            writer.writeheader()
            writer.writerows(records)
        
        print(f"Berhasil menulis {len(records)} records ke {new_file}")
        print("Migration selesai!")
        
    except Exception as e:
        print(f"Error menulis file CSV: {e}")
        return


if __name__ == "__main__":
    print("=== Migration Script: pinjaman.txt -> pinjaman.csv ===")
    migrate_old_to_csv()
