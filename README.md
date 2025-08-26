# USB Security Key 🔑
A Python script that uses a USB drive as a security key to keep your Windows session locked when the drive is removed.

## Features
- Monitors all drives for an authorized USB
- Locks the PC if the USB is removed
- Runs silently in the background
- Optional kill-switch for disabling the script

## Usage
1. Install Python 3.x and add to PATH.
2. Edit `usb_Security_key.py` and set your authorized USB’s serial number.
3. Run the script.
4. Paste the Startup file.txt in startup folder (win + r = shell:startup) and rename it with .bat.
5. Make sure the .bat file is enable in startup (TaskManager).

## Additional Points
1. Edit the .bat file according to path.
2. Edit the usb_security_key.py file according to your authorized USB’s serial number.
3. If you lost your USB drive and stuck in the loop then you can create a (1.txt) file on desktop to kill the process refer the file name and the path to create in     the usb_security_key.py (line no.7). 
