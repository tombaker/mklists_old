class ListFolder:

    def __init__(*kwargs):
        pass

    def ls_visible_files(folder='.'):
        visible_files = [name for name in glob.glob('*')
                         if os.path.isfile[name]]
        return visible_files


@dataclass
class ListFile():
    file = click.Path
    # is_utf8_encoded()
    # file has legal name (only allowable characters - e.g., no spaces)
    # is_text (implement this?)
    #   allowable_percent_non_ascii_characters
    #   return True or False
    # return { file: [['one line\n'], [...]] }
