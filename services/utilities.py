from random import choice

from services.config import Config

config = Config().get_config()


class Utilities:

    @staticmethod
    def generate_secret():
        """
        Creates a secret-key based on the character-set passed by the configuration.
        Returns a string.

        :return: String, secret-key
        """
        result = ""
        for i in range(0, config.security.secret_length):
            result += choice(config.security.character_list)
        return result
