import re
from beautifultable import BeautifulTable as bt


prog = re.compile(r'-ROOT|-LEAF|-MP|-MPP|-MMP|-mp|-mpp|-mmp|mesh|-\d')


def parse_access_point_list(source):
	"""Parse access point from table.

	Parse data from a text file and build a list of 
	access points represented as dictionaries. 

	Parameters
	----------
	source : string
		A string representing the absolute path to the data source.
	
	Returns
	-------
	list
		A list of AP represented as dict.
	"""
	if source == None:
		source = 'data.txt'
	access_points = list()
	with open(source) as fp:
		for line in iter(fp.readline, ''):
			line_splitted =line.split()
			access_point = list()
			access_point = {
				'id' : int(line_splitted[0]),
				'mac' : line_splitted[1],
				'ap-name' : line_splitted[2],
				'ap-group' : line_splitted[3],
				'ip' : line_splitted[4],
				'product' : line_splitted[5],
				'status' : line_splitted[6],
				'sta' : int(line_splitted[7]),
				'running-time' : line_splitted[8]
				}
			access_points.append(access_point)

	return access_points


def create_site_buckets(access_points):
	"""Splits sites name by regex and returns a list of site.

	AP group name identifies the name of the city in which the AP is installed (according to the project naming convention).
	Use regular expression to remove mesh naming markers.

	Parameters
	----------
	access_points : list
		list of access points represented as dict.

	Returns
	-------
	list
		a list of sites yet to be populated.
	"""
	unique_sites = set()

	for ap in access_points:
		site = max(prog.split(ap['ap-group']), key=len)
		unique_sites.add(site)

	unique_sites = sorted(unique_sites)
	sites = list()
	for site in unique_sites:
		site_info =  {
			'name' : site,
			'region' : None,
			'active' : int(),
			'expected' : int(),
			'faulty' : int(),
			'mesh' : int()
			}
		sites.append(site_info)

	return sites


def populate_sites_info(access_points, sites):
	"""Create a new list based of aggregated access points based on sites.

	Populates the values of the dictionaries in sites with info 
	read from the access point list and returns the populated
	list.

	Parameters
	----------
	access_points : list
		list of access points.

	sites : list
		list of cities to be populated.

	Returns
	-------
	list
		populated list.
	"""
	for ap in access_points:
		
		site_name = max(prog.split(ap['ap-group']), key=len)
		
		for item in sites:
			
			if item['name'] == site_name:
				item['expected'] += 1
				
				if ap['status'] == 'nor':
					item['active'] += 1
				else:
					item['faulty'] += 1

				if '-MP' in ap['ap-group'] and 	\
				'-MPP' not in ap['ap-group'] or	\
				'-LEAF' in ap['ap-group'] or	\
				'-1' in ap['ap-group'] or		\
				'-2' in ap['ap-group']:
					item['mesh'] += 1
				break

	return sites


def print_beautifultable(sites, file_dest):
	"""Print the site list in ASCII table markdown format.
	
	Parameters
	----------
	sites : list
		list of sites.

	file_dest : string
		absoulte path to the output file
	"""
	if file_dest is None:
		file_dest = 'tables.txt'
	if sites is None:
		print(None)
	table = bt()
	table.set_style(bt.STYLE_MARKDOWN)
	table.column_headers = list(sites[0].keys())
	for item in sites:
		table.append_row(list(item.values()))

	with open(file_dest, 'w') as fp:
		fp.write(str(table))

	print(str(table))
