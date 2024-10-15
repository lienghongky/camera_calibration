import os
import time

# Path to your dataset
dataset_path = '/data/dataset/cam1'  # Update this to your dataset's path
# Set starting timestamp (in seconds since epoch)
start_time = time.time()

# Define the time interval between consecutive files (e.g., 0.1 seconds between images)
time_interval = 0.1  # Adjust as needed

# Get the list of files in the directory
files = sorted(os.listdir(dataset_path))
print("Found {} files.".format(len(files)))
# Loop through the files and rename them

for i, file in enumerate(files):
    # Calculate the timestamp for each file
    timestamp = start_time + (i * time_interval)
    # Convert timestamp to integer (seconds) and nanoseconds
    secs = int(timestamp)
    nsecs = int((timestamp - secs) * 1e9)
    
    # Create new filename with timestamp
    new_filename = "{}.png".format(secs+i)  # Use the appropriate extension for your images

    # Full paths for renaming
    old_file_path = os.path.join(dataset_path, file)
    new_file_path = os.path.join(dataset_path, new_filename)

    # Rename the file
    os.rename(old_file_path, new_file_path)

    print('Renamed {} to {}'.format(file, new_filename))

print("Renaming complete.")
