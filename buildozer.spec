[app]

# App information
title = AI HUB
package.name = aihub
package.domain = org.belachew

# Source files
source.dir = .
source.include_exts = py,png,jpg,kv

# Version
version = 1.0

# Requirements
requirements = python3,kivy,pyjnius

# Orientation
orientation = portrait

# App icon
icon.filename = icons/appicon.png

# Screen mode
fullscreen = 0


# Android settings
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

# Permissions (important for internet apps)
android.permissions = INTERNET


[buildozer]

# Log level
log_level = 2

# Warn if running as root
warn_on_root = 1
