Using Macports:

	sudo port install pgrouting

osm2pgrouting from [github](https://github.com/pgRouting/osm2pgrouting)

	cmake -H. -Bbuild
    cd build/
	make
	sudo make install

Create an empty DB

	createdb mydb
	psql mydb

Open psql and add extensions:

	psql -U postgres
	CREATE DATABASE routing;
	\c routing
	CREATE EXTENSION postgis;
	CREATE EXTENSION pgrouting;

Settings?

	/system/library/LaunchDaemons/org.postgresql.postgres_alt.plist

Running?

	ps aux | grep postgres


Opened this with root:

	sudo /Applications/Xcode.app/Contents/MacOS/Xcode /system/library/LaunchDaemons/org.postgresql.postgres_alt.plist

Changed this:

	From 	/var/pgsql_socket_alt
	To:		/tmp/.s.PGSQL.5432
	
Got it working with this:

	sudo launchctl load -w /system/library/LaunchDaemons/org.postgresql.postgres_alt.plist


No database active if:

	""/tmp/.s.PGSQL.5432""

Worked after this:	

	sudo port install postgresql93-server
	
	sudo mkdir -p /opt/local/var/db/postgresql93/defaultdb

	sudo chown postgres:postgres /opt/local/var/db/postgresql93/defaultdb

	sudo su postgres -c '/opt/local/lib/postgresql93/bin/initdb -D /opt/local/var/db/postgresql93/defaultdb'
	
Start with:

    /opt/local/lib/postgresql93/bin/postgres -D /opt/local/var/db/postgresql93/defaultdb

	or
    
    /opt/local/lib/postgresql93/bin/pg_ctl -D /opt/local/var/db/postgresql93/defaultdb -l logfile start
   
Load Port

	sudo port load postgresql93-server

Does it work?
	
	psql -U postgres