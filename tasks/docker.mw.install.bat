@ECHO off

ECHO MediaWiki Docker Setup Script
ECHO ===============================
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

REM Start MySQL database container
ECHO Starting MySQL database container...
docker run -d --name mediawiki-db -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=mediawiki mysql:8.0
if %errorlevel% neq 0 (
    ECHO ERROR: Failed to start database container
    ECHO This might be because the container already exists
    ECHO Run: docker rm mediawiki-db
    PAUSE
    exit /b 1
)
ECHO Database container started successfully
ECHO.

REM Wait for database to initialize
ECHO Waiting 10 seconds for database to initialize...
TIMEOUT /t 10 /nobreak
ECHO.

REM Start MediaWiki container
ECHO Starting MediaWiki container...
docker run -d --name mediawiki -p 8080:80 --link mediawiki-db:mysql mediawiki
if %errorlevel% neq 0 (
    ECHO ERROR: Failed to start MediaWiki container
    ECHO This might be because the container already exists
    ECHO Run: docker rm mediawiki
    PAUSE
    exit /b 1
)
ECHO MediaWiki container started successfully
ECHO.

REM Wait for MediaWiki to start
ECHO Waiting 10 seconds for MediaWiki to start...
TIMEOUT /t 10 /nobreak
ECHO.

ECHO ===============================
ECHO MANUAL STEPS REQUIRED:
ECHO ===============================
ECHO.
ECHO 1. Open browser and navigate to: http://localhost:8080
ECHO 2. Complete the setup wizard with these settings:
ECHO   Language
ECHO     - Your language: en-English
ECHO     - Wiki language: en-English
ECHO   Connect to database
ECHO     - Database type: MySQL
ECHO     - Database host: mysql
ECHO     - Database name: mediawiki
ECHO     - Database username: root
ECHO     - Database password: root
ECHO   Database settings
ECHO     - Use the same account as for installation: Yes
ECHO   Name
ECHO     - URL host name: http://localhost:8080
ECHO     - Name of wiki: Starfield Wiki
ECHO     - Project namespace: Same as the wiki name, 'Starfield_Wiki'
ECHO     - Admin username: Admin
ECHO     - Admin password: default123
ECHO   Options
ECHO     - User rights profile: Open wiki
ECHO     - Copyright and license: No license footer
ECHO     - Enable email authentication: No
ECHO     - Skins: All (Vector, use as default)
ECHO     - Enable file uploads: Yes
ECHO     - Directory for deleted files: (leave empty for default)
ECHO.
ECHO 3. Download LocalSettings.php when prompted.
ECHO 4. Run the post-setup script: tasks\docker.mw.setup.bat
ECHO.
ECHO Press any key when you have completed the wizard and downloaded LocalSettings.php...
PAUSE
