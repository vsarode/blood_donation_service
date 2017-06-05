from donation_service.conf.environment import get_config
import os


def set_config(app):
    app.secret_key = "2421da99-1770-4949-90a0-71c09d409fbb"
    blood_env = os.environ.get('BLOOD_ENV', 'dev')
    config = get_config(blood_env)
    app.config.from_object(config)
    app.logger.info("Loaded environment: " + blood_env)
    return
