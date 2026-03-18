from PyQt6.QtWebEngineCore import QWebEngineSettings

# --- Add this to your MainWindow __init__ ---

# 1. User Agent Switcher
self.ua_selector = QComboBox()
self.ua_map = {
    "Default": self.profile.httpUserAgent(),
    "Windows/Chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "iPhone/Safari": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Android/Pixel": "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
}
self.ua_selector.addItems(self.ua_map.keys())
self.ua_selector.currentIndexChanged.connect(self.change_user_agent)
self.navbar.addWidget(self.ua_selector)

# 2. HTML Settings Toggles
self.js_toggle = QCheckBox("JS")
self.js_toggle.setChecked(True)
self.js_toggle.stateChanged.connect(self.update_html_settings)
self.navbar.addWidget(self.js_toggle)

self.img_toggle = QCheckBox("IMG")
self.img_toggle.setChecked(True)
self.img_toggle.stateChanged.connect(self.update_html_settings)
self.navbar.addWidget(self.img_toggle)

# --- New Methods inside BotHunterBrowser class ---

def change_user_agent(self):
    label = self.ua_selector.currentText()
    new_ua = self.ua_map[label]
    # This changes it for the WHOLE profile (all tabs)
    self.profile.setHttpUserAgent(new_ua)
    self.tabs.currentWidget().reload()

def update_html_settings(self):
    # Get the settings object for the current profile
    settings = self.profile.settings()
    
    # Toggle JavaScript
    settings.setAttribute(
        QWebEngineSettings.WebAttribute.JavascriptEnabled, 
        self.js_toggle.isChecked()
    )
    
    # Toggle Auto-loading Images
    settings.setAttribute(
        QWebEngineSettings.WebAttribute.AutoLoadImages, 
        self.img_toggle.isChecked()
    )
    
    # Reload to apply
    self.tabs.currentWidget().reload()
