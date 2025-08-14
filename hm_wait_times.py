import network
import time
import urequests as requests
from secrets import secrets
import json
import gc

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets['ssid'], secrets['password'])

print("Connecting to Wi-Fi", end="")
while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.5)
print("\nConnected!")


dl_id = None
def see_wait_times():
    while True:
        try:
            parks_resp = requests.get("http://queue-times.com/parks.json")
            companies = parks_resp.json()
            parks_resp.close()
            for company in companies:
                if company['name'] == 'Walt Disney Attractions':
                    print('got wd')
                    for park in company['parks']:
                        if park['name'] == 'Disneyland':
                            dl_id = park['id']
                            print(f'Got DL MK id {dl_id}')  
            gc.collect()   
        except Exception as e:
            print(f"Stuff happened: {e}")


        try:
            wait_times_resp = requests.get(f"http://queue-times.com/parks/{dl_id}/queue_times.json")
            if wait_times_resp.status_code == 200:
                all_rides = wait_times_resp.json()
                wait_times_resp.close()

                found = False
                for land in all_rides['lands']:
                    if land['name'] == "New Orleans Square":
                        for ride in land['rides']:
                            if ride['name'] == 'Haunted Mansion':
                                wait_time = ride['wait_time']
                                is_open = ride['is_open']
                                found = True
                                break
            wait_times_resp.close()
            del data  # Free memory explicitly
                if found:
                    status = 'not' if not is_open else 'definitely'
                    print(f"Haunted Mansion is {status} open. Wait time is {wait_time} min.")
                else:
                    print("Haunted Mansion not found.")
            else:
                print(f"Error: Status code {wait_times_resp.status_code}")
            gc.collec()
        except Exception as e:
            print(f"Error retrieving ride data: {e}")


if __name__ == "__main__":
    see_wait_times()
    