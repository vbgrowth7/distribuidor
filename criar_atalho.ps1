# Criar atalho para o aplicativo STATUS JUSGESTANTE na área de trabalho
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\STATUS JUSGESTANTE.lnk")
$Shortcut.TargetPath = "$env:LOCALAPPDATA\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts\streamlit.exe"
$Shortcut.Arguments = "run `"$PSScriptRoot\status_jusgestante.py`""
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.IconLocation = "$env:SystemRoot\System32\SHELL32.dll,27"
$Shortcut.Description = "Aplicativo STATUS JUSGESTANTE"
$Shortcut.Save()

Write-Host "Atalho 'STATUS JUSGESTANTE' criado na área de trabalho!" -ForegroundColor Green
Write-Host "Agora você pode iniciar o aplicativo com um duplo clique." -ForegroundColor Yellow
Write-Host "Pressione qualquer tecla para sair..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 