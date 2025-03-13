# Script PowerShell para executar o aplicativo STATUS JUSGESTANTE
Write-Host "Executando o aplicativo STATUS JUSGESTANTE..." -ForegroundColor Green
Set-Location -Path $PSScriptRoot
& "$env:LOCALAPPDATA\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts\streamlit.exe" run status_jusgestante.py
Write-Host "`nSe o navegador não abrir automaticamente, acesse http://localhost:8501" -ForegroundColor Yellow 