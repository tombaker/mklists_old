def get_globlines(cwd=os.getcwd()):
    """Something like:
    globlines_list = []
    for file in glob.glob('*'):
        globlines_list.append(file.readlines())
    return globlines_list
    """
    return cwd

if __name__ == "__main__":
    get_globlines()
