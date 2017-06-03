The idea for what is now called `mklists` dates back to 1993, and I have been
using the script in various incarnations almost every day, sometimes every hour
since then.  Since the script processes plain-text lists

The [mklists project](http://github.com/tombaker/mklists) aims at implementing
the latest iteration of a script first published:
* in 1994 as
  [`shuffle`](http://web.archive.org/web/20080807155330/http://web.bilkent.edu.tr/Online/uworld/archives/94/grabbag/06.lst.html#L1A),
  a Korn shell script based extensively on `grep`, which was which was featured in a 
  [column by Becca Thomas in UnixWorld](http://web.archive.org/web/20080513171823/http://web.bilkent.edu.tr/Online/uworld/archives/94/grabbag/06.txt.html).
  `shuffle` was written using the MKS Toolkit, a Unix shell environment, running on DOS 3.3.
* in 2006 as [`shawkle`](history/shawkle.md), which improved on `shuffle` by using `awk` for field-based pattern matching 
  (hence: `shawkle`).  This iteration of the program was featured in [lifehacker.com](http://lifehacker.com/217063/getting-things-done-with-rule+based-list-processing)
  with an introduction by Gina Trapani.
* starting in 2011, as [`shawkle.py`](https://github.com/tombaker/shawkle/blob/master/shawkle.py), 
  a re-write of the `shawkle` idea in Python, partly with the aim of teaching myself Python.

The 2012 Python script introduced the idea of automating the movement of list
items between folders according to rules.
[`shuffle.py`](https://github.com/tombaker/shawkle/blob/master/shuffle.py), is
stable, orders of magnitude faster its shell-based predecessors, and I still
use it every day for my work.  Over the years I have had to patch it only two
or three times to handle edge cases.  

The idea of re-implementing the `shawkle` idea under the name `mklists`, with a
proper test suite and documentation, was inspired by reading David Copeland's
excellent _Build Awesome Command-Line Applications in Ruby_ in 2012.  Seeing
this as an opportunity to learn Ruby, I made some progress on aspects of
`mklists.rb` as a back-burner project.  This work, along with work on the
Python version using test-driven development with `py.test`, proceeded at a low
level, as time allowed, in previous incarnations of the [`mklists` Github
repo](https://github.com/tombaker/mklists).

In June 2017, my discovery of the excellent (and fortuitously named) static
site generator [`MkDocs`](https://github.com) gave me a day-job-related reason
to re-start the Github repo, in the spirit of "documentation-driven
development", with its own website.

