@echo off
cd %~dp0
echo Executando o Status JUSGESTANTE...
"%LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts\streamlit.exe" run status_jusgestante.py
echo.
echo Se o navegador não abrir automaticamente, acesse http://localhost:8501
pause 