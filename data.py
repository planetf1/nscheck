#!/usr/bin/env python3

import subprocess
import statistics
from prettytable import PrettyTable
import logging

# Set up logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# List of websites
websites = ["google.co.uk", "microsoft.com", "amazon.co.uk", "facebook.com","www.x.com","google.com","github.com","www.bbc.co.uk"]
# List of custom DNS servers
dns_servers = ["dns.quad9.net", "one.one.one.one", "dns.google.com","62.6.40.178","dns.controld.com"]

def resolve_ip(website, dns_server):
	try:
		logging.debug(f"Resolving IP for {website} using DNS server {dns_server}")
		result = subprocess.run(["dig", "+short", "@{}".format(dns_server), website], capture_output=True, text=True)
		ip_address = result.stdout.strip().split("\n")[0]
		logging.debug(f"Resolved IP for {website}: {ip_address}")
		return ip_address
	except Exception as e:
		logging.error(f"Error resolving IP for {website}: {e}")
		return None

def ping_website(ip_address):
	try:
		logging.debug(f"Pinging IP address {ip_address}")
		result = subprocess.run(["ping", "-i", "0.25","-c", "20", ip_address], capture_output=True, text=True)
		lines = result.stdout.split("\n")
		times = [float(line.split("time=")[1].split(" ")[0]) for line in lines if "time=" in line]
		min_time = min(times)
		median_time = statistics.median(times)
		max_time = max(times)
		return min_time, median_time, max_time
	except Exception as e:
		logging.error(f"Error pinging IP address {ip_address}: {e}")
		return None, None, None

def traceroute_website(ip_address):
	try:
		logging.debug(f"Running traceroute for IP address {ip_address}")
		result = subprocess.run(["traceroute", ip_address], capture_output=True, text=True)
		lines = result.stdout.split("\n")
		hops = len([line for line in lines if line.strip() and not line.startswith("traceroute")])
		return hops
	except Exception as e:
		logging.error(f"Error running traceroute for IP address {ip_address}: {e}")
		return None

# Create a table to display results
table = PrettyTable()
table.field_names = ["Website", "DNS Server", "Min Ping (ms)", "Median Ping (ms)", "Max Ping (ms)", "Traceroute Hops"]

# Collect and print results for each website
for website in websites:
	table = PrettyTable()
	table.field_names = ["DNS Server", "Min Ping (ms)", "Median Ping (ms)", "Max Ping (ms)", "Traceroute Hops"]
	
	for dns_server in dns_servers:
		ip_address = resolve_ip(website, dns_server)
		if ip_address:
			min_ping, median_ping, max_ping = ping_website(ip_address)
			hops = traceroute_website(ip_address)
			table.add_row([dns_server, min_ping, median_ping, max_ping, hops])
		else:
			table.add_row([dns_server, None, None, None, None])
	
	print(f"Results for {website}:")
	print(table)
	print("\n")
