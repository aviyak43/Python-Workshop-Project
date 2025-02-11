import logging

# configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("project.log"), logging.StreamHandler()],
)
# Get the root logger
logger = logging.getLogger()
