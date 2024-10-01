"""Custom Password Option which doesn't confirm."""

import click
from click.decorators import t, FC


def password_option(*param_decls: str, **kwargs: t.Any) -> t.Callable[[FC], FC]:
    """Add a ``--password`` option which prompts for a password, hiding
    input and asking to enter the value again for confirmation.

    :param param_decls: One or more option names. Defaults to the single
        value ``"--password"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
    """
    if not param_decls:
        param_decls = ("--password",)

    kwargs.setdefault("prompt", True)
    kwargs.setdefault("hide_input", True)
    return click.option(*param_decls, **kwargs)
