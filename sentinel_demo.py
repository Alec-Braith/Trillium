from sentinelhub import SHConfig, MimeType, CRS, BBox, SentinelHubRequest,   \
SentinelHubDownloadClient, DataCollection, bbox_to_dimensions, DownloadRequest
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from utils import plot_image, plot_animation

download_dir = "data"

#=============================================================================
# SETUP CONFIGS
#=============================================================================

#set configs for sentinel API
config = SHConfig()
config.instance_id = '49f1ba81-5174-4d9e-a532-33681ee90e3c'
config.sh_client_id = 'a20966ba-df0a-45f5-b81b-00526e40dc2c'
config.sh_client_secret = '?jrfwIJ&#dbc@[gg;L?3m<M^9x,!>3_UfQtR/HI#'

#check that authorization is added
if not config.sh_client_id or not config.sh_client_secret:
    print("Warning! To use Process API, please provide the credentials \
    	(OAuth client ID and client secret).")

#=============================================================================
# CREATE BOUNDING BOXES
#=============================================================================
#used this ink to find coords:http://bboxfinder.com/

#create bounding box for shawnigan lake
shawnigan_coords_wgs84 = [-123.696731,48.575624,-123.564895,48.670031]
resolution = 10
shawnigan_bbox = BBox(bbox=shawnigan_coords_wgs84, crs=CRS.WGS84)
shawnigan_size = bbox_to_dimensions(shawnigan_bbox, resolution=resolution)

#create bounding box for tofino area
shawnigan_coords_wgs84 = [-123.696731,48.575624,-123.564895,48.670031]
resolution = 10
shawnigan_bbox = BBox(bbox=shawnigan_coords_wgs84, crs=CRS.WGS84)
shawnigan_size = bbox_to_dimensions(shawnigan_bbox, resolution=resolution)

#create bounding box for chilliwak lake
shawnigan_coords_wgs84 = [-123.696731,48.575624,-123.564895,48.670031]
resolution = 10
shawnigan_bbox = BBox(bbox=shawnigan_coords_wgs84, crs=CRS.WGS84)
shawnigan_size = bbox_to_dimensions(shawnigan_bbox, resolution=resolution)

#=============================================================================
# CREATE EVALSCRIPTS
#=============================================================================
#the evalscript is used to select what colour bands we want

evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
"""

evalscript_NDVI = """
//VERSION=3

function setup() {
  return {
    input: ["B04", "B08"],
    output: { bands: 3 }
  };
}

function evaluatePixel(sample) {
    let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);

return colorBlend(ndvi,
   [-0.2, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0 ],
   [[0, 0, 0],                               //  < -.2 = #000000 (black)
    [165/255,0,38/255],        //  -> 0 = #a50026
    [215/255,48/255,39/255],   //  -> .1 = #d73027
    [244/255,109/255,67/255],  //  -> .2 = #f46d43
    [253/255,174/255,97/255],  //  -> .3 = #fdae61
    [254/255,224/255,139/255], //  -> .4 = #fee08b
    [255/255,255/255,191/255], //  -> .5 = #ffffbf
    [217/255,239/255,139/255], //  -> .6 = #d9ef8b
    [166/255,217/255,106/255], //  -> .7 = #a6d96a
    [102/255,189/255,99/255],  //  -> .8 = #66bd63
    [26/255,152/255,80/255],   //  -> .9 = #1a9850
    [0,104/255,55/255]         //  -> 1.0 = #006837
   ]);
}
"""
#=============================================================================
# CREATE TIMESLOTS FOR GIF
#=============================================================================
#creats an array of time intervals in this case each month of 2019
start = datetime.datetime(2019,1,1)
end = datetime.datetime(2019,12,31)
n_chunks = 13
tdelta = (end - start) / n_chunks
edges = [(start + i*tdelta).date().isoformat() for i in range(n_chunks)]
slots_2019 = [(edges[i], edges[i+1]) for i in range(len(edges)-1)]

#=============================================================================
# GENERATE REQUESTS
#=============================================================================
def get_request(bbox, size, config, time_interval, dl_dir=None, \
				evalscript=evalscript_true_color):
	"""Generates a request
		Args: 
			bbox(int array) : bounding coordinates
			size(not sure) : size and resolution of image
			config(config object) : configs for sentinel hub API
			time_interval(datetime) : what interval the image should come from
			dl_dir(string) : directory for downloads to go into
			evalscript(strin) : script for sentinel hub API 

		Returns: the resulting reply from the API request
	"""
	return SentinelHubRequest(
	    data_folder=dl_dir,
	    evalscript=evalscript,
	    input_data=[
	        SentinelHubRequest.input_data(
	            data_collection=DataCollection.SENTINEL2_L1C,
	            time_interval=time_interval,
	        )
	    ],
	    responses=[
	        SentinelHubRequest.output_response('default', MimeType.PNG)
	    ],
	    bbox=bbox,
	    size=size,
	    config=config
	)

#create a list of requests for shawnigan lake area for NDVI
list_of_requests = [get_request(bbox=shawnigan_bbox,		    \
								size=shawnigan_size,		    \
								config=config,					\
								time_interval=slot,   	 	    \
								dl_dir=download_dir,			\
								evalscript=evalscript_NDVI)     \
								for slot in slots_2019]
#create list of image packages
list_of_images = [request.get_data() for request in list_of_requests]
#create list of images
list_of_images_fr = [image[0] for image in list_of_images]
#create annimation for array of images
plot_animation(list_of_images_fr, factor=.8/255, clip_range=(0,1))
