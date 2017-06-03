```
#!/bin/pdksh
# @(#) shawkle  A rule-based list processor
# Author: Thomas Baker <tbaker@unix.amherst.edu> (1994)
#                      <thomas.baker@bi.fhg.de> (2002)
# 
# Based on program "shuffle", originally published in 1994 as
#    "Shuffle: a rule-based list processor" in: Thomas, Rebecca, 
#    "The data shuffle" [monthly column ``Wizard's Grabbag''],
#    UnixWorld Open Computing} 11(6), pp. 123-127.
#
# 1995:       Further modified by author:
#             Uses "gawk" instead of "grep" in the main
#             function (movelines), allowing rules to specify matches to *fields*.
# 1995-10-02: Added "data" in filetype detection line because file sees umlauts as "data"
#       Changed: { file $File | grep -E 'data|text|empty|shell' >|$Devnull 2>&1;} ||
# 1999-09-03: Appended urlify-lists functionality
# 2000-01-18: Added modules at end to move various files to other directories
# 2002-01-16: Further configured for Voltimand (Dell laptop)
# 2002-04-04: Unix and Unix-under-Windows variables separated for clarity
#             Now MKS and Cygwin support "hidden" .filenames (starting with "dot")
# 2002-06-17: Ported shawkle from MKS to Cygwin
#             1c1        # CHANGED MKS/ksh to AST/ksh
#             < #!e:/mks/mksnt/sh.exe
#             > #!/ast/bin/ksh
#             75c75      # egrep -> grep -E
#             < egrep -v '^$' |                     # Remove blank lines.
#             > grep -Ev '^$' |                     # Remove blank lines.
#             123c123      # egrep -> grep -E
#             <     { file $File | egrep 'data|text|empty|shell' >|$Devnull 2>&1;} ||
#             >     { file $File | grep -E 'data|text|empty|shell' >|$Devnull 2>&1;} ||
#             125c125      # egrep -> grep -E
#             <     egrep '^[   ]*$' $File >|$Devnull 2>&1 &&
#             >     grep -E '^[   ]*$' $File >|$Devnull 2>&1 &&
#             141c141      # egrep -> grep -E
#             < egrep -v '^$' |                     # Remove blank lines
#             > grep -Ev '^$' |                     # Remove blank lines
#             173c173
#             < e:/u/bin/urlify-lists 1>>$NULL &
#             > /cygdrive/e/u/cygbin/urlify-lists 1>>$NULL &
# 2002-06-17: Added "game" in filetype detection line because file sees some lines as "game dumps"
#             { file $File | grep -E 'data|text|empty|shell|game' >|$Devnull 2>&1;} ||
# 2003-05-11: Added /cygdrive/a/u/lines/agenda/.rulesall, called $Rulesall below.
#             This implies at a minimum that every shawkle directory will use
#             the default name "lines" and that the $Rulesall rules will apply to the
#             data in every directory where shawkle is run.
# 2003-05-22: Added flip -ub to make sure everything is in Unix text format.
# 2003-10-20: Cygwin now has pdksh, so now use instead of AST KSH
# 2003-11-03: Changed "file" to "file -i" to ensure that text is seen as text, in line:
#             Change: { file -i $File | grep -E 'data|text|empty|shell|game' >|$Devnull 2>&1;} ||
#             To:     { file -i $File | grep -E 'text|empty' >|$Devnull 2>&1;} ||
# 2003-11-08: DANGER!  Need to add new sanity check for .rule file, somthing like:
#             toupper($3) == toupper($4) { print $0, ": ", $3, "and", $4, "same under WIN2000!" 
#             Problem: a rule like "0|KEYWORD|Filename|FILENAME|' will quickly generate
#             a runaway process, filling up the hard disk (400+ MB in just 10-15 seconds...)
#             and can only be stopped by Ctrl-C!
# 2004-09-09 "file -i" option makes "file" use an alternative magic file!
#             This makes it interpret an "ASCII text" starting with "MMI " as "image/tiff"!
#             Solution for now: use "DCMMI" as keyword.
# 2006-06-16  This slighly pared-down, cleaned-up version prepared for Gina Trapani
#
# To configure for a particular system, edit the following
# -- First line (#!e:/mks/mksnt/sh.exe or #!/bin/ksh as needed)
# -- Configuration variables (possibly commenting out Unix-under-Windows variables)
# -- Appendix 1: calls "urlify-lists" to create parallel directory with .html lists:
#    For each $LISTS/agenda*, creates $LISTS/_html/html-agenda*
#    Comment out Appendix 1 or install/configure "urlify-lists" script
#    Note that "urlify-lists" calls the script "urlify", which must itself be configured
# -- Appendix 2: moves various files to other directories as needed
#    Comment out Appendix 2 or configure as needed

$DBG_SH                             # Dormant debugging directive
umask 077

trap 'rm -f $Tmpfile $Targetfilenames >|$Devnull 2>&1; \
    exit $Stat' 0
trap 'print -u2 "$(basename $0): Interrupted!"; exit' 1 2 3 15

# CONFIGURATION
Allfiles=combined.dat               # File for all catenated input files
Bkupdir=.backup                     # Input-files backup directory
Devnull="/dev/null"                 # Bit-bucket file
Rulefile=.rules                     # Local rule file
Ruleall=.ruleall                    # Global rule file (added 2003-05-11)
Usage="Usage: $(basename $0) datafile [datafile ...]" # Correct usage
Tmpdir=/tmp                         # Temporary directory
Targetfilenames=$Tmpdir/sht$$.tmp   # Target-names file (uses $Tmpdir)
Tmpfile=$Tmpdir/shf$$.tmp           # Temporary work file (uses $Tmpdir)

# UNIX-UNDER-WINDOWS CONFIGURATION: comment out if using Unix/Linux
Tmpdir=c:/cygwin/tmp                # MKS/Unix temporary directory
Devnull=$Tmpdir/null                # Bit-bucket file, alternative (using $Tmpdir)

# FUNCTION DEFINITIONS:
function usage_exit {
    print -u2 "$Usage"; Stat=1 ; exit
}
function movelines { # Args: $Searchfield $Searchkey $Source $Target $Sortcmd
#    print -n "Lines with [$2] in field $1 moved from \""$3"\" to \""$4"\""
    print -n "$1 [$2] \""$3"\" to \""$4"\""
    #egrep "$2" $3 >>$4; egrep -v "$2" $3 >|$Tmpfile; mv $Tmpfile $3
	gawk '$'$Searchfield' ~ /'$Searchkey'/' $3 >>$4
	gawk '$'$Searchfield' !~ /'$Searchkey'/' $3 >|$Tmpfile; mv $Tmpfile $3
    [ "$5" ] && print ", ${5}." || print "." # Print sort command
    [ "$5" ] && { eval $5 -o $4 $4 ||
        { print "\aBad rule-file sort command: $5"; Stat=2; exit;};}
}

# PROCESS COMMAND-LINE ARGUMENTS:
case $# in      # User must specify at least one file-name argument
    0)  usage_exit ;;
esac

# SANITY CHECK: Rule file:
[ -r $Ruleall ] ||
    { print -u2 "\aCannot read \"$Ruleall\" file!"; Stat=4; exit;}
[ -r $Rulefile ] ||
    { print -u2 "\aCannot read \"$Rulefile\" file!"; Stat=4; exit;}
sed 's/#.*$//' $Ruleall $Rulefile | # Remove comments.
grep -Ev '^$' |                     # Remove blank lines.
gawk -F\| '                         # Rules separated by vertical bar
NR == 1 && ($2 != "." || $3 != "$Allfiles") {   # Check first rule
    print $0, ": rule 1 is illegal!" }
NF != 4 && NF != 5 {                # All rules have 4 or 5 fields.
    print $0, ": must have 4 or 5 fields!" }
$3 == $4 {                          # Source different from target.
    print $0, ": source cannot equal target!" }
$5 != "" && $5 !~ /^sort/ {         # Field 5 is for sort commands.
    print $0, ": field 5 is only for sort!" }
$1 == "" || $2 == "" || $3 == "" || $4 == "" {  # First four fields non-empty.
    print $0, ": 1 of first four fields is empty!" }
{ target[$4] = 1 }                  # Note names of target files
NR > 1 {                            # For all lines after the first
    if ($3 in target)               # If source file is also a target
        next;                       # No problem, fetch next input line
    else print $0, ": ", $3, "has no precedent!"
}' >| $Tmpfile                      # Save unique lines and display
[ -s $Tmpfile ] &&
    { print -u2 "Bad rule format:\n$(cat $Tmpfile)"; Stat=5; exit;}

# SANITY CHECKS: Current directory, combined data, backup directory:
[ -w "." ] ||                       # Current (data) directory
    { print -u2 "\aCannot write to current directory!"; Stat=6; exit;}
[ -f $Allfiles ] &&                 # Combined data file
    { print -u2 "\a\"$Allfiles\" should not yet exist!"; Stat=7; exit;}
[ -d $Bkupdir ] || mkdir $Bkupdir 2>|$Devnull ||
    { print -u2 "\aCannot make directory \"$Bkupdir\"!"; Stat=8; exit;}
[ "$(ls $Bkupdir)" ] && {           # if there are files in backup dir
# Note: Following line commented out and ans="y" added.
# print -n "Okay to replace files in $Bkupdir (y*|Y*/n)? "; read ans
ans="y"
case $ans in
    y*|Y*)  rm -f $Bkupdir/* >|$Devnull 2>&1 ;; # Remove old backups
    *)      print "Exiting, check $Bkupdir directory."; Stat=0; exit ;;
esac;}

# CHECK DATA FILES, BACK UP, THEN COMBINE INTO A COMMON FILE:
for File in "$@"; do
    [ -d $File ] && continue                # Ignore directories.
    [ "$File" = "$Rulefile" ] && continue   # Ignore rules (just data).
    [ "$(dirname $File)" = "." ] || [ "$(dirname $File)" = "$PWD" ] ||
        { print -u2 "\aData files must be in current directory!"
        Stat=9; exit;}
    [ -r $File ] ||
        { print -u2 "\a\"$File\" file not readable."; Stat=10; exit;}
    { file -i $File | grep -E 'text|empty' >|$Devnull 2>&1;} ||
        { print -u2 "\a\"$File\" not text nor empty."; Stat=11; exit;}
    grep -E '^[   ]*$' $File >|$Devnull 2>&1 &&
        { print -u2 "\a\"$File\" has blank lines!"; Stat=12; exit;}
    cp $File $Bkupdir ||    # Copy to backup directory.
        { print -u2 "\aCannot back up $File!"; Stat=13; exit;}
    cat $File >> $Allfiles; rm $File   # Combine into common file.
done

# CHECK COMBINED DATA FILE:
[ -s $Allfiles ] || { print -u2 "\aNo data to process!"; Stat=14; exit;}
flip -ub $Allfiles # Added 2003-05-22
Beforesize=$(wc -c <$Allfiles | gawk '{ print $1 }') # Data size before
print "Data backed up to \"$Bkupdir\", concatenated in \"$Allfiles\"."

# PROCESS DATA FILES under direction of rule file:
OldIFS="$IFS"               # Save old internal field separator char(s)
IFS="|"                     # Rule-file field separator for "read"
sed 's/#.*$//' $Ruleall $Rulefile | # Remove rule-file comments
grep -Ev '^$' |                     # Remove blank lines
while read Searchfield Searchkey From To Sortcmd ; do # fields into variables
    eval Source=$From; eval Target=$To      # interpolate these var.
    movelines $Searchfield $Searchkey $Source $Target $Sortcmd # Do the shuffle
    print -u3 "$Target"             # Output goes to fd 3.
done 3>| $Targetfilenames           # Store fd3 output in a file.
IFS="$OldIFS"                       # Restore original IFS values.
Targetnames=$(sort -u $Targetfilenames) # Place unique list in variable.

# CONCLUSION: Cleanup and exit message:
chmod go-r $Targetnames
flip -ub $Targetnames         # Mar 2002: MKS command to convert all files to Unix text
for File in $Targetnames $Allfiles; do
    [ -s $File ] || rm $File        # Erase data files if empty
done
if [ $Beforesize -ne $(cat $Targetnames 2>|$Devnull | wc -c) ]; then
    print -u2 "Warning: data may have been lost--use backup!\a\a\a"
else
    print -u2 "Done: data shawkled and intact!"
fi
```
