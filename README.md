# WiFi Connection Monitor

A Python script that automatically monitors and manages your Windows 11 WiFi connection. When a disconnection is detected, the script automatically resets the WiFi adapter and logs the event.

## Features

- Continuous WiFi connection monitoring
- Automatic WiFi reset on disconnection detection
- Comprehensive logging system
- Unlimited disconnection history tracking
- Real-time status reporting
- Summary statistics

## Requirements

- Windows 11
- Python 3.x
- Administrator privileges (required for network interface commands)

## Installation

1. Clone or download this repository to your local machine
2. Ensure Python 3.x is installed on your system
3. No additional Python packages are required (uses only standard library)

## Usage

1. Open Command Prompt as administrator
2. Navigate to the script directory
3. Run the script:
```bash
python wifi_monitor.py
```

To stop the monitoring, press `Ctrl+C`. The script will display a summary of disconnection statistics before exiting.

## Output Files

The script generates two files:

1. `wifi_monitor.log`
   - Detailed technical log of all events
   - Includes timestamps, actions taken, and any errors
   - Example:
     ```
     2024-11-05 10:30:15 - INFO - WiFi monitoring started
     2024-11-05 10:35:20 - WARNING - Internet connection lost
     2024-11-05 10:35:22 - INFO - Attempting to reset WiFi connection
     ```

2. `disconnection_history.json`
   - Persistent record of all disconnection events
   - Stores the complete history of disconnections
   - Preserved between script runs
   - Example:
     ```json
     [
       {
         "timestamp": "2024-11-05T10:35:20",
         "reconnected": true
       },
       {
         "timestamp": "2024-11-06T14:22:41",
         "reconnected": false
       }
     ]
     ```

## Features in Detail

### Connection Monitoring
- Checks connection every 10 seconds
- Requires 2 consecutive failed checks before triggering reset
- Tests connection by attempting to reach Google's DNS (8.8.8.8)

### WiFi Reset Process
1. Disables WiFi adapter
2. Waits 5 seconds
3. Re-enables WiFi adapter
4. Waits 10 seconds for connection to establish

### Status Reporting
- Real-time disconnection notifications
- Total recorded disconnections
- Timestamp of most recent disconnection

## Troubleshooting

1. "Access Denied" error
   - Make sure you're running Command Prompt as administrator
   - Right-click Command Prompt → Run as administrator

2. Script not detecting WiFi adapter
   - Verify your WiFi adapter name matches "Wi-Fi"
   - If different, modify the interface name in the `toggle_wifi()` function

3. Logs not generating
   - Ensure the script has write permissions in its directory
   - Check available disk space

## Customization

You can modify these variables in the script to adjust its behavior:

- `time.sleep(10)` in main loop: Adjust the connection check frequency
- `time.sleep(5)` in `toggle_wifi()`: Modify the wait time after disabling WiFi
- `consecutive_failures >= 2`: Change the number of failed checks before reset

## Contributing

Feel free to fork this repository and submit pull requests with improvements. Some areas for potential enhancement:

- GUI interface
- Email notifications for disconnections
- Network speed monitoring
- Custom reset strategies
- Multiple network adapter support

## License

This project is open source and available under the MIT License.

## Disclaimer

This script requires administrator privileges to function properly as it needs to modify network interface settings. Use at your own risk.
