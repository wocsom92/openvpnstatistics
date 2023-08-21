import requests

class IpInfo:
    def get_ip_location(ip_address):
        url = f"https://ipinfo.io/{ip_address}/json"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                ip_data = response.json()
                return ip_data
            else:
                print("Failed to retrieve IP location:", response.status_code)
        except requests.RequestException as e:
            print("An error occurred:", e)
        
        return None