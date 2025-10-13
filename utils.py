import logging

USER = "root"
PASSWORD = "shashank935"

logger = logging.getLogger(__name__)
logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s: %(message)s')
