import sys
import os
import logging
import subprocess
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==========================================
# DETECTION: WAYLAND vs X11 + VULKAN
# ==========================================

def detect_display_server():
    """Detect if running on Wayland or X11"""
    if os.environ.get("WAYLAND_DISPLAY"):
        return "wayland"
    elif os.environ.get("DISPLAY"):
        return "x11"
    else:
        # Try to detect from session
        session = os.environ.get("XDG_SESSION_TYPE", "").lower()
        if "wayland" in session:
            return "wayland"
        else:
            return "x11"

def detect_gpu_driver():
    """Detect GPU driver for optimal Vulkan setup"""
    try:
        # Check for Intel GPU
        if os.path.exists("/sys/class/drm/card0/device/driver"):
            with open("/sys/class/drm/card0/device/driver") as f:
                driver = f.read()
                if "i915" in driver or "intel" in driver:
                    return "intel"
                elif "amdgpu" in driver or "amd" in driver:
                    return "amd"
    except:
        pass
    
    # Fallback to lspci
    try:
        lspci = subprocess.run(["lspci"], capture_output=True, text=True)
        if "Intel" in lspci.stdout:
            return "intel"
        elif "AMD" in lspci.stdout:
            return "amd"
        elif "NVIDIA" in lspci.stdout:
            return "nvidia"
    except:
        pass
    
    return "generic"

def detect_kernel_version():
    """Detect kernel version"""
    try:
        kernel_version = os.uname().release
        if "lts" in kernel_version.lower():
            return "lts"
        else:
            return "standard"
    except:
        return "unknown"

# Get system info
DISPLAY_SERVER = detect_display_server()
GPU_DRIVER = detect_gpu_driver()
KERNEL_TYPE = detect_kernel_version()

logger.info(f"Display Server: {DISPLAY_SERVER.upper()}")
logger.info(f"GPU Driver: {GPU_DRIVER.upper()}")
logger.info(f"Kernel Type: {KERNEL_TYPE.upper()}")

# ==========================================
# ENVIRONMENT SETUP - WAYLAND/X11 COMPATIBLE
# ==========================================

# Core QT settings - WAYLAND/X11 compatible
os.environ["QT_QPA_PLATFORM_PLUGIN

