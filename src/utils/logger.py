import logging
import os

def setup_logger(name):
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # Console Handler (prints to screen)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File Handler (saves to file)
        fh = logging.FileHandler(f"logs/{name}.log")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger