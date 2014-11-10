
##### Aprinto Workflow

1. the Aporo printer driver 'checks in' with this server:
		
			URL: http://ec2-54-88-101-190.compute-1.amazonaws.com/api/check/
			JSON Posted:
	
				[
				    {
				        "application_name": "application_name1", 
				        "doc_name": "test_unit_1", 
				        "machine_id": "machine_id1", 
				        "pdf_id": "a60fefe9-65f2-468c-9743-345bd6be2604", 
				        "printer_id": "printer_id1"
				    }
				]

2. Aprinto  returns variables/instructions for the printer driver:

		{
		    "doc_post_url": "http://printer.aporodelivery.com", 
		    "order_tag": "NKKJ", 
		    "qr_code_scale": 0.001, 
		    "qr_code_x": 5, 
		    "qr_code_y": 1, 
		    "qr_url": "http://app.aporodelivery.com/qr/a60fefe9-65f2-468c-9743-345bd6be2604", 
		    "tag_scale": 0.001, 
		    "tag_x": 5, 
		    "tag_y": 1
		}

3. the Aporo printer driver then:

	* superimposes a QR code and order tag (according to the above specifications, e.g., 'qr_code_scale', 'tag_x', etc...) onto the PDF doc being posted,
	* transmits said doc to the server recieving the file at 'doc_post_url', and
	* prints the document at a location designated by the Aporo printer driver user. </br></br>

4. Aprinto recieves/saves the PDF doc, updates the below pgSQL database columns, and adds the doc to the task queue (Celery/Redis):

		pdf_id character varying(38) NOT NULL,
		created timestamp with time zone NOT NULL,
		order_tag character varying(4),
		printer_id text,
		machine_id text,
		application_name text,
		doc_name character varying(100),
		local_document character varying(255),
		qr_url text,
		doc_as_xml text,
		status text,
		date_uploaded timestamp with time zone NOT NULL,

5. Aprinto 
		. PDF received via url post request
		. PDF saved to filesystem
		. filepath and url post attributes saved to mySQL
		. task added to queue
		
Second, Aprinto continues processing the url post request and PDF until all servers are fully updated with Aporo printer driver communication.  This processing includes:

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
		
			
