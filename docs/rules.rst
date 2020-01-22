$ mklists run (the default)
  * For all datadirs
    * Change to rootdir
      * Run mklists, using
        * rules from current directory
        * rules from parent directories, if available - stopping at root

$ mklists run --here
  * For current datadir
      * Run mklists, using
        * rules from current directory
        * rules from parent directories, if available - stopping at root
  * If run in root directory, will exit with: "No data to process!".

. Tree 1: top is '/' (i.e., root directory of the _repo_)
├── .rules                    $ mklists run --here: "No data to process!"
├── a                         $ mklists run --here: uses /.rules a/.rules
│   ├── .rules                $
│   ├── a1                    $ mklists run --here: uses /.rules a/.rules a/a1/.rules
│   │   ├── .rules
│   │   └── c                 $ mklists run --here: uses /.rules a/.rules a/a1/.rules a/a1/c/.rules
│   │       └── .rules        $
│   └── a2                    $
│       └── .rules            $
├── b                         $ mklists run --here: uses /.rules b/.rules
│   └── .rules                $

. Tree 2: top is '/detached' (i.e., subdirectory under the root directory of the _repo_)
├── detached                  $ mklists run --here: uses detached/.rules: "No data to process!"
│   ├── .rules                $
│   ├── e                     $ mklists run --here: uses detached/.rules e/.rules
│   │   └── .rules            $
│   └── f                     $ mklists run --here: uses detached/.rules f/.rules
│       └── .rules            $
└── mklists.yml
