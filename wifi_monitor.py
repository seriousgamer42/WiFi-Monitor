import subprocess
import time
import socket
import logging
from datetime import datetime
from collections import deque
import json
import os

class WifiMonitor:
    def __init__(self):
        self.setup_logging()
        self.disconnection_history = deque()  # Store all disconnections
        self.load_history()
        self.last_status = True  # True = connected, False = disconnected
        
    def setup_logging(self):
        """Set up logging configuration"""
        logging.basicConfig(
            filename='wifi_monitor.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def load_history(self):
        """Load disconnection history from file"""
        try:
            if os.path.exists('disconnection_history.json'):
                with open('disconnection_history.json', 'r') as f:
                    history = json.load(f)
                    self.disconnection_history = deque(history)
        except Exception as e:
            logging.error(f"Error loading disconnection history: {str(e)}")
            
    def save_history(self):
        """Save disconnection history to file"""
        try:
            with open('disconnection_history.json', 'w') as f:
                json.dump(list(self.disconnection_history), f)
        except Exception as e:
            logging.error(f"Error saving disconnection history: {str(e)}")

    def check_internet_connection(self):
        """Check if there's an active internet connection"""
        try:
            # Try to connect to Google's DNS server
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def toggle_wifi(self):
        """Turn WiFi off and then on"""
        try:
            # Turn WiFi off
            subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'admin=disable'], check=True)
            logging.info("WiFi turned off")
            
            # Wait for a few seconds
            time.sleep(5)
            
            # Turn WiFi on
            subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'admin=enable'], check=True)
            logging.info("WiFi turned on")
            
            # Wait for connection to establish
            time.sleep(10)
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Error toggling WiFi: {str(e)}")
            return False

    def log_disconnection(self):
        """Log disconnection event with timestamp"""
        timestamp = datetime.now().isoformat()
        self.disconnection_history.append({
            'timestamp': timestamp,
            'reconnected': False
        })
        self.save_history()
        
        # Print summary to console
        print(f"\nDisconnection detected at {timestamp}")
        print(f"Total disconnections: {len(self.disconnection_history)}")
        
    def print_status(self):
        """Print current status summary"""
        total_count = len(self.disconnection_history)
        print(f"\nStatus Summary:")
        print(f"Total recorded disconnections: {total_count}")
        if self.disconnection_history:
            last_disconnect = datetime.fromisoformat(self.disconnection_history[-1]['timestamp'])
            print(f"Last disconnection: {last_disconnect.strftime('%Y-%m-%d %H:%M:%S')}")

    def run(self):
        """Main monitoring loop"""
        logging.info("WiFi monitoring started")
        print("WiFi monitoring started. Press Ctrl+C to stop.")
        
        consecutive_failures = 0
        
        while True:
            current_status = self.check_internet_connection()
            
            if not current_status:
                consecutive_failures += 1
                if consecutive_failures >= 2:  # Reset after 2 consecutive failed checks
                    if self.last_status:  # Only log if this is a new disconnection
                        self.log_disconnection()
                        self.last_status = False
                    
                    logging.info("Attempting to reset WiFi connection")
                    if self.toggle_wifi():
                        consecutive_failures = 0
                        self.last_status = True
                        logging.info("WiFi reset completed")
            else:
                consecutive_failures = 0
                self.last_status = True
            
            time.sleep(10)  # Check connection every 10 seconds

def main():
    monitor = WifiMonitor()
    try:
        monitor.run()
    except KeyboardInterrupt:
        logging.info("WiFi monitoring stopped by user")
        print("\nMonitoring stopped")
        monitor.print_status()

if __name__ == "__main__":
    main()
