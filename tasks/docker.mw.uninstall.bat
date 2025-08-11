@ECHO off

ECHO MediaWiki Docker Cleanup
ECHO =========================
ECHO.
ECHO This will stop and remove MediaWiki containers.
ECHO.
SET /p confirm="Are you sure? (y/N): "
if /i not "%confirm%"=="y" (
    ECHO Cancelled.
    PAUSE
    exit /b 0
)
ECHO.

ECHO Stopping containers...
docker stop mediawiki 2>NUL
docker stop mediawiki-db 2>NUL
ECHO.

ECHO Removing containers...
docker rm mediawiki 2>NUL
docker rm mediawiki-db 2>NUL
ECHO.
