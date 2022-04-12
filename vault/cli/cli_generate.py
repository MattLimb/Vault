import hashlib
import pathlib
import string
import random
import uuid
import click

from .cli_outputs import Outputs
from vault.hash import HashTool
from vault.encryption import Encryption

__author__ = "Matt Limb <matt.limb17@gmail.com>"

@click.group("generate", help="Some useful static tools.")
def generate():
    """Command group for the generate command collection. Cannot be executed by itself.
    """
    pass

@generate.command("password", help="Generte a random secure password.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="TEXT", help="Enable debug mode")
@click.argument("length", default=20, type=int)
def generate_password(length, debug, output):
    """Generate a random password.

    Options:
    -d/--debug  : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.

    Arguments:
    length : The Length the password should be in characters. Defaults to 20.

    Returns:
    The randomly generated password as a string.
    """
    
    new_password = ""
    choice_string = random.choice(
        [
            f"{string.ascii_letters}{string.punctuation}",
            string.ascii_letters
        ]
    )
    
    for _ in range(length+1):
        new_password += random.choice(choice_string)

    Outputs(format_=output.lower()).write(dict(
        type="normal",
        error=0,
        message=new_password
    ))

@generate.command("uuid", help="Generte a random uuid.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="TEXT", help="Format to output to the terminal in")
def generate_uuid(debug, output):
    """Generate a random uuid.

    Options:
    -d/--debug : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.

    Returns:
    The randomly generated uuid as a string.
    """
    Outputs(format_=output.lower()).write(dict(
        type="normal",
        error=0,
        message=str(uuid.uuid4())
    ))


@generate.command("encryption-key", help="Generte a random encryption key.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="TEXT", help="Format to output to the terminal in")
def generate_encryption_key(debug, output):
    """Generate a random encryption key.

    Options:
    -d/--debug : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.

    Returns:
    The randomly generated encryption key as a string.
    """
    Outputs(format_=output.lower()).write(dict(
        type="normal",
        error=0,
        message=str(Encryption.generate_key().decode())
    ))

@generate.command("hash", help="Generte a hash of a file or string.")
@click.option("-f", "--file", "input_type", flag_value="file", help="The given string is a filename.")
@click.option("-s", "--string", "input_type", flag_value="string", help="The given string is a string.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="TEXT", help="Format to output to the terminal in")
@click.argument("algorithm", nargs=1, type=str)
@click.argument("input", nargs=-1, type=str)
def generate_hash(input_type, algorithm, input, debug, output):
    """Generate a hash from a string or filepath.

    Options:
    -d/--debug : Enable debug mode for more information.
    -f/--file  : The given strings are filenames.
    -s/--string: The given string are strings.
    -o/--output : The format to output to the terminal in.

    Arguments: 
    algorithm : The hashing algorithm to use
    input     : The file to hash, or the string to hash

    Returns:
    The hash of the string or filepath.
    """
    if algorithm not in hashlib.algorithms_available:
        Outputs(format_=output.lower()).write(data=dict(
            type="error",
            error=0,
            message=f"Error: {algorithm.upper()} is not supported"
          ))
        quit(1)

    for some_input in input:
        h = HashTool(algorithm, vault=None)
        hash_function = h.hash_string

        if input_type == "file":
            hash_function = h.hash_file
        elif input_type == "string":
            hash_function = h.hash_string
        else:
            if pathlib.Path(some_input).exists():
                hash_function = h.hash_file
            
        Outputs(format_=output.lower()).write(data=dict(
            type="normal",
            error=0,
            message={ algorithm.upper() : hash_function(some_input) }
          ))