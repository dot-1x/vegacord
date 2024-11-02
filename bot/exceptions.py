class MemberAlreadyChangedError(Exception):
    """exception class for member already changed"""

    ...


class MemberUnchanged(Exception):
    """Exception class if member is filling the same data as before"""
