from colorama import Fore, Back, Style
import json
import click

"""
The data field in _text, _json and _xml should be given in the following format:

{
    "type": "success|error|normal",
    "message": "Some message to show the user",
    "data": [
        {
            "keys": "values"
        }
    ]
}
"""

class Outputs:
    """An class to handle outputting data to the terminal in different formats.
    """
    def __init__(self, format_="text"):
        """Init method to setup the class

        Params:
        format : The format to output to the terminal in.
        """

        self.format = format_

    def _text(self, data: dict) -> None:
        """Output to the terminal in the text format.

        Params:
        data : The data to be processed be shown to the User.
        """
        
        pass

    def _json(self, data:dict) -> None:
        """Output to the terminal in the JSON format.

        Params:
        data : The data to be processed be shown to the User.
        """
        pass

    def _xml(self, data:dict) -> None:
        """Output to the terminal in the XML format.

        Params:
        data : The data to be processed be shown to the User.
        """
        pass

    def write(self, data:dict) -> None:
        """Write the data to the terminal in the right format.

        Params:
        data : The data to be processed be shown to the User.
        """
        pass