import routeros_api
import time
from collections import defaultdict

# --- Configuration ---
# IP address of your MikroTik router
MIKROTIK_HOST = '192.168.77.1'
# The user you created for the API
MIKROTIK_USER = 'py-script'      
# The password for the API user
MIKROTIK_PASS = 'Amin070565'  
# Default API port
MIKROTIK_PORT = 8728            

# --- AI Logic Settings ---
# If an IP accesses more than 15 unique ports within 60 seconds, it's considered an attacker
# Number of unique ports to trigger the block
PORT_SCAN_THRESHOLD = 15  
# Time window in seconds to track the ports
TIME_WINDOW = 60          

# --- Global Variables ---
# This dictionary will store data about potential attackers
potential_attackers = defaultdict(lambda: {'ports': set(), 'start_time': time.time()})

def process_logs(logs):
    """Analyzes log entries to detect port scanning behavior."""
    detected_attackers = []
    current_time = time.time()

    for log in logs:
        message = log.get('message', '')
        parts = message.split()
        
        src_address = ''
        dst_port = ''

        # Extract source IP and destination port from the log message
        for part in parts:
            if 'src-address=' in part:
                # Get the IP before the colon (:)
                src_address = part.split('=')[1].split(':')[0]
            if 'dst-port=' in part:
                dst_port = part.split('=')[1]
        
        # If IP or port couldn't be found, skip this log entry
        if not src_address or not dst_port:
            continue

        # Get the data for the current source IP
        attacker_data = potential_attackers[src_address]
        
        # If the current time is outside the tracking window, reset the data for this IP
        if current_time - attacker_data['start_time'] > TIME_WINDOW:
            attacker_data['ports'] = {dst_port}
            attacker_data['start_time'] = current_time
        else:
            # Otherwise, add the new port to the set of tracked ports for this IP
            attacker_data['ports'].add(dst_port)

        # Check if the number of unique ports has exceeded the threshold
        if len(attacker_data['ports']) > PORT_SCAN_THRESHOLD:
            if src_address not in detected_attackers:
                print(f"🚨 Port scan attack detected from IP: {src_address}")
                detected_attackers.append(src_address)
                # Reset data for this IP to prevent repeated alerts in the same cycle
                del potential_attackers[src_address]

    return detected_attackers

def connect_to_mikrotik():
    """Establishes a connection to the MikroTik router."""
    try:
        connection = routeros_api.RouterOsApiPool(MIKROTIK_HOST, username=MIKROTIK_USER, password=MIKROTIK_PASS, plaintext_login=True)
        api = connection.get_api()
        print("✅ Successfully connected to MikroTik router.")
        return api
    except routeros_api.exceptions.RouterOsApiConnectionError as e:
        print(f"❌ Error connecting to MikroTik: {e}")
        return None

def get_firewall_logs(api):
    """Fetches firewall log entries with the specific prefix."""
    # We only get logs with the prefix we set in the firewall rule
    return api.get_resource('/log').get(topic='firewall,info', message='PORT_SCAN_LOG')

def block_attacker(api, ip_address):
    """Adds the attacker's IP to the 'blocked_attackers' address list in the firewall."""
    try:
        firewall_list = api.get_resource('/ip/firewall/address-list')
        firewall_list.add(list='blocked_attackers', address=ip_address, comment=f'Blocked by AI IDS at {time.ctime()}')
        print(f"🚫 IP {ip_address} has been successfully blocked.")
    except routeros_api.exceptions.RouterOsApiError as e:
        # This handles the case where the IP is already in the list
        if "already has such entry" in str(e):
            print(f"ℹ️ IP {ip_address} is already in the block list.")
        else:
            print(f"❌ Error while trying to block {ip_address}: {e}")

def clear_logs(api):
    """Clears the processed logs from the router to avoid re-reading them."""
    # In a production environment, you might want to archive logs instead of deleting
    log_resource = api.get_resource('/log')
    logs_to_clear = log_resource.get(topic='firewall,info', message='PORT_SCAN_LOG')
    for log in logs_to_clear:
        log_resource.remove(id=log['id'])
    print("--- Processed logs have been cleared ---")

def main():
    """The main loop of the program."""
    api = connect_to_mikrotik()
    if not api:
        return

    print("🚀 AI Intrusion Detection System is now running...")
    while True:
        try:
            logs = get_firewall_logs(api)
            if logs:
                attackers = process_logs(logs)
                for attacker_ip in attackers:
                    block_attacker(api, attacker_ip)
                clear_logs(api)
            
            # Wait for 10 seconds before checking again
            time.sleep(10)

        except KeyboardInterrupt:
            print("\n🛑 Program stopped by user.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Attempting to reconnect in 30 seconds...")
            time.sleep(30)
            api = connect_to_mikrotik()
            if not api:
                print("❌ Reconnection failed. Exiting program.")
                break

if __name__ == "__main__":
    main()