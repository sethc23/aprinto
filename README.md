
#####Workflow
First, the Aporo printer driver communicates with this server.

		. PDF received via url post request
		. PDF saved to filesystem
		. filepath and url post attributes saved to mySQL
		. task added to queue
		
Second, Aprinto continues processing the url post request and PDF until all servers are fully updated with Aporo printer driver communication.  This processessing includes:

        . generating an HTML from the PDF (pdftohtml)
        . saving contents of the HTML are posted via URL request
        . the HTML is parsed and posted via URL request
            --> vendor, tag, web, web_url, deliv_addr. deliv_cross_street

#####Continued Workflow
A separate server then picks up where Aprinto leaves off:

		. coordinates obtained via google API and posted via URL request
            --> deliv_lat, deliv_long
    	. distances between a point and all other points cached 
    		<-- provided by pgrouting/qgis/postgresql/NYC.gis system

#####Comparing Data between servers
A quick comparison of data between simulation and application:

	SIM DATA		APORO DATA

		Vendor:

			id			=	vendor name
			vend_X		=	vend_lat, pickup_addr_lat
			vend_Y		=	vend_long, pickup_addr_long
			orderNum	=	[ index of orders from one vendor ]

			deliveryID	=	order_id
			orderTime	=	created
			start_X		=	pickup_addr_lat / vend_lat
			start_Y		=	pickup_addr_long / vend_long
			end_X		=	deliv_lat
			end_Y		=	deliv_long
		
		Order:
			
		
		DG:
		
			
