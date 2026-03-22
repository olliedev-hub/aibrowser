import sys
import os
import logging
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==========================================
# VULKAN OPTIMIZATION FOR CHROMEBOOK + ARCH LINUX LTS
# ==========================================

# Enable Vulkan for maximum performance on LTS kernel
os.environ["QT_QUICK_BACKEND"] = "vulkan"
os.environ["QT_XCB_GL_INTEGRATION"] = "xcb_egl"

# Comprehensive Vulkan + Chrome flags for LTS kernel
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    # Vulkan primary settings
    "--enable-features=Vulkan,VulkanFromANGLE,VulkanExtensionDynamicRendering,SkiaGraphite,SkiaUseGanesh "
    "--use-vulkan=native "
    
    # GPU acceleration
    "--enable-gpu-rasterization "
    "--enable-native-gpu-memory-buffers "
    "--ignore-gpu-blocklist "
    "--disable-gpu-sandbox "
    "--enable-gpu-compositing "
    
    # Performance tuning for LTS kernel
    "--disable-software-rasterizer "
    "--disable-sync "
    "--enable-fast-unzip "
    "--enable-preconnect "
    
    # Chromebook-specific optimizations
    "--enable-low-res-tiling "
    "--enable-tcp-fast-open "
    "--enable-parallel-downloading "
    
    # Memory optimization for limited Chromebook RAM
    "--memory-pressure-off "
    "--disable-preconnect "
    "--enable-aggressive-domstorage-flushing "
)

# Linux-specific Vulkan settings
if sys.platform.startswith("linux"):
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
    os.environ["VK_ICD_FILENAMES"] = "/usr/share/vulkan/icd.d/intel_icd.x86_64.json:/usr/share/vulkan/icd.d/amd_icd64.json"
    os.environ["MESA_VK_DEVICE_SELECT"] = "0"
    os.environ["VKCUBE_QUEUE

