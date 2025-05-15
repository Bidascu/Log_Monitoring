# ---------------------------------------------------------------------------
#
# Title: Log Monitoring Application
# Date: 15/05/2025
# Version: 2.0
# Author: Bidascu Denis
#
# Purpose: This script is used to monitor logs and check the status of jobs.
#
# Command to run: python path/to/log_monitor.py <path_logs> <path_job_status>
#
# ---------------------------------------------------------------------------
import re
import os
from datetime import datetime
import sys

if len(sys.argv) < 3:
    print("Usage: python log_check.py <path_job_status> <path_logs> \n"
          + "<path_job_status> - Enter the path to the job status file (default: job_status.txt)\n"
          + "<path_logs> - Enter the path to the log file (default: logs.log)")
    sys.exit(1)

# Define regex pattern of the log: Timestamp, Job Description, Start or End, PID
pattern = r'(\d{2}:\d{2}:\d{2}),(.+?), (START|END),(\d+)'

# Paths to the log file and job status file
path_logs = sys.argv[1]
path_job_status = sys.argv[2]

# Open or create the job status file
with open(path_job_status, 'w') as f:
    f.write("Job Status\n")
    f.write("-" * 91 + "\n")

# Read the log file line by line
with open(path_logs, 'r') as file:
    logs = file.readlines()

# Loop to find START entries
    for i, log in enumerate(logs):

        # Check if the log matches the pattern
        match = re.match(pattern, log)
        if match:
            timestamp, job_description, status, pid = match.groups()

            # Look for the START entry
            if status == 'START':
                # Loop through the logs to find the corresponding END entry
                for j in range(i + 1, len(logs)):
                    log_aux = logs[j]

                    # Store the END entry
                    task_completed = re.match(pattern, log_aux)
                    if task_completed:
                        timestamp1, job_description1, status1, pid1 = task_completed.groups()
                        
                        # Check for END of the job and time taken. - Store the logs accordingly
                        if status1 == 'END' and job_description1 == job_description and pid1 == pid:
                            with open(path_job_status, 'a') as f:
                                f.write("\n" + f"Job Description: {job_description}, PID: {pid} | "
                                        + f"{status} Time: {timestamp} & {status1} Time: {timestamp1}\n")
                            time_diff = datetime.strptime(timestamp1, '%H:%M:%S') - datetime.strptime(timestamp, '%H:%M:%S')
                            total_time = time_diff.total_seconds()/ 60
                            if total_time > 10:
                                with open(path_job_status, 'a') as f:
                                    f.write(f"Error  : Job took longer than 10 minutes! Time taken: {time_diff} minutes\n")
                            elif total_time > 5:
                                with open(path_job_status, 'a') as f:
                                    f.write(f"Warning: Job took longer than 5 minutes!  Time taken: {time_diff} minutes\n")
                            else:
                                with open(path_job_status, 'a') as f:
                                    f.write(f"Success: Job completed.                   Time taken: {time_diff} minutes\n")
                            with open(path_job_status, 'a') as f:
                                f.write("-" * 91 + "\n")

# End of the job status file
with open(path_job_status, 'a') as f:
    f.write("End of Job Status")