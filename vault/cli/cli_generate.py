import click

__author__ = "Matt Limb <matt.limb17@gmail.com>"

@click.group("generate", help="Some useful static tools.")
def generate():
    """Command group for the generate command collection. Cannot be executed by itself.
    """
    pass

@generate.command("password", help="Generte a random secure password.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), help="Enable debug mode")
@click.argument("length", default=20, type=int)
def gen_password(length, debug, ouput):
    """Generate a random password.

    Options:
    -d/--debug  : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.

    Arguments:
    length : The Length the password should be in characters. Defaults to 20.

    Returns:
    The randomly generated password as a string.
    """
    pass

@generate.command("uuid", help="Generte a random uuid.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="TEXT", help="Format to output to the terminal in")
def uuid(debug, output):
    """Generate a random uuid.

    Options:
    -d/--debug : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.

    Returns:
    The randomly generated uuid as a string.
    """
    pass


@generate.command("encryption-key", help="Generte a random encryption key.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="TEXT", help="Format to output to the terminal in")
def encryption_key(debug, output):
    """Generate a random encryption key.

    Options:
    -d/--debug : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.

    Returns:
    The randomly generated encryption key as a string.
    """
    pass

@generate.command("hash", help="Generte a hash of a file or string.")
@click.option("-f", "--file", is_flag=True, help="The given string is a filename.")
@click.option("-s", "--string", is_flag=True, help="The given string is a string.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="TEXT", help="Format to output to the terminal in")
@click.argument("algorithm", nargs=1, type=str)
@click.argument("input", nargs=-1, type=str)
def encryption_key(file, string, algorithm, input, debug, output):
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
    pass
