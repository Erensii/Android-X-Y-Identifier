# android-xy

Print **X,Y tap coordinates** from your Android phone over USB. Use the numbers for MacroDroid, Tasker, or any UI automation.

---

## What you need (all platforms)

| Item | Notes |
|------|--------|
| Android phone | USB debugging enabled |
| USB cable | Data-capable (not charge-only) |
| Python 3 | 3.10+ recommended |
| `adb` | Android platform tools |

### Enable USB debugging on your phone

1. **Settings → About phone** → tap **Build number** 7 times (enables Developer options).
2. **Settings → Developer options** → turn on **USB debugging**.
3. Plug the phone into the computer.
4. On the phone, tap **Allow** when asked to trust this computer.

Check the connection (any OS):

```bash
adb devices
```

You should see your device as `device` (not `unauthorized`).

---

## Linux

### 1. Install `adb` and Python

**Arch Linux**

```bash
sudo pacman -S android-tools python
```

**Debian / Ubuntu / Fedora**

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install android-tools-adb python3

# Fedora
sudo dnf install android-tools python3
```

### 2. Get the script

```bash
git clone https://github.com/YOUR_USERNAME/android-xy.git
cd android-xy
```

Or download `xy.py` only and `cd` into that folder.

### 3. Run

```bash
python xy.py
```

Tap the phone screen. The terminal prints something like:

```text
x=360, y=1850  →  tap [360, 1850]
```

**Ctrl+C** to quit.

### 4. Optional flags (Linux)

```bash
python xy.py --live          # show X,Y while finger moves
python xy.py --overlay-on    # draw coordinates on the phone screen
python xy.py --overlay-off   # turn overlay off
python xy.py -s SERIAL       # pick a device if several are listed in adb devices
```

### Linux troubleshooting

| Problem | Fix |
|---------|-----|
| `adb: command not found` | Install `android-tools` / `android-tools-adb` (see above). |
| `no permissions` / empty device list | Add udev rules or run `adb kill-server && adb start-server`. On some distros, add your user to plugdev. |
| `unauthorized` | Unlock phone, replug USB, accept the debugging prompt. |
| Wrong coordinates | Values are in the phone’s touch resolution; recalibrate if you change resolution or rotate the screen. |

---

## macOS

### 1. Install Homebrew (if needed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install `adb` and Python

```bash
brew install android-platform-tools python
```

### 3. Get the script

```bash
git clone https://github.com/YOUR_USERNAME/android-xy.git
cd android-xy
```

### 4. Run

```bash
python3 xy.py
```

Tap the screen and read `x=…, y=…` in the terminal.

### 5. Optional flags (macOS)

Same as Linux:

```bash
python3 xy.py --overlay-on
python3 xy.py --live
python3 xy.py -s SERIAL
```

### macOS troubleshooting

| Problem | Fix |
|---------|-----|
| `adb: command not found` | Run `brew install android-platform-tools`, then open a new terminal. |
| Device not listed | Use a data cable; try another USB port; unlock the phone. |
| `command not found: python` | Use `python3` instead of `python`. |

---

## Windows

### 1. Install Python

1. Download Python from [python.org/downloads](https://www.python.org/downloads/).
2. Run the installer.
3. Check **“Add python.exe to PATH”**.
4. Finish install.

Open **PowerShell** or **Command Prompt** and check:

```powershell
python --version
```

### 2. Install `adb` (platform-tools)

1. Download [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools) for Windows.
2. Extract the zip (e.g. to `C:\platform-tools`).
3. Add that folder to your **PATH**:
   - Start → search **Environment Variables**
   - **Path** → **Edit** → **New** → `C:\platform-tools` (your actual path)
   - OK, then **close and reopen** PowerShell.

Check:

```powershell
adb version
```

### 3. Get the script

**Option A — Git**

```powershell
git clone https://github.com/YOUR_USERNAME/android-xy.git
cd android-xy
```

**Option B — Manual**

Download `xy.py` into a folder, then:

```powershell
cd Downloads\android-xy
```

### 4. Run

```powershell
python xy.py
```

Tap the phone; coordinates appear in the terminal.

### 5. Optional flags (Windows)

```powershell
python xy.py --overlay-on
python xy.py --overlay-off
python xy.py --live
python xy.py -s SERIAL
```

### Windows troubleshooting

| Problem | Fix |
|---------|-----|
| `adb` is not recognized | Platform-tools not on PATH; reopen terminal after editing PATH. |
| `python` is not recognized | Reinstall Python with “Add to PATH”, or use `py xy.py`. |
| Phone shows as `unauthorized` | Unlock phone, revoke USB debugging authorizations in Developer options, replug and allow again. |
| No device | Install OEM USB driver (Samsung, Xiaomi, etc.) if Windows does not see the phone. |
| Script stops immediately | Run PowerShell as normal user in the folder that contains `xy.py`. |

---

## Using the coordinates

Each tap prints:

```text
tap [360, 1850]
```

Use **`[360, 1850]`** as X and Y in:

- MacroDroid → UI Interaction → Click → coordinates  
- Tasker → Tap → coordinates  
- Your own automation scripts  

**Tip:** Run `python xy.py` (or `python3` on Mac) once per button: inbox, search, send, etc. Write each pair down or paste into your macro config.

---

## On-screen overlay (all platforms)

Show X,Y **on the phone** (Android’s pointer location):

```bash
python xy.py --overlay-on
```

Turn off:

```bash
python xy.py --overlay-off
```

---

## Quick reference

| Task | Command |
|------|---------|
| Print tap position | `python xy.py` |
| Live drag position | `python xy.py --live` |
| Overlay on phone | `python xy.py --overlay-on` |
| Multiple phones | `adb devices` then `python xy.py -s SERIAL` |
| List devices | `adb devices` |

---

## License

MIT — use and modify freely.
