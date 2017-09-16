def is_utf8(file):
    class NotUTF8Error(SystemExit): pass
    try:
        open(file).read(512)
    except UnicodeDecodeError as e:
        raise NotUTF8Error(f'File {file} not UTF-8: convert or delete, then retry.') from e

