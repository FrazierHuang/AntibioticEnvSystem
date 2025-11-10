# build_dmg.py
import dmgbuild
import os

APP_NAME = "AntibioticEnvSystem"
APP_PATH = f"dist/{APP_NAME}.app"
DMG_NAME = f"{APP_NAME}.dmg"

print(f"🚀 正在创建 {DMG_NAME} ...")

settings = {
    "volume_name": APP_NAME,
    "icon": "AntibioticEnvSystem.icns",
    "background": "builtin-arrow",  # 可改成 background.png
    "files": [APP_PATH],
    "symlinks": {"Applications": "/Applications"},
    "window_rect": ((100, 100), (540, 380)),
    "default_view": "icon-view",
    "icon_size": 96,
    "text_size": 12,
}

# ✅ 新版写法（显式传入 settings 参数）
dmgbuild.build_dmg(DMG_NAME, APP_NAME, settings=settings)

print(f"✅ DMG 打包完成：{DMG_NAME}")