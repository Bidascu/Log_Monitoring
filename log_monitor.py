# ---------------------------------------------------------------------------
#
# Title: Log Monitoring Application
# Date: 14/05/2025
# Version: 1.0
# Author: Bidascu Denis
#
# Purpose: This script is used to monitor logs and check the status of jobs.
# Command to run: python path/to/log_monitor.py
#
# ---------------------------------------------------------------------------
import re
import os

# Define regex pattern of the log: Timestamp, Job Description, Start or End, PID
pattern = r'(\d{2}:\d{2}:\d{2}),(.+?), (START|END),(\d+)'

with open('./logs.log', 'r') as file:
    logs = file.readlines()
    # Read the log file line by line
    for log in logs:
        i = 0
        match = re.match(pattern, log)
        if match:
            timestamp, job_description, status, pid = match.groups()
            print(f"Timestamp: {timestamp}, Job Description: {job_description}, Status: {status}, PID: {pid}")
# Check Job Start and End time, based on that check the duration of the job
