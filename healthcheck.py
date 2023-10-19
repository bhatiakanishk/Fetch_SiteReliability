import time
import requests
import yaml
from urllib.parse import urlparse

def health_check(endpoints):
    # Dictionary to store availability for each domain
    availability = {}
    
    while True:
        for endpoint in endpoints:
            url = endpoint['url']
            domain = urlparse(url).netloc
            method = endpoint.get('method', 'GET')
            headers = endpoint.get('headers', {})
            body = endpoint.get('body')
            availability.setdefault(domain, {'UP': 0, 'TOTAL': 0})
            
            try:
                # Starting time of the HTTP request
                start_time = time.time()
                
                response = requests.request(method, url, headers=headers, data=body)
                
                # Ending time of the HTTP request
                end_time = time.time()
                
                # Check if response code is in the 200-299 range and response latency is less than 500 ms
                if 200 <= response.status_code < 300 and end_time - start_time < 0.5:
                    availability[domain]['UP'] += 1
                availability[domain]['TOTAL'] += 1
                
            except requests.exceptions.RequestException:
                availability[domain]['TOTAL'] += 1
                
        for domain, stats in availability.items():
            # Calculate availability percentage for the domain
            availability_percentage = round((stats['UP'] / stats['TOTAL']) * 100)
            
            # Print the availability percentage for the domain
            print(f"{domain} has {availability_percentage}% availability percentage")
            
        print("-----------------------------------------------------")
        
        # Wait 15 seconds
        time.sleep(15)
        
if __name__ == "__main__":
    file_path = input("Enter the file path: ")
    with open(file_path, 'r') as file:
        endpoints = yaml.safe_load(file)
    health_check(endpoints)