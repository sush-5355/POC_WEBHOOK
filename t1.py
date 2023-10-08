import os
import json
import re
import time

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

while True:
    # Check the modification time of the log file
    log_file_modification_time = os.path.getmtime(log_file_path)

    # If the modification time has changed, read and process new log entries
    if log_file_modification_time != getattr(
        write_log_entries_to_json, '_log_file_modification_time', None
    ):
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

        # Update the stored modification time
        write_log_entries_to_json._log_file_modification_time = log_file_modification_time

    time.sleep(1)  # Check for new entries every second
