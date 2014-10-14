#Getting Started

###Initial Setup

Install the software:

	sudo port install pgrouting
	sudo port install postgresql93
	sudo port install postgresql93-server
	sudo port install postgresql_select
	sudo port select postgresql postgresql93


The instructions for `postgresql93` dictate:

	To create a database instance, after install do this:
	
 		sudo mkdir -p /opt/local/var/db/postgresql93/defaultdb
 		sudo chown postgres:postgres /opt/local/var/db/postgresql93/defaultdb
 		sudo su postgres -c '/opt/local/lib/postgresql93/bin/initdb -D /opt/local/var/db/postgresql93/defaultdb' 

Need to make a small change config

	sudo emacs /opt/local/var/db/postgresql93/defaultdb/pg_hba.conf

	add to the top:
	
		local   all             postgres                                trust

Start the postgresql server:

	sudo su postgres -c "/opt/local/lib/postgresql93/bin/postgres -D /opt/local/var/db/postgresql93/defaultdb"

Check that you can get into cmd prompt:

	psql -U postgres

#Loading Data

####IMPORTANT CONSIDERATIONS:

1. Are GIS files using same CRS? (see end re: CRS)
2. Are positions in the GIS files Project or Unprojected?
3. Are the initial starting reference points the same?


### --- NYC Data ---

######NYC GIS data obtained:

1. NYC part from OpenStreetMap

		http://mapzen.com/metro-extracts

2. Single Line Street base map dataset

		http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml#lion
3. 


######Load OpenStreetMap Data:
	
	osm2pgrouting -file "/Users/sethchase/Projects/GIS/OpenStreetMaps/new-york.osm" \
                          -conf "/Users/sethchase/Projects/GIS/mapconfig.xml" \
                          -dbname routing \
                          -user postgres \
                          -clean
	cd /Users/sethchase/Projects/GIS/OpenStreetMaps/new-york.osm2pgsql-geojson/
	ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 user=postgres dbname=db1" new-york.osm-line.geojson -nln geoj_line
	ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 user=postgres dbname=routing" new-york.osm-point.geojson -nln geoj_point
	ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 user=postgres dbname=routing" new-york.osm-polygon.geojson -nln geoj_polygon
	
	cd /Users/sethchase/Projects/GIS/OpenStreetMaps/new-york.osm2pgsql-geojson/
	ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 user=postgres dbname=routing" new-york.osm-line.geojson -nln shp_line
	ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 user=postgres dbname=routing" new-york.osm-point.geojson -nln shp_point
	ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 user=postgres dbname=routing" new-york.osm-polygon.geojson -nln shp_polygon

######Convert NYC BYTES Data:

1. Open QGIS

2. Add New Vector from Directory --> lion.gdb

3. Reproject layers "lion" and "node" to 4326 (WGS84).
	
		from Processing Toolbox,
			--> QGIS geoalgorithms,
			--> Vector general tools,
			--> Reproject layer.
		
4. Add New Vector from File MNMapPLUTO.shp4

5. Right-click, Save Layers as ESRI Shapefiles:
		
		lion_wgs84.shp
		node_wgs84.shp
		MNMapPLUTO.shp

######Load Converted NYC BYTES Data in psql:
		
		shp2pgsql -s 4326 /Users/sethchase/Projects/GIS/NYC_gov_data/lion/lion_wgs84.shp public.lion_ways | psql -U postgres -h localhost routing
		
		shp2pgsql -s 4326 /Users/sethchase/Projects/GIS/NYC_gov_data/lion/node_wgs84.shp public.lion_nodes | psql -U postgres -h localhost routing
		
		shp2pgsql -s 4326 /Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/MNMapPLwgs_WGS84.shp public.pluto | psql -U postgres -h localhost routing
		
# END

####Appendix A:  Coordinate Reference Systems (CRSs)

EPSG codes for commonly used CRS (in the U.S.):
	
	Latitude/Longitude
	
		WGS84 (EPSG: 4326) 
		+init=epsg:4326 +proj=longlat +ellps=WGS84 
		+datum=WGS84 +no_defs +towgs84=0,0,0
		## CRS used by Google Earth and the U.S. Department of 
		Defense for all their mapping. Tends to be used for global 
		reference systems. GPS satellites broadcast the predicted 
		WGS84 orbits.
	
		NAD83 (EPSG:4269) 
		+init=epsg:4269 +proj=longlat +ellps=GRS80 +datum=NAD83 
		+no_defs +towgs84=0,0,0
		##Most commonly used by U.S. federal agencies. Aligned 
		with WGS84 at creation, but has since drifted. Although 
		WGS84 and NAD83 are not equivalent, for most applications 
		they are considered equivalent.
	
		NAD27 (EPSG: 4267)
		+init=epsg:4267 +proj=longlat +ellps=clrk66 +datum=NAD27 
		+no_defs
		+nadgrids=@conus,@alaska,@ntv2_0.gsb,@ntv1_can.dat
		##Has been replaced by NAD83, but is still encountered!

	Projected (Easting/Northing)
	
		UTM, Zone 10 (EPSG: 32610)
		## Zone 10 is used in the Pacific Northwest
	
		Mercator (EPSG: 3857)
		## Tiles from Google Maps, Open Street Maps, Stamen 
		Maps
