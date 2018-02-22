import os

from dotenv import load_dotenv


class Config(dict):
    def __init__(self):
        self['SESSION_TYPE'] = 'filesystem'


class ConfigDev(Config):
    """
    Class to load development secrets
    from local file .env located in root of project.
    """

    def __init__(self):
        super(ConfigDev, self).__init__()

        # root of project is one dir earlier
        root_path = os.path.dirname(os.path.abspath(__file__))[:-3]

        # dotenv will parse the .env file and add everythong to env vars
        dotenv_path = os.path.join(root_path, '.env')
        load_dotenv(dotenv_path)

        # iterate over env files and add them to self
        for k, v in os.environ.iteritems():
            self[k] = v


class ConfigProd(Config):
    """
    Class to load production configs from environment variables.
    This is to work with Heroku, where secrets are added as env vars.
    """

    def __init__(self):
        super(ConfigProd, self).__init__()

        # iterate over env files and add them to self
        for k, v in os.environ.iteritems():
            self[k] = v
