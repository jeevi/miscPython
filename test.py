

import sys

print "1"
try:
    print "2"
    if int(sys.argv[1]) == 1:
        print "3"
        print sys.argv
        print "4"
        raise foo
        print "5"


    
except foo:
    print "7"
    print "\nworked!!\n"
