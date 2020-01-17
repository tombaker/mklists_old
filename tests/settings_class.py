class Settings:
    """Holds settable settings."""

    # pylint: disable=too-few-public-methods
    # It is not unreasonable to use a class instance as a namespace.

    def __init__(self):
        self.invalid_filename_regexes_list = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
        self.verbose = True
        self.htmlify = True
        self.backup_depth_int = 3
        self.files2dirs_dict = {}


settings_dict = vars(Settings())
