@ECHO off

ECHO MediaWiki Post-Setup Configuration
ECHO ===================================
ECHO.

REM Check Docker is available
ECHO Checking Docker installation...
docker --version
if %errorlevel% neq 0 (
    ECHO ERROR: Docker is not installed or not in PATH
    PAUSE
    exit /b 1
)
ECHO.


REM Move MediaWiki files to /w directory in container
@REM TODO: If the /var/www/html/w already exists, then exit/skip copying
ECHO Moving MediaWiki files to /w subdirectory...
docker exec mediawiki mkdir -p /var/www/html/w
docker exec mediawiki sh -c "mv /var/www/html/* /var/www/html/w/ 2>/dev/null || true"
ECHO.


CALL tasks\docker.mw.setup.files
ECHO LocalSettings_File=%LocalSettings_File%
ECHO LocalSettings_File_Edited=%LocalSettings_File_Edited%


REM Copy files to container
ECHO Copying .htaccess to container...
docker cp .htaccess mediawiki:/var/www/html/.htaccess

ECHO Copying %LocalSettings_File_Edited% to container...
docker cp %LocalSettings_File_Edited% mediawiki:/var/www/html/w/LocalSettings.php
ECHO.

REM Restart MediaWiki container
ECHO Restarting MediaWiki container...
docker restart mediawiki
ECHO.

ECHO Waiting for MediaWiki to restart...
TIMEOUT /t 5 /nobreak
ECHO.

ECHO ===============================
ECHO Setup Complete!
ECHO ===============================
ECHO.
ECHO Your MediaWiki site should now be available at:
ECHO - Main site: http://localhost:8080/wiki/Main_Page
ECHO - Admin panel: http://localhost:8080/w/index.php/Special:SpecialPages
ECHO.
ECHO Admin credentials:
ECHO - Username: Admin
ECHO - Password: default123
ECHO.
