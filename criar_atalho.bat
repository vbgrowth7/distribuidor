@echo off
cd %~dp0
echo Criando atalho na área de trabalho...
powershell -ExecutionPolicy Bypass -File "%~dp0\criar_atalho.ps1" 