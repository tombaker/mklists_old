### Pseudocode for mklists.py

    Check whether mklists directory
        Has .rules.yaml file?
        Has .mklists.yaml file?
        For each visible file (ignoring directories):
            plain text?
            no spaces in filename?

    Read .mklists.yaml

    Read .rules.yaml
        for each line
            strip comments ('#')                          - or will a YAML library take care of this?
            ignore empty lines and all-whitespace lines
