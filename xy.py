#!/usr/bin/env python3
"""Print X,Y when you tap the Android screen (USB debugging + adb required)."""

from __future__ import annotations

import argparse
import subprocess
import sys


def check_adb(device: str | None) -> None:
    cmd = ["adb"]
    if device:
        cmd.extend(["-s", device])
    cmd.append("get-state")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        sys.exit("adb not found. Install: sudo pacman -S android-tools")
    except subprocess.CalledProcessError:
        sys.exit("No device. Plug in phone, enable USB debugging, run: adb devices")


def stream_taps(device: str | None, live: bool) -> None:
    cmd = ["adb"]
    if device:
        cmd.extend(["-s", device])
    cmd.extend(["shell", "getevent", "-l"])

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    assert proc.stdout is not None

    x: int | None = None
    y: int | None = None

    print("Tap the phone. Ctrl+C to quit.\n")

    for line in proc.stdout:
        if "ABS_MT_POSITION_X" in line:
            x = _parse_hex_value(line)
        elif "ABS_MT_POSITION_Y" in line:
            y = _parse_hex_value(line)
        elif live and x is not None and y is not None and "ABS_MT" in line:
            print(f"\rx={x}, y={y}   ", end="", flush=True)
        elif "BTN_TOUCH" in line and "UP" in line and x is not None and y is not None:
            print(f"\rx={x}, y={y}  →  tap [{x}, {y}]")
            x = y = None


def _parse_hex_value(line: str) -> int:
    # getevent -l lines end with hex, e.g. "003a"
    token = line.strip().split()[-1]
    return int(token, 16)


def enable_pointer_overlay(device: str | None, on: bool) -> None:
    """Show X,Y on the phone screen itself (developer-style overlay)."""
    cmd = ["adb"]
    if device:
        cmd.extend(["-s", device])
    value = "1" if on else "0"
    subprocess.run(
        cmd + ["shell", "settings", "put", "system", "pointer_location", value],
        check=True,
    )
    if on:
        print("Pointer overlay ON — coordinates show at top of phone screen.")
        print("Turn off: python xy.py --overlay-off")
    else:
        print("Pointer overlay OFF.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Show Android touch X,Y via adb")
    parser.add_argument("-s", "--device", help="adb device serial (adb devices)")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Print position while finger moves (noisier)",
    )
    parser.add_argument(
        "--overlay-on",
        action="store_true",
        help="Draw X,Y on the phone screen (pointer location)",
    )
    parser.add_argument(
        "--overlay-off",
        action="store_true",
        help="Turn off on-screen pointer location",
    )
    args = parser.parse_args()

    check_adb(args.device)

    if args.overlay_on:
        enable_pointer_overlay(args.device, True)
        return
    if args.overlay_off:
        enable_pointer_overlay(args.device, False)
        return

    try:
        stream_taps(args.device, args.live)
    except KeyboardInterrupt:
        print("\nDone.")


if __name__ == "__main__":
    main()
