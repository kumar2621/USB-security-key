import ctypes
import time
import os

# --- CONFIG ---
AUTHORIZED_SERIAL = "CEF3-1656"   # your USB serial (from `vol D:`)
KILL_SWITCH = r"C:\Users\YourUsername\Desktop\1.txt"  # if this file exists, script exits

# Windows API
kernel32 = ctypes.windll.kernel32

# Drive type constants
DRIVE_UNKNOWN = 0
DRIVE_NO_ROOT_DIR = 1
DRIVE_REMOVABLE = 2
DRIVE_FIXED = 3
DRIVE_REMOTE = 4
DRIVE_CDROM = 5
DRIVE_RAMDISK = 6

def get_drive_type(root_path):
    """Return drive type for a root path like 'D:\\'."""
    return kernel32.GetDriveTypeW(root_path)

def get_volume_serial_root(root_path):
    """
    Uses GetVolumeInformationW to return the volume serial in 'XXXX-YYYY' format,
    or None if it can't be retrieved.
    root_path must be like 'D:\\'
    """
    vol_name_buf = ctypes.create_unicode_buffer(260)
    fs_name_buf = ctypes.create_unicode_buffer(260)
    vol_serial = ctypes.c_uint()
    max_comp_len = ctypes.c_uint()
    fs_flags = ctypes.c_uint()

    res = kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p(root_path),
        vol_name_buf,
        ctypes.sizeof(vol_name_buf),
        ctypes.byref(vol_serial),
        ctypes.byref(max_comp_len),
        ctypes.byref(fs_flags),
        fs_name_buf,
        ctypes.sizeof(fs_name_buf)
    )
    if res == 0:
        return None

    serial_int = vol_serial.value
    high = (serial_int >> 16) & 0xFFFF
    low = serial_int & 0xFFFF
    return f"{high:04X}-{low:04X}"

def normalize_serial(s):
    """Remove dash and uppercase, so formats match."""
    if s is None:
        return None
    return s.replace("-", "").upper()

def find_drives_with_serial(target_serial):
    """
    Scan A:..Z: and return list of drive letters (['D:', 'E:']) that match the serial.
    """
    found = []
    target_norm = normalize_serial(target_serial)
    for i in range(65, 91):  # ASCII A..Z
        drive_letter = chr(i) + ":\\"
        dtype = get_drive_type(drive_letter)
        if dtype in (DRIVE_NO_ROOT_DIR, DRIVE_UNKNOWN):
            continue
        serial = get_volume_serial_root(drive_letter)
        if serial and normalize_serial(serial) == target_norm:
            found.append(drive_letter[:-1])  # return like "D:"
    return found

def lock_screen():
    """Lock the Windows workstation."""
    ctypes.windll.user32.LockWorkStation()

def main():
    print("🔑 USB Guard started. Monitoring for authorized key...")

    while True:
        # Safety kill-switch
        if os.path.exists(KILL_SWITCH):
            print("⚠️ Kill-switch file detected, exiting guard.")
            break

        matched = find_drives_with_serial(AUTHORIZED_SERIAL)
        present = len(matched) > 0

        if present:
            print("✅ Authorized USB found on:", ", ".join(matched))
        else:
            print("❌ Authorized USB NOT found. Locking system...")
            lock_screen()

        time.sleep(8)  # check every 3 seconds

if __name__ == "__main__":
    main()


