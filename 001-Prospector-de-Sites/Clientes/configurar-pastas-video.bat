@echo off
REM Marca todas as pastas "video" das oficinas como tipo VIDEOS (coluna Comprimento em Detalhes)
setlocal enabledelayedexpansion
cd /d "%~dp0"
set "N=0"
for /d %%O in ("sites\bh\oficinas\*") do (
  if exist "%%O\video" (
    set "V=%%O\video"
    > "!V!\desktop.ini" echo [.ShellClassInfo]
    >> "!V!\desktop.ini" echo FolderType=Videos
    attrib +s "!V!" >nul 2>&1
    attrib +s +h "!V!\desktop.ini" >nul 2>&1
    set /a N+=1
    echo   [OK] !V!
  )
)
echo.
echo Pronto: !N! pasta(s) marcada(s) como VIDEOS.
echo Feche e reabra as pastas no Explorer para ver a coluna "Comprimento".
echo Dica: ajuste UMA pasta em Detalhes com as colunas desejadas e use
echo   Opcoes de Pasta ^> Exibir ^> "Aplicar as Pastas" para padronizar todas.
pause
