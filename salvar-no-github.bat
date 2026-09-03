@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   Salvar workspace no GitHub (MDG-Digital)
echo ============================================
echo.

REM Verifica se e um repositorio git
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Esta pasta nao e um repositorio git.
    echo.
    pause
    exit /b 1
)

REM Monta a mensagem do commit: usa o que foi digitado ou data/hora
set "MSG=%*"
if "%MSG%"=="" (
    set "MSG=Atualizacao %date% %time%"
)

echo Mensagem do commit: !MSG!
echo.

echo [1/3] Adicionando arquivos...
git add -A
if errorlevel 1 goto erro

REM Se nao houver mudancas, avisa e sai sem erro
git diff --cached --quiet
if not errorlevel 1 (
    echo.
    echo Nenhuma mudanca para salvar. Tudo ja esta atualizado.
    echo.
    pause
    exit /b 0
)

echo [2/3] Criando commit...
git commit -m "!MSG!"
if errorlevel 1 goto erro

echo [3/3] Enviando para o GitHub...
git push
if errorlevel 1 goto erro

echo.
echo ============================================
echo   Concluido! Alteracoes salvas no GitHub.
echo ============================================
echo.
pause
exit /b 0

:erro
echo.
echo [ERRO] Algo falhou. Confira as mensagens acima.
echo.
pause
exit /b 1
