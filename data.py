#!/usr/bin/env python3
import subprocess
import statistics
from prettytable import PrettyTable
import logging
import time

# Set up logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# List of websites
websites = ["google.co.uk", "microsoft.com", "amazon.co.uk", "facebook.com", "x.com", "google.com", "github.com", "bbc.co.uk", "apple.com", "www.gov.uk", "spotify.com", "youtube.com", "reddit.com", "netflix.com", "tiktok.com", "bing.com", "instagram.com", "bluesky.com"]
# List of custom DNS servers
dns_servers = ["dns.quad9.net", "dns11.quad9.net", "one.one.one.one", "dns.google.com", "62.6.40.178", "dns.controld.com"]

def resolve_ip(website, dns_server):
    try:
        logging.debug(f"Resolving IP for {website} using DNS server {dns_server}")
        start_time = time.time()
        result = subprocess.run(["dig", "+short", "@{}".format(dns_server), website], capture_output=True, text=True)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        ip_address = result.stdout.strip().split("\n")[0]
        logging.debug(f"Resolved IP for {website}: {ip_address} in {response_time:.2f} ms")
        return ip_address, response_time
    except Exception as e:
        logging.error(f"Error resolving IP for {website}: {e}")
        return None, None

def ping_website(ip_address):
    try:
        logging.debug(f"Pinging IP address {ip_address}")
        result = subprocess.run(["ping", "-i", "0.20", "-c", "100", ip_address], capture_output=True, text=True)
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

# Collect and print results for each website
for website in websites:
    table = PrettyTable()
    table.field_names = ["DNS Server", "DNS Response Time (ms)", "Resolved IP", "Min Ping (ms)", "Median Ping (ms)", "Max Ping (ms)", "Traceroute Hops"]
    
    for dns_server in dns_servers:
        ip_address, dns_response_time = resolve_ip(website, dns_server)
        if ip_address:
            min_ping, median_ping, max_ping = ping_website(ip_address)
            hops = traceroute_website(ip_address)
            table.add_row([dns_server, dns_response_time, ip_address, min_ping, median_ping, max_ping, hops])
        else:
            table.add_row([dns_server, dns_response_time, None, None, None, None, None])
    
    print(f"Results for {website}:")
    print(table)
    print("\n")
