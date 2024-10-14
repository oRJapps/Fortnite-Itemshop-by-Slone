@echo off
setlocal enabledelayedexpansion

REM Pythonスクリプトの実行
python fortnite_shop_scraper_v2.py

REM 画像グリッドの作成
python create_adaptive_image_grid.py

echo フォートナイトショップの情報を取得し、画像グリッドを作成しました。

pause
