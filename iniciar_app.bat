@echo off
cd %~dp0
echo Executando o aplicativo STATUS JUSGESTANTE...
echo.

REM Método 1: Executar diretamente o streamlit
echo Tentando executar o Streamlit diretamente...
"%LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts\streamlit.exe" run status_jusgestante.py

REM Se o método 1 falhar, use o método 2: PowerShell
if %ERRORLEVEL% NEQ 0 (
    echo Tentando executar via PowerShell...
    powershell -ExecutionPolicy Bypass -File "%~dp0\executar_status.ps1"
)

echo.
echo Se o navegador não abrir automaticamente, acesse http://localhost:8501
pause 