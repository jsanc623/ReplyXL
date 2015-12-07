"""
ConfigWrapper
"""
import json
import os
import sys

class ConfigWrapper(object):
    """
    ConfigWrapper
    This class contains methods for loading configuration files and settings
    into various levels of our application.
    """
    env = None

    @staticmethod
    def load_env_var(key=None):
        """
        load_env_var()
        This method will check for an environment variable and return the value
        :param key:
        """
        env_var = None

        try:
            env_var = os.environ[key]
        except Exception as app_exception:
            print "Error Retrieving Environment Variable - " + \
            key + " => " + app_exception.message

        return env_var

    @staticmethod
    def load_config(file_name, key=None):
        """
        load_config()
        @retun - Definition
        This method will attempt to load a JSON config file, convert it to JSON and return the Definition
        :param key:
        :param file_name:
        """
        data = {}

        try:
            tmp_file = json.loads(open(file_name).read())
            for env in tmp_file:
                if key and key in tmp_file:
                    data = tmp_file[key]
                else:
                    data = tmp_file[env]
        except IOError:
            print "File can't be found"
        except Exception as app_exception:
            print "Error Parsing Config File => " + str(file_name) + " - " + app_exception.message

        return data

    def set_environment(self, override=None):
        """
        set_environment()
        @retun - string [environment name for modules to inherit]
        This method will parse the command line arguments for a value matching this pattern "--env=WORD"
        and will then set that value as our environment setting for the modules to inherit
        :param override:
        """
        if override is None:
            environment = "TEST"

            if len(sys.argv) > 1:
                for item in sys.argv:
                    env_value = self.parse_environment(item)
                    if env_value is not None:
                        environment = env_value
        else:
            environment = override

        return environment

    @staticmethod
    def parse_environment(key):
        """
        parse_environment()
        @retun - string [environment name for modules to inherit]
        :param key:
        """
        parsed_value = None
        prefix = "--env="
        env_keys = ['DEVELOPMENT', 'WORKINGDEV', 'TEST', 'STAGING', 'SANDBOX', 'PREPROD', 'PRODUCTION', 'QA']

        stripped = key.replace(prefix, "")
        if prefix in key and stripped in env_keys:
            parsed_value = stripped

        return parsed_value

    def get_environment(self):
        """
        get_environment()
        @param - self [python reference]
        @retun - string [environment name for modules to inherit]
        If no environment is set then set one and return it.
        """
        if self.env is None:
            self.env = self.set_environment()

        return self.env