@echo off
:: run.bat - Script simplificado para executar os bots RPA em diferentes ambientes

:: Exibe ajuda se solicitado
if "%1"=="-h" goto show_help
if "%1"=="--help" goto show_help

:: Configura variáveis padrão
set ENVIRONMENT=development
set BOT_NAME=

:: Processa os argumentos
if "%~2"=="" (
    :: Apenas um argumento - assume que é o nome do bot
    set BOT_NAME=%~1
) else (
    :: Dois argumentos - ambiente e nome do bot
    if "%~1"=="prd" (
        set ENVIRONMENT=production
    ) else if "%~1"=="dev" (
        set ENVIRONMENT=development
    ) else (
        echo Erro: Ambiente invalido. Use 'dev' ou 'prd'.
        exit /b 1
    )
    set BOT_NAME=%~2
)

:: Verifica se o diretório do bot existe
if not exist "src\bots\%BOT_NAME%" (
    echo Erro: Bot '%BOT_NAME%' nao encontrado em src\bots\
    echo Bots disponiveis:
    dir /b src\bots\
    exit /b 1
)

:: Define variável de ambiente
set ENVIRONMENT=%ENVIRONMENT%

echo Executando %BOT_NAME% em ambiente de %ENVIRONMENT%...

:: Executa o bot
python -m src.bots.%BOT_NAME%.main
exit /b %ERRORLEVEL%

:show_help
echo Uso: run.bat [ambiente] ^<nome_do_bot^>
echo.
echo Ambientes:
echo   dev         Ambiente de desenvolvimento (padrao se omitido)
echo   prd         Ambiente de producao
echo.
echo Exemplo:
echo   run.bat prd bot1    # Executa bot1 em ambiente de producao
echo   run.bat dev bot2    # Executa bot2 em ambiente de desenvolvimento
echo   run.bat bot1        # Executa bot1 em ambiente de desenvolvimento (padrao)
exit /b 0