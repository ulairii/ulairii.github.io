---
title: "Building CARLA (v0.9.15) from Source on Windows 11 with Visual Studio 2022: My Personal Guide & Tips"
date: 2026-02-20
permalink: /posts/2026/02/carla-install-windows11/
tags:
  - autonomous driving
  - tools tutorials
---

Building [CARLA](https://carla.org/) from source on Windows is notoriously painful — outdated guides, cryptic errors, and hours of compilation. This post is based on [this excellent guide by wambitz](https://wambitz.github.io/tech-blog/carla/python/c++/simulation/autonomous-vehicles/2024/09/29/carla-win11.html), combined with my own personal experience, additional fixes, and troubleshooting tips for issues I ran into that weren't covered elsewhere.

> **Credit:** Original guide by [wambitz](https://wambitz.github.io/tech-blog/). I'm reposting the key steps here and layering in my own notes.

---

## Table of Contents

1. [Why This Guide?](#why-this-guide)
2. [Prerequisites](#prerequisites)
3. [Setting Up the Environment](#setting-up-the-environment)
4. [Build Unreal Engine 4 for CARLA](#build-unreal-engine-4-for-carla)
5. [Building CARLA from Source](#building-carla-from-source)
6. [Launching the CARLA Simulator](#launching-the-carla-simulator)
7. [Running the CARLA Client](#running-the-carla-client)
8. [My Personal Tips & Fixes](#my-personal-tips--fixes)

---

## Why This Guide?

- **Up-to-Date:** Tailored for CARLA v0.9.15, Windows 11, and Visual Studio 2022.
- **Time-Saving:** Avoid pitfalls that cost me hours or days.
- **Personal Fixes:** Includes troubleshooting for real errors I hit beyond the original guide.

---

## Prerequisites

### System Requirements

> **NOTE:** The build can take **5+ hours** on the reference hardware below.

| Component  | Requirement |
|------------|-------------|
| OS         | 64-bit Windows 10 or 11 |
| CPU        | Quad-core Intel or AMD, 2.5 GHz or faster |
| RAM        | 32 GB (recommended) |
| GPU        | Dedicated GPU with ≥ 6 GB VRAM (8 GB recommended) |
| Disk Space | ~165 GB total (CARLA ~32 GB + UE4 ~133 GB) |
| TCP Ports  | 2000 and 2001 must be open |

### Software Requirements

> **IMPORTANT:** If you have multiple Python versions installed, make sure **Python 3.8** is first in your PATH. Python 3.10 will not work. **Do NOT use a virtual environment** for building the CARLA package.

Required tools:

| Tool | Version / Notes |
|------|-----------------|
| Git | Latest |
| CMake | **>= 3.15 and < 3.50** — e.g., [3.28.6](https://cmake.org/files/v3.28/) is safe |
| Make | **3.81 strictly** |
| 7-Zip | Latest |
| Python | **3.8 (64-bit only)** |
| Visual Studio | **2022** (Community Edition is sufficient) |
| Unreal Engine | **4.26 CARLA fork** (see below) |

> ⚠️ **CMake Version Warning:** Use CMake **>= 3.15** but **< 3.50**. CMake 3.50+ removed backward compatibility that CARLA's build scripts rely on and will cause cryptic errors later. Download older releases from [cmake.org/files](https://cmake.org/files/).

Ensure all tools are added to your system **PATH**.

### Python Dependencies

```bat
pip install --upgrade pip
pip install --user setuptools
pip install --user wheel
```

---

## Setting Up the Environment

### Install Dependencies

**Git** — verify:
```bat
git --version
```

**CMake** (must be >= 3.15 and < 3.50):
```bat
cmake --version
rem Must show >= 3.15 and < 3.50
```

**Make** via Chocolatey (requires admin):
```bat
choco install make
make --version
```

**7-Zip** — download from [7-zip.org](https://www.7-zip.org/).

**Python 3.8 (64-bit)** — download from [python.org](https://www.python.org/downloads/release/python-380/). Add to PATH during installation:
```bat
python --version
pip --version
```

### Install Visual Studio 2022

> **IMPORTANT:** Do not have multiple Visual Studio versions installed simultaneously — even uninstalled remnants can cause conflicts.

Download [Visual Studio 2022](https://visualstudio.microsoft.com/vs/) and select:

**Workloads:**
- Desktop Development with C++
- .NET Desktop Development

**Individual Components:**
- Windows 10 SDK (use the latest Windows 10 SDK even on Windows 11)
- C++ CMake Tools for Windows

Complete installation and **restart your computer**.

---

## Build Unreal Engine 4 for CARLA

> **NOTE:** You need your GitHub account linked to your Epic Games account to access the CARLA UE4 fork. Follow [these instructions](https://www.unrealengine.com/en-US/ue-on-github).

> **Keep the path short** (e.g., `C:\CarlaUE4`). Long paths cause errors in `Setup.bat`.

```bat
git clone --depth 1 -b carla https://github.com/CarlaUnreal/UnrealEngine.git CarlaUE4
cd CarlaUE4
```

Run the setup scripts:

> **NOTE:** If a Windows pop-up about an incompatible framework appears, select **Download**.

```bat
Setup.bat
GenerateProjectFiles.bat
```

### Compile the Engine

> **NOTE:** This step takes **several hours** (5+ hours on the reference machine).

1. Open `UE4.sln` in `C:\CarlaUE4` with Visual Studio 2022.
2. Set **Configuration:** `Development Editor` and **Platform:** `Win64`.
3. In Solution Explorer, right-click **UE4** → **Build**.
4. After the build, verify by running `Engine\Binaries\Win64\UE4Editor.exe`.

---

## Building CARLA from Source

### Clone the CARLA Repository

```bat
git clone https://github.com/carla-simulator/carla.git -b 0.9.15 carla-0.9.15
cd carla-0.9.15
```

### Download Assets

> **NOTE:** If assets are missing at runtime, `make launch-only` will crash with a segmentation fault.

Before running `Update.bat`, you must apply **two patches** to fix known bugs in the script:

**Patch 1 — Fix the broken download URL**

The original S3 URL is dead for CARLA 0.9.15 (asset ID `20231108_c5101a5`). Open `C:\carla-0.9.15\Update.bat` and replace:

```bat
set CONTENT_LINK=http://carla-assets.s3.amazonaws.com/%CONTENT_ID%.tar.gz
```

with:

```bat
set CONTENT_LINK=https://carla-assets.s3.us-east-005.backblazeb2.com/%CONTENT_ID%.tar.gz
```

**Patch 2 — Fix the 7-Zip command path**

`Update.bat` calls `7zip`, but the actual executable is `7z.exe`. Without this fix, extraction falls back to PowerShell's `Expand-Archive`, which does not support `.tar.gz` and will throw:

```
Expand-Archive : .gz is not a supported archive file format.
```

Find the line calling `7zip x ...` and replace `7zip` with the full path:

```bat
"C:\Program Files (x86)\7-Zip\7z.exe" x ...
```

> If you installed 7-Zip elsewhere, adjust the path accordingly. Alternatively, add `C:\Program Files (x86)\7-Zip` to your system PATH so that `7z` is recognized globally.

After applying both patches, run:

```bat
Update.bat
```

### Install Python Packages

> **IMPORTANT:** Do NOT compile CARLA inside a virtual environment — this triggers a `B2.EXE` error. Use Python 3.8 system-wide.

```bat
python --version
rem Must output: Python 3.8.XX

pip install wheel
pip list
pip --version
```

### Compile the Python API

> **NOTES:**
> - The build defaults to Visual Studio 2019. Since we're on VS 2022, we must specify the generator explicitly.
> - Python 3.8 must be the top version in your system PATH.
> - This takes around **30 minutes**.

> ❗ **You CANNOT run this in a regular `cmd` or PowerShell terminal.** You must use the **x64 Native Tools Command Prompt for VS 2022**, which sets up the correct compiler environment variables. Running in a regular terminal causes cryptic build failures.
>
> **How to open it:** Start menu → type `x64` → select **"x64 Native Tools Command Prompt for VS 2022"**

```bat
cd C:\carla-0.9.15
make PythonAPI GENERATOR="Visual Studio 17 2022"
```

---

### 🔧 Troubleshooting: Boost Linker Error (Wrong MSVC Toolset)

> ⚠️ **Error:**
> ```
> LINK : fatal error LNK1104: cannot open file 'libboost_filesystem-vc142-mt-x64-1_80.lib'
> ```

**Cause:** Boost was compiled with MSVC 14.2 (VS 2019) but you're using MSVC 14.3 (VS 2022).

**Fix:** Delete the existing Boost build and reinstall with the correct toolset:

```bat
rem Delete the current Boost installation
rm -r .\Build\boost-1.80.0-install\

rem Reinstall with the correct toolset (-j 32 = parallel jobs, adjust to your CPU)
.\Util\InstallersWin\install_boost.bat --build-dir "C:\carla-0.9.15\Build\" --toolset msvc-14.3 --version 1.80.0 -j 32

rem Rebuild the Python API
make PythonAPI GENERATOR="Visual Studio 17 2022"
```

---

### 🔧 Troubleshooting: `b2.exe` Boost Build Error (Toolset Mismatch in Scripts)

> ⚠️ **Error:**
> ```
> -[install_boost]: [B2 ERROR] An error ocurred while installing using "b2.exe".
> ```

**Cause:** Boost 1.80's `bootstrap.bat` auto-detects `vc143`, but CARLA's build scripts hardcode `vc141`/`vc142` in two places.

**Fix:** Update the toolset to `vc143` in two files:

1. `Util\BuildTools\Windows.mk` — around **line 75**, change `vc141` or `vc142` to `vc143`.
2. `Util\InstallersWin\install_boost.bat` — around **line 109**, change the same.

Then retry:

```bat
make PythonAPI GENERATOR="Visual Studio 17 2022"
```

> *Credit: fix originally identified by [ThibaultFy](https://github.com/carla-simulator/carla/issues/21) (Aug 2021).*

---

### 🔧 Troubleshooting: zlib Download Failure (Broken URL)

> ⚠️ **Error:**
> ```
> [install_zlib]: Retrieving zlib.
> Exception calling "DownloadFile" ... (404) Not Found.
> [install_zlib]: [CMAKE ERROR] An error ocurred while executing cmake command.
> ```

**Cause:** `zlib.net` no longer hosts the file; the backup URL returns a `301` redirect that PowerShell's `WebClient` won't follow.

**Fix:** Open `C:\carla-0.9.15\Util\InstallersWin\install_zlib.bat`, find the line with `ZLIB_REPO` (containing `zlib.net`) and replace it with:

```bat
set ZLIB_REPO=https://github.com/madler/zlib/archive/refs/tags/v%ZLIB_VERSION%.zip
```

Clean up the half-created folders and retry:

```bat
rmdir /s /q Build\zlib-source
rmdir /s /q Build\zlib-install
del /q Build\zlib-1.2.13.zip

make PythonAPI GENERATOR="Visual Studio 17 2022"
```

---

### 🔧 Troubleshooting: CMake Too New (Compatibility Error)

> ⚠️ **Error:**
> ```
> Compatibility with CMake < 3.5 has been removed from CMake.
> [install_zlib]: [CMAKE ERROR] An error ocurred while executing cmake command.
> ```

**Cause:** CMake ≥ 3.50 dropped backward compatibility that CARLA's `CMakeLists.txt` requires.

**Fix:** Downgrade to CMake **>= 3.15 and < 3.50** (e.g., [3.28.6](https://cmake.org/files/v3.28/)). Verify after installing:

```bat
cmake --version
rem Must show >= 3.15 and < 3.50
```

Then clean up and retry `make PythonAPI` as above.

---

### Compile the CARLA Server

> **NOTE:** This step takes **2+ hours**.

```bat
make CarlaUE4Editor GENERATOR="Visual Studio 17 2022"
```

Output files will be created at: `C:\carla-0.9.15\PythonAPI\carla\dist`

---

### 🔧 Troubleshooting: OSM2ODR CMake "x64" Path Error

> ⚠️ **Error:**
> ```
> CMake Error: The source directory ".../Build/osm2odr-visualstudio/x64" does not exist.
> Ignoring extra path from command line: "...\Build\om2odr-source""
> ```

**Cause:** The script passes `x64` as a positional argument instead of an architecture flag, so CMake misinterprets it as the source directory.

**Fix:** Open `C:\carla-0.9.15\Util\BuildTools\BuildOSM2ODR.bat`, find the CMake configure line containing `-G %GENERATOR% %PLATFORM%`, and change `%PLATFORM%` to `-A x64`:

```bat
cmake -G %GENERATOR% -A x64^
```

Clean the broken dirs and retry:

```bat
rmdir /s /q Build\osm2odr-visualstudio
rmdir /s /q Build\osm2odr-source
rmdir /s /q Build\om2odr-source

make PythonAPI GENERATOR="Visual Studio 17 2022"
```

---

### 🔧 Troubleshooting: "Unreal Engine Not Detected" / `UE4_ROOT` Not Set

> ⚠️ **Error:**
> ```
> ERROR: The system was unable to find the specified registry key or value.
> -[BuildCarlaUE4]: [ERROR] Unreal Engine not detected
> ```

**Cause:** CARLA checks the `UE4_ROOT` environment variable first, then falls back to the Windows registry — which usually doesn't exist.

**Fix:** Set `UE4_ROOT` to wherever **you** cloned the CARLA UE4 fork. This path varies per user — the examples below use `C:\CarlaUE4`, but substitute your actual install location:

```bat
rem For the current session only
set UE4_ROOT=C:\CarlaUE4

rem To persist across all terminals (run once)
setx UE4_ROOT "C:\CarlaUE4"
```

If you cloned UE4 to a different drive, e.g. `D:\UnrealEngine\CarlaUE4`:

```bat
setx UE4_ROOT "D:\UnrealEngine\CarlaUE4"
```

Verify it's correct (`UE4Editor.exe` should be listed):

```bat
echo %UE4_ROOT%
dir "%UE4_ROOT%\Engine\Binaries\Win64\UE4Editor.exe"
```

> **`UE4_ROOT` must point to the root folder** (the one containing `Engine\`), **not** to `Engine\Binaries\Win64` itself.

> **Haven't built UE4 yet?** Go back to the [Build Unreal Engine 4 for CARLA](#build-unreal-engine-4-for-carla) section. The CARLA-specific fork (`-b carla`) must be fully compiled before this step will succeed.

---

## Launching the CARLA Simulator

### Change the Default Map (Optional)

By default, CARLA loads `Town10HD_Opt`, which is large and resource-intensive. To switch to a lighter map like `Town02`, edit `Unreal\CarlaUE4\Config\DefaultEngine.ini`:

```ini
[/Script/EngineSettings.GameMapsSettings]
EditorStartupMap=/Game/Carla/Maps/Town02.Town02
GameDefaultMap=/Game/Carla/Maps/Town02.Town02
ServerDefaultMap=/Game/Carla/Maps/Town02.Town02
GlobalDefaultGameMode=/Game/Carla/Blueprints/Game/CarlaGameMode.CarlaGameMode_C
GameInstanceClass=/Script/Carla.CarlaGameInstance
TransitionMap=/Game/Carla/Maps/Town02.Town02
GlobalDefaultServerGameMode=/Game/Carla/Blueprints/Game/CarlaGameMode.CarlaGameMode_C
```

### Launch the CARLA Server

> **NOTE:** The first launch is slow. On my machine it took ~20 min to open the Editor and ~30 min more for shader compilation. Subsequent launches are much faster thanks to caching.

```bat
make launch-only
```

Click **Play** in the Unreal Editor to start the simulation. Use **WASD** + mouse to move around.

---

## Running the CARLA Client

### Create a Python Virtual Environment

> **IMPORTANT:** Do NOT create a virtual environment until the **full build is complete**. Use Python 3.8.

```bat
py -3.8 -m venv .venv
.\.venv\Scripts\activate
```

### Install the CARLA Package

```bat
cd C:\carla-0.9.15\PythonAPI\carla\dist
pip install .\carla-0.9.15-cp38-cp38-win_amd64.whl
```

### Install Example Script Dependencies

```bat
cd C:\carla-0.9.15\PythonAPI\examples
pip install -r requirements.txt
```

### Start the Traffic Simulation

> **NOTE:** Ensure the CARLA server is running before executing client scripts.

```bat
python generate_traffic.py
```

You should now see traffic in the simulation.

---

## My Personal Tips & Fixes

*I will continue updating this section with additional workarounds and lessons learned beyond the issues already documented above.*

<!-- TODO: Add personal tips here -->

---

## Conclusion

You've now built and launched CARLA on Windows 11 using Visual Studio 2022. Whether you're using it for research, development, or experimentation, CARLA is a powerful platform for autonomous driving simulation. Good luck, and feel free to reach out if you hit issues not covered here!

---

## Additional Resources

| Resource | Link |
|----------|------|
| Official CARLA Docs | [carla.readthedocs.io](https://carla.readthedocs.io/) |
| CARLA GitHub | [carla-simulator/carla](https://github.com/carla-simulator/carla) |
| Unreal Engine on GitHub | [unrealengine.com/ue-on-github](https://www.unrealengine.com/en-US/ue-on-github) |
| CARLA Forum | [github.com/carla-simulator/carla/discussions](https://github.com/carla-simulator/carla/discussions) |
| Python 3.8 Downloads | [python.org](https://www.python.org/downloads/release/python-380/) |
| Visual Studio 2022 | [visualstudio.microsoft.com](https://visualstudio.microsoft.com/vs/) |
| CMake 3.28 (recommended) | [cmake.org/files/v3.28](https://cmake.org/files/v3.28/) |
| Original Guide by wambitz | [wambitz.github.io](https://wambitz.github.io/tech-blog/carla/python/c++/simulation/autonomous-vehicles/2024/09/29/carla-win11.html) |
