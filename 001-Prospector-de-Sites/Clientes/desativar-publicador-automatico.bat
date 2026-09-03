@echo off
title Prospector de Sites - desativar publicador automatico
echo.
echo  Removendo a tarefa agendada "ProspectorPublicador" (a que subia sozinho a cada 1 min)...
schtasks /Delete /TN ProspectorPublicador /F
echo.
echo  Pronto. A partir de agora NADA sobe sozinho.
echo  Para publicar, rode o "publicar-agora.bat" quando quiser.
echo.
pause
