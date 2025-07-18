import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime

def get_ssl_expiry_date(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port), timeout=10) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expiry_str = cert['notAfter']
            expiry_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")
            return expiry_date

def check_ssl(url):
    if not url.startswith("http"):
        url = "https://" + url
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    try:
        expiry_date = get_ssl_expiry_date(hostname)
        days_left = (expiry_date - datetime.utcnow()).days
        return hostname, expiry_date, days_left
    except Exception as e:
        print(f"❌ Failed to get SSL certificate info for {hostname}: {e}")
        return hostname, None, None

# Lista URL da controllare
url_list = [
    "www.sisalwincity.it",
    "inside.sisal.com",
    "wildcard.sisal.it"
]

# Creazione del file di output
output_file = "ssl_results.csv"

with open(output_file, "w") as f:
    # intestazione CSV
    f.write("Hostname;Expiry Date;Days Left\n")  
    for url in url_list:
        hostname, expiry_date, days_left = check_ssl(url)
        if expiry_date is not None:
            f.write(f"{hostname};{expiry_date};{days_left};\n")
        else:
            f.write(f"{hostname};ERROR;ERROR\n")

