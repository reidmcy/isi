import papers
import os
import csv
import sys
import networkx as nx

outfile = "city-city.graphml"

class BadPaper(Warning):
    pass

def paperParser(paper):
    """
    paperParser reads paper until it reaches 'EF' for each field tag it adds an
    entry to the returned dict with the tag as the key and a list of the entries
    for the tag as the value, the list has each line as an entry.   
    """
    tdict = {}
    currentTag = ''
    for l in paper:
        if 'ER' in l[:2]:
            return tdict
        elif '   ' in l[:3]: #the string is three spaces in row
            tdict[currentTag].append(l[3:-1])
        elif l[2] == ' ':
            currentTag = l[:2]
            tdict[currentTag] = [l[3:-1]]
        else:
            raise BadPaper("Field tag not formed correctly: " + l)
    raise BadPaper("End of file reached before EF")

def isiParser(isifile):
    """
    isiParser reads a file, checks that the header is correct then reads each
    paper returning a list of of dicts keyed with the field tags.
    """
    f = open(isifile, 'r')
    if "VR 1.0" not in f.readline() and "VR 1.0" not in f.readline():
        raise BadPaper(isifile + " Does not have a valid header")
    notEnd = True
    plst = []
    while notEnd:
        l = f.next()
        if not l:
            raise BadPaper("No ER found in " + isifile)
        elif l.isspace():
            continue
        elif 'EF' in l[:2]:
            notEnd = False
            continue
        else:
            try:
                if l[:2] != 'PT':
                    raise BadPaper("Paper does not start with PT tag")
                plst.append(paperParser(f))
                plst[-1][l[:2]] = l[3:-1]
            except Warning as w:
                raise BadPaper(str(w.message) + "In " + isifile)
            except Exception as e:
                 raise e
    try:
        f.next()
        print "EF not at end of " + isifile
    except StopIteration as e:
        pass
    finally:
        return plst

def getCity(s):
    if s[0] == '[':
        s = s.split('] ')[1]
    clev = s.split(', ')
    if clev[-1] == 'Tunisia.':
        s = ''
        for w in clev[-2].split(' '):
            if not any(c.isdigit() for c in w):
                s += w + ' '
        return s[:-1]
    else:
        return ''

def graphAdder(plst, grph):
    for p in plst:
        try:
            for loc1 in p['C1']:
                c1 = getCity(loc1)
                if c1:
                    if not grph.has_node(c1):
                        grph.add_node(c1)
                    for loc2 in p['C1'][p['C1'].index(loc1) + 1:]:
                        c2 = getCity(loc2)
                        if c2:
                            if grph.has_edge(c1, c2):
                                grph[c1][c2]['weight'] += 1
                            else:
                                print str(c1) + ' - ' + str(c2)
                                grph.add_edge(c1, c2, weight = 1)
        except KeyError as e:
            print "Key Error"
            print p.keys()

if __name__ == '__main__':
    if os.path.isfile(outfile):
        #Checks if the output already exists and terminates if so
        print outfile +  " already exists\nexisting"
        #sys.exit()
        os.remove(outfile)
    flist = [f for f in os.listdir(".") if f.endswith(".isi")]
    if len(flist) == 0:
        #checks for any valid files
        print "No isi Files"
        sys.exit()
    else:
        #Tells how many files were found
        print "Found " + str(len(flist)) + " isi files"
    G = nx.Graph()
    for isi in flist:
        try:
            graphAdder(isiParser(isi), G)
        except Exception, e:
            print type(e)
            print isi
            print e
            raise
            break
    nx.write_graphml(G, outfile)
    print "Done"
