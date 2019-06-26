import requests
import json
import os
from .values import non_sites, regions


def get_site_info(sites):
	"""Retrieve geographic info of every site.

	Query the Bing geolocalization tool to retrieve the region in which the AP group is installed.

	Parameters
	----------
	sites : list
		list containing dicts representing APs.

	"""
	key = os.environ['BING_API']
	for site in sites:
		if site['name'] not in non_sites:
			parameters = {'query' : site['name'], 'key' : key}
			r = requests.get('http://dev.virtualearth.net/REST/v1/Locations', params = parameters)
			json_response = json.loads(r.text)
			set_region(json_response, site)


def set_region(json_obj, site):
	"""Set the region on the AP object in the list.

	Perform the pairing between the region found through geolocalization and the official region list.
	When the region found is not present in the official region list, replace it with n.d.

	Parameters
	----------

	json_obj : dict
		json response obtained from geolocalization query.
	site : dict
		dict representing the access point.
	"""
	region = None
	try:
		site_region = json_obj['resourceSets'][0]['resources'][0]['address']['adminDistrict']
		if site_region not in regions.keys():
			print('Region not found ---> %s' % site_region)
			region = 'n.d.'
		else:
			region = regions[site_region]
	except IndexError as err:
		print('Index error: ', err)
		region = 'n.d.'
	except KeyError as err:
		print('KeyError: ' , err)
	finally:
		site['region'] = region
