# Docker

### Initial Setup
Check the Docker version in use.
```shell
docker --version
```

Start the My SQL database container.
```shell
# Start database first
docker run -d --name mediawiki-db -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=mediawiki mysql:8.0
```

Start the MediaWiki container.
```shell
# Wait a few seconds for database to initialize, then start MediaWiki
docker run -d --name mediawiki -p 8080:80 --link mediawiki-db:mysql mediawiki
```

### MediaWiki Setup
Navigate to http://localhost:8080 and run the setup wizard on-site.
Download the `LocalSettings.php` file at the end of the on-site setup wizard.

#### Wizard
MediaWiki needs initial configuration.
Click **"Please set up the wiki first"** to run the setup wizard.

**Language Selection:**
- Choose English as the language.

**Environment Check:**
- MediaWiki will verify everything is working. Some warnings can be ignored.

**Database Configuration:**
- **Database type:** MySQL
- **Database host:** `mysql` (this connects to the database container)
- **Database name:** `mediawiki`
- **Database username:** `root`
- **Database password:** `root`

**Wiki Configuration:**
- **Wiki name:** `Starfield Wiki`
- **Admin username:** `Admin`
- **Admin password:** `default123`

**Complete Setup:**
- MediaWiki will create the configuration
- Download the `LocalSettings.php` file when prompted


#### Edit `LocalSettings.php`
Open `LocalSettings.php` locally and apply changes for the *script path* and *short url* for the wiki.

```shell
$wgScriptPath = "/w";
$wgArticlePath = "/wiki/$1";
$wgUsePathInfo = true;
```

#### Create `.htaccess`
Create and open the `.htaccess` file locally with the following content.
```apache
RewriteEngine On
RewriteRule ^wiki/(.*)$ /w/index.php/$1 [L]
```

#### Docker Files
Move all the MediaWiki Docker container *files and folders* in `/var/www/html/*` to `/var/www/html/w/*`.

Copy the `.htaccess` file into the MediaWiki Docker container at `/var/www/html/.htaccess`.
```shell
docker cp .htaccess mediawiki:/var/www/html/.htaccess
```

Copy the `LocalSettings.php` file into the MediaWiki Docker container at `/var/www/html/w/LocalSettings.php`.
```shell
docker cp LocalSettings.php mediawiki:/var/www/html/w/LocalSettings.php
```

Restart the MediaWiki Docker container.
```shell
docker restart mediawiki
```
