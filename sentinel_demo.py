from sentinelhub import SHConfig, MimeType, CRS, BBox, SentinelHubRequest,   \
SentinelHubDownloadClient, DataCollection, bbox_to_dimensions, DownloadRequest
import os
import datetime
import yaml
import numpy as np
import matplotlib.pyplot as plt
from utils import plot_image, plot_animation

download_dir = "data"

#=============================================================================
# SETUP CONFIGS
#=============================================================================
SHconfig = yaml.load(open('SHconfig.yaml'), Loader=yaml.FullLoader)
#set configs for sentinel API
config = SHConfig()
config.instance_id = SHconfig['instance_id']
config.sh_client_id = SHconfig['sh_client_id']
config.sh_client_secret = SHconfig['sh_client_secret']

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
tofino_coords_wgs84 = [-126.033804,48.918678,-125.429556,49.213799]
resolution = 10
tofino_bbox = BBox(bbox=tofino_coords_wgs84, crs=CRS.WGS84)
tofino_size = bbox_to_dimensions(tofino_bbox, resolution=resolution)

#create bounding box for chilliwack lake
chilliwack_coords_wgs84 = [-121.596894,48.991100,-121.243272,49.162019]
resolution = 10
chilliwack_bbox = BBox(bbox=chilliwack_coords_wgs84, crs=CRS.WGS84)
chilliwack_size = bbox_to_dimensions(chilliwack_bbox, resolution=resolution)

#=============================================================================
# LOAD EVALSCRIPTS
#=============================================================================
#the evalscript is used to select what colour bands we want and  
#they are stored in evalscripts.yaml
evalscript = yaml.load(open('evalscripts.yaml'), Loader=yaml.FullLoader)

#=============================================================================
# CREATE TIMESLOTS FOR GIF
#=============================================================================
#creats an array of time intervals, in this case each month of 2019
start = datetime.datetime(2019,1,1)
end = datetime.datetime(2019,12,31)
n_chunks = 13
tdelta = (end - start) / n_chunks
edges = [(start + i*tdelta).date().isoformat() for i in range(n_chunks)]
slots_2019 = [(edges[i], edges[i+1]) for i in range(len(edges)-1)]

#=============================================================================
# REQUESTS BUILDER
#=============================================================================
def get_request(bbox, size, config, time_interval, dl_dir=None, \
				evalscript=evalscript['true_color']):
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

def main():
    #create a list of requests for shawnigan lake area for NDVI
    list_of_requests = [get_request(bbox=shawnigan_bbox,		    \
    								size=shawnigan_size,		    \
    								config=config,					\
    								time_interval=slot,   	 	    \
    								dl_dir=download_dir,			\
    								evalscript=evalscript['NDVI'])     \
    								for slot in slots_2019]
    #create list of image packages
    list_of_images = [request.get_data() for request in list_of_requests]
    #create list of images
    list_of_images_fr = [image[0] for image in list_of_images]
    #create annimation for array of images
    plot_animation(list_of_images_fr, factor=.8/255, clip_range=(0,1))


if __name__ == "__main__":
    main()
