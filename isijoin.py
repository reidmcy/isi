import os
import sys

outfile = "CompiledData.isi"

FileSuffix = '.isi'

if __name__ == '__main__':
    if os.path.isfile(outfile):
        #Checks if the output outfile already exists and terminates if so
        print outfile +  " already exists\nexisting"
        sys.exit()
        #os.remove(outfile)
    flist = sys.argv[1:] if sys.argv[1:] else [f for f in os.listdir(".") if f.endswith(FileSuffix)]
    if len(flist) == 0:
        #checks for any valid files
        print "No " + FileSuffix + " Files"
        sys.exit()
    else:
        #Tells how many files were found
        print "Found " + str(len(flist)) + ' ' + FileSuffix + "  files"
    of = open(outfile, 'w')
    of.write("FN Thomson Reuters Web of Science\nVR 1.0\n")
    for f in flist:
        inf = open(f, 'r')
        for l in inf.readlines()[2:-1]:
            of.write(l)
    of.write('EF')
    of.close()
    print "Done"