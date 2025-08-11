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


SET LocalSettings_File="LocalSettings.php"
SET LocalSettings_File_Edited="LocalSettings.edited.php"

REM Check if LocalSettings.php exists
if NOT EXIST %LocalSettings_File% (
    ECHO ERROR: %LocalSettings_File% not found in current directory.
    ECHO Please download it from the MediaWiki setup wizard first.
    PAUSE
    exit /b 1
)

REM Create a working copy of LocalSettings.php
ECHO Creating working copy of %LocalSettings_File% ...
COPY %LocalSettings_File% %LocalSettings_File_Edited%
ECHO.


REM Modify the LocalSettings.edited.php for short URLs
ECHO Modifying %LocalSettings_File_Edited% for short URLs...
(
    ECHO.
    ECHO # Short URL configuration
    ECHO $wgScriptPath = "/w";
    ECHO $wgResourceBasePath = $wgScriptPath;
    ECHO $wgArticlePath = "/wiki/$1";
    ECHO $wgUsePathInfo = true;
) >> %LocalSettings_File_Edited%
ECHO.


REM Create .htaccess file, using escaped dollar sign with `$$`
ECHO Creating .htaccess file...
ECHO RewriteEngine On > .htaccess
ECHO RewriteRule ^^wiki/^(.*^)$ /w/index.php/$1 [L] >> .htaccess
ECHO.

REM Move MediaWiki files to /w directory in container
ECHO Moving MediaWiki files to /w subdirectory...
docker exec mediawiki mkdir -p /var/www/html/w
docker exec mediawiki sh -c "mv /var/www/html/* /var/www/html/w/ 2>/dev/null || true"
ECHO.

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
