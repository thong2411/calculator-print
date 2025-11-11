[app]

# (str) Title của app
title = May Tinh

# (str) Package name (không dấu, chữ thường)
package.name = calculator

# (str) Package domain (ngược lại)
package.domain = org.calculator

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0

# (list) Application requirements
# QUAN TRỌNG: Chỉ python3 và kivy, KHÔNG thêm gì khác!
requirements = python3,kivy

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (màu nền khi mở app)
#android.presplash_color = #FFFFFF

# (string) Icon của app (nếu có file icon.png)
icon.filename = %(source.dir)s/icon_calcu.png

# (string) Presplash của app (nếu có file presplash.png)
presplash.filename = %(source.dir)s/icon_calcu.png

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android SDK version to use
android.sdk = 31

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (nếu muốn chỉ định)
#android.ndk_path =

# (str) Android SDK directory (nếu muốn chỉ định)
#android.sdk_path =

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (list) The Android archs to build for
# Tạo 2 APK: 1 cho chip 64-bit, 1 cho chip 32-bit
android.archs = arm64-v8a,armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup rules
#android.backup_rules =

# (str) The Android app theme, default is ok for Kivy-based app
android.theme = @android:style/Theme.NoTitleBar

# (list) Java classes to add as activities to the manifest.
#android.add_activities = com.example.ExampleActivity

# (str) OUYA Console category. Should be one of GAME or APP
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (bool) Enable AndroidX support
android.enable_androidx = True

# (list) Add Java .jar files to libs
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project
#android.add_src =

# (list) Android AAR archives to add
#android.add_aars =

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact storage, absolute or relative to spec file
#build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
#bin_dir = ./bin
