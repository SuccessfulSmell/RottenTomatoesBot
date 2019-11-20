import logging

logging.basicConfig(level=logging.INFO,
                    filename='./logs/debug.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
