@echo off
set DIFICULDADE=4

:inicio_loop
cls
echo ======================================================
echo    FLYFOOD - ESCALADA DE DIFICULDADE
echo ======================================================
echo [*] Nivel atual: %DIFICULDADE% CIDADES
echo [Pressione Ctrl + C para parar]
echo --------------------------------------------------

python gerar_matriz.py %DIFICULDADE% > teste_auto.txt

python forca_bruta.py < teste_auto.txt > temp_resultado.txt

type temp_resultado.txt

echo ----- TESTE COM %DIFICULDADE% CIDADES ----- >> log_resultados_oficial.txt
type teste_auto.txt >> log_resultados_oficial.txt
echo [ RESULTADO ] >> log_resultados_oficial.txt
type temp_resultado.txt >> log_resultados_oficial.txt
echo ======================== >> log_resultados_oficial.txt
echo. >> log_resultados_oficial.txt

echo.
echo Concluido! Preparando o proximo nivel...
timeout /t 2 > nul

set /a DIFICULDADE=%DIFICULDADE%+1

if %DIFICULDADE% GTR 10 (
    set DIFICULDADE=4
    echo.
    echo Limite maximo atingido. Reiniciando a escalada...
    timeout /t 3 > nul
)

goto inicio_loop