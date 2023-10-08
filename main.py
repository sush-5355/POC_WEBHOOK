# import re

# log_file_path = 'sample_log.txt'

# log_entries = []

# # Define a regular expression pattern to match log entries
# log_pattern = r'\[(.*?)\] (.*?)\s*:\s*(.*)'

# with open(log_file_path, 'r') as file:
#     for line in file:
#         # Match the log pattern using regular expressions
#         match = re.match(log_pattern, line)
#         if match:
#             timestamp, log_level, message = match.groups()
#             log_entry = {
#                 'timestamp': timestamp,
#                 'log_level': log_level,
#                 'message': message
#             }
#             log_entries.append(log_entry)

# # Now log_entries contains a list of dictionaries, each representing a log entry
# for entry in log_entries:
#     print(entry)
#######################################################


import os
import json
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

log_file_path = 'sample_log.txt'  # Replace with your log file path
json_output_file = 'log_entries.json'

# Define a regular expression pattern to match log entries
log_pattern = r'\[(.*?)\] (.*?)\s*:\s*(.*)'

# Initialize a list to store processed log entries
log_entries = []

# Function to parse a log line and convert it to a dictionary
def parse_log_line(line):
    match = re.match(log_pattern, line)
    if match:
        timestamp, log_level, message = match.groups()
        log_entry = {
            'timestamp': timestamp,
            'log_level': log_level,
            'message': message
        }
        return log_entry
    return None

# Function to write log entries to a JSON file
def write_log_entries_to_json():
    with open(json_output_file, 'w') as json_file:
        json.dump(log_entries, json_file, indent=4)

# Define a custom event handler for file changes
class LogFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == log_file_path:
            with open(log_file_path, 'r') as file:
                # Read the new lines added to the log file
                new_lines = file.readlines()[len(log_entries):]

                # Process and add new log entries to the list
                for line in new_lines:
                    log_entry = parse_log_line(line.strip())
                    if log_entry:
                        log_entries.append(log_entry)

                # Write the updated log entries to a JSON file
                write_log_entries_to_json()

# Start monitoring the log file for changes
event_handler = LogFileHandler()
observer = Observer()
observer.schedule(event_handler, path=os.path.dirname(log_file_path), recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
    observer.stop()

observer.join()
