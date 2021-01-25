from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from colorama import Fore, Back, Style
import json
import click
import colorama

__author__ = "Matt Limb <matt.limb17@gmail.com>"

"""
The data field in _text, _json and _xml should be given in the following format:

{
    "type": "success|error|normal",
    "error": 0,
    "message": "Some message to show the user",
    "vault": null
    "data_about": "vault|group|folder|file"
    "seperate_data": true|false,
    "initial_line": true|false,
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

        self.format = format_.lower()

        self.output_functions = {
            "text": self._text,
            "txt": self._text,
            "stdout": self._text,
            "json": self._json,
            "xml": self._xml
        }

    def _text(self, data: dict) -> None:
        """Output to the terminal in the text format.

        Params:
        data : The data to be processed be shown to the User.
        """
        if data.get("type") == "error":
            out_colour = Fore.RED
        elif data.get("type") == "success":
            out_colour = Fore.GREEN
        else:
            out_colour = Fore.WHITE

        if data.get("message"):
            click.echo(f"{out_colour}{data.get('message')}")
            Style.RESET_ALL
        
        if data.get("initial_line"):
            click.echo("")
        
        if data.get("data"):
            for item in data.get("data"):
                if data.get("seperate_data", False):
                    click.echo("")
                    
                for key, value in item.items():
                    click.echo(f"{out_colour}{key}{' '*(15-len(key))}: {value}")

    def _json(self, data:dict) -> None:
        """Output to the terminal in the JSON format.

        Params:
        data : The data to be processed be shown to the User.
        """
        
        if data.get("type"):
            del data["type"]
        
        if data.get("seperate_data"):
            del data["seperate_data"]

        new_data = []

        for item in data.get("data"):
            new_item = {}
        
            for key, value in item.items():
                new_item[key.lower().replace(" ", "_")] = str(value)
        
            new_data.append(new_item)

        data["data"] = new_data
        
        click.echo(json.dumps(data, indent=2))

    def _xml(self, data:dict) -> None:
        """Output to the terminal in the XML format.

        Params:
        data : The data to be processed be shown to the User.
        """
        output = Element("vault_output")

        err = SubElement(output, "error")
        err.text = str(data.get("error"))
        
        message = SubElement(output, "message")
        message.text = str(data.get("message"))
        
        if data.get("vault"):
            vault = SubElement(output, "vault")
            vault.text = str(data.get("vault"))
      
        if ( data.get("data") ) and ( len(data.get("data")) != 0 ) and ( data.get("data_about") ):
            data_elm = SubElement(output, "data")
            data_about = data.get("data_about")

            for item in data.get("data"):
                new_item = SubElement(data_elm, data_about)

                for key, value in item.items():
                    sub_elm = SubElement(new_item, key.lower().replace(" ", "_"))
                    sub_elm.text = str(value)

        as_str = tostring(output, "utf-8").decode() 
        click.echo(minidom.parseString(as_str).toprettyxml(indent="  "))

    def write(self, data:dict) -> None:
        """Write the data to the terminal in the right format.

        Params:
        data : The data to be processed be shown to the User.
        """
        if self.format in self.output_functions.keys():
            self.output_functions[self.format](data)
        else:
            raise VaultVauleError("Error: Given output format is not supported in Vault", data.get("vault"))


class VaultVauleError(ValueError):
    """The base Vaule Error for Vault
    """
    def __init__(self, message, vault):
        """Override the base exception to do our own thing.
        """
        super().__init__(message)

        Outputs().write({
            "error": 10,
            "message": message,
            "vault": vault            
        })
