@ECHO off

SET LocalSettings_File=LocalSettings.php
SET LocalSettings_File_Edited=LocalSettings.edited.php

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
    ECHO.
    ECHO # Use existing MediaWiki logo
    ECHO $wgLogos = [
    ECHO     "1x" =^> "$wgResourceBasePath/resources/assets/change-your-logo.svg",
    ECHO     "icon" =^> "$wgResourceBasePath/resources/assets/change-your-logo.svg",
    ECHO ];
) >> %LocalSettings_File_Edited%


REM Create .htaccess file
ECHO Creating .htaccess file...
ECHO RewriteEngine On > .htaccess
ECHO RewriteRule ^^wiki/^(.*^)$ /w/index.php/$1 [L] >> .htaccess
ECHO.
