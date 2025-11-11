@echo off
echo Building AntibioticEnv System v1.1 (Windows, onefile)...
python -m pip install --upgrade pip
pip install pyinstaller pyqt6 pandas matplotlib openpyxl
pyinstaller --noconsole --onefile --windowed --icon=AntibioticEnvSystem.ico --name AntibioticEnvSystem main_gui.py
echo Done. Find EXE in dist\AntibioticEnvSystem.exe
pause
