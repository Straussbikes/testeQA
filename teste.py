
import argparse
import hashlib
import logging
import os
import shutil
# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handlers
file_handler = logging.FileHandler('sync.log')
console_handler = logging.StreamHandler()

# Set the level for each handler
file_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for each handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def calculate_md5(file_path):
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

def sync_folders(source_folder, replica_folder):

    source_files = {os.path.relpath(os.path.join(dirpath, f), source_folder): calculate_md5(os.path.join(dirpath, f))
                    for dirpath, _, files in os.walk(source_folder) for f in files}

    replica_files = {os.path.relpath(os.path.join(dirpath, f), replica_folder): calculate_md5(os.path.join(dirpath, f))
                    for dirpath, _, files in os.walk(replica_folder) for f in files}

    # Copy files from source to replica
    for relative_path, md5 in source_files.items():
        source_path = os.path.join(source_folder, relative_path)
        replica_path = os.path.join(replica_folder, relative_path)
        if relative_path not in replica_files:
            os.makedirs(os.path.dirname(replica_path), exist_ok=True)
            shutil.copy2(source_path, replica_path)
            logger.info(f"File copied: {relative_path}")
            print(f"File copied: {relative_path}")
        elif md5 != replica_files[relative_path]:
            shutil.copy2(source_path, replica_path)
            logger.info(f"File updated: {relative_path}")
            print(f"File updated: {relative_path}")

    # Delete files from replica that are not in source
    for relative_path in replica_files.keys():
        if relative_path not in source_files:
            replica_path = os.path.join(replica_folder, relative_path)
            os.remove(replica_path)
            logger.info(f"File deleted: {relative_path}")
            print(f"File deleted: {relative_path}")
def main():

    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler('sync.log')
    console_handler = logging.StreamHandler()

    # Set the level for each handler
    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.INFO)

    # Create a formatter and set it for each handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    parser = argparse.ArgumentParser(description="Example script that receives arguments from the console")

    parser.add_argument('pathoriginal', type=str, help='The original folder path')
    parser.add_argument('pathclone', type=str, help='The clone folder path')
    parser.add_argument('--synctime', type=int, default=60, help='the time of sync')
    parser.add_argument('--logfilepath', type=str, default='sync.log', help='the place where u can see creation copy or removal')

    args = parser.parse_args()
    synctime=args.synctime
    timecount=synctime
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logging.getLogger().addHandler(console_handler)

    logger.info("Starting the sync process")

    try:
        while True:
            sync_folders(args.pathoriginal, args.pathclone)
            
    except KeyboardInterrupt:
        logger.info("Sync process interrupted by user")

    while(True):
        time=synctime
        if(timecount==0):
            sync_folders(args.pathoriginal,args.pathclone)
            logger.info("time refreshed")
            time=time-1
        

if __name__ == "__main__":
    main()
