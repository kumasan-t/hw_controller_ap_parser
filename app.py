import argparse
import tools.utils as ut
import tools.geo as geo

	
def run(source, destination):
	# Parse the access point table of the controller.
	access_points = ut.parse_access_point_list(source)
	# Create a list of sites from an access point list.
	sites = ut.create_site_buckets(access_points)
	# Populate each site with aggregated data from access point.
	populated_sites = ut.populate_sites_info(access_points, sites)
	# Use Bing geocoding REST service to get region of each site.
	geo.get_site_info(populated_sites)
	# Print an ASCII table of the site list.
	ut.print_beautifultable(populated_sites, destination)


if __name__ == '__main__':
	# Defining arguments for CLI usage.
	parser = argparse.ArgumentParser()
	parser.description = 'This tool is used to obtain a		\
		markdown-styled ASCII table of the access points	\
		currently installed on a Huawei Access Controller.'
	parser.add_argument('--src', help=r"Path to source file. By default, it's .\data.txt.")
	parser.add_argument('--dest', help=r"Path to destination file. By default, it's .\tables.txt.")
	args = parser.parse_args()
	run(args.src, args.dest)
