import logging
import os

#Function to obtain the API Credentials stored in pem files
def obtain_keys():
    with open("api_key.pem", "r") as f: # Location of private key file
        api_key = f.read()
    with open("api_secret.pem", "r") as f: # Location of secret key file
        secret_key = f.read()

    print("Keys obtained successfully.")
    return api_key, secret_key

#Function to setup logging
def setup_logging():
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_directory, "trading_bot.log")),
            logging.StreamHandler() # Also print to console
        ]
    )
    logging.getLogger('urllib3').setLevel(logging.WARNING) # Suppress urllib3 logs
    logging.getLogger('asyncio').setLevel(logging.WARNING) # Suppress asyncio logs