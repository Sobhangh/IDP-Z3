# __main__.py
import sys
import re
import argparse
import time
from fileinput import filename
from textx import get_location

from .ast_engine.Parse import IDP
from .ast_engine.utils import IDPZ3Error

def output(lijst,soort):
    """Output of error/warning in format 'warning/error: line .. - colStart .. - colEnd=> message' """
    print(f"-- {soort} : aantal = {len(lijst)}")
    for i in lijst:
        location = get_location(i[0])
        if hasattr(i[0], 'name'):
            colEnd = location['col'] + len(i[0].name)
        elif hasattr(i[0], 'annotations') and i[0].annotations is not None:
            colEnd = location['col'] + len(i[0].annotations['reading'])
        else:
            colEnd = location['col']
        if argfilename :
            print(f"{filename}: {i[2]}: line {location['line']} - colStart {location['col']} - colEnd {colEnd} => {i[1]}")
        else:
            print(f"{i[2]}: line {location['line']} - colStart {location['col']} - colEnd {colEnd} => {i[1]}")

def doe_de_check(A):
    fouten = []
    A.SCA_Check(fouten)
    warnings = []
    errors = []
    for i in fouten:            #splits warning en errors
        if i[2] == "Warning":
            warnings.append(i)
        else :
            errors.append(i)
    output(errors,"Error")      #output errors
    output(warnings,"Warning")  #output warnings
    return len(fouten)

def sca(idp):
    aantal = 0
    print("\n---------- Vocabulary Check ----------")
    for v in idp.vocabularies:      #check all vocabularies
        print("-----",v)
        V = idp.get_blocks(v)       #get vocabulary block
        aantal += doe_de_check(V[0])          #check
    print("\n---------- Structure Check ----------")
    for s in idp.structures:        #check all structures
        print("-----",s)
        V = idp.get_blocks(s)       #get structure block
        aantal += doe_de_check(V[0])          #check
    print("\n---------- Theory Check ----------")
    for t in idp.theories:          #check all theories
        print("-----",t)
        T = idp.get_blocks(t)       #get theory block
        aantal += doe_de_check(T[0])          #check
    print("\n---------- Procedure Check ----------")
    for p in idp.procedures:        #check all procedures
        print("-----",p)
        P = idp.get_blocks(p)       #get procedure block
        aantal += doe_de_check(P[0])          #check
    return aantal

def extra(file):
    f = open(file, "r")     #open file
    fouten = []
    extra_check(f,fouten)   #controleer op extra style guide fouten
    extra_output(fouten)    #output de gevonden fouten
    f.close()               #close file
    return len(fouten)

def extra_check(f,fouten) :
    pattern = re.compile("\s,\S?") # als voor de komma een spatie en na de komma geen of wel spatie
    pattern2 = re.compile("\/\/") # search voor comments
    consistentie = ''
    consistentie_help = False
    unicode_symbols = ['⨯','→','𝔹','ℤ','ℝ','∀','∃','∈','∉','←','∧','∨','¬','⇒','⇔','⇐','≤','≠','≥']
    ascii_symbols = ['*','->','Bool','Int','Real','!','?',' in ',' not in ','<-','&','|','~','=>','<=>','<=','=<','~=','>=']
    lineNumber = 1
    help_lines = []
    duplicate_check = 0
    for line in f:
        # style guide regel: spaties niet voor/wel na de komma
        for match in re.finditer(pattern, line):
            fouten.append((lineNumber,match.span()[0],match.span()[1],"Style guide, to much spaces","Warning"))

        # style guide regel: commentaar op aparte lijnen
        for match in re.finditer(pattern2, line):
            if len(line[0:match.span()[0]].strip()) != 0:
                fouten.append((lineNumber,match.span()[0],match.span()[1],"Style guide, comment on seperate line","Warning"))

        # style guide regel: nieuwe regel op een nieuwe lijn
        if line.count('.') > 1:
            fouten.append((lineNumber,0,len(line),"Style guide, use new line for new rule","Warning"))

        # style guide regel: use indentation
        if not(line.startswith('\t') or line.startswith('    ')):
            keywords = ["vocabulary", "structure", "theory", "procedure","}"]
            if not(len(line.strip())==0 or any(word in line for word in keywords)):
                fouten.append((lineNumber,0,4,"Style guide, wrong indentation","Warning"))

        # style guide regel: Consistent gebruik van tekens in unicode of ASCII
        if not(consistentie_help):
            if any(symbol in line for symbol in unicode_symbols):
                consistentie = "unicode"
                consistentie_help = True
            elif any(symbol in line for symbol in ascii_symbols):
                consistentie = "ASCII"
                consistentie_help = True
        else:
            if any(symbol in line for symbol in unicode_symbols) and any(symbol in line for symbol in ascii_symbols):
                fouten.append((lineNumber,0,4,"Style guide, stay consistent in use of unicode or ASCII symbols","Warning"))
            elif any(symbol in line for symbol in unicode_symbols) and consistentie=="ASCII":
                fouten.append((lineNumber,0,4,"Style guide, stay consistent in use of unicode or ASCII symbols","Warning"))
            elif any(symbol in line for symbol in ascii_symbols) and consistentie=="unicode":
                fouten.append((lineNumber,0,4,"Style guide, stay consistent in use of unicode or ASCII symbols","Warning"))

        # style guide regel: Geen dezelfde regels/lijnen
        test_keywords = ["theory", "procedure"] #duplicates in structure en vocabulary worden door idp gemeld, net zoals duplicate bloknamen
        if any(word in line for word in test_keywords) and duplicate_check==0:
            help_lines.append(line)
            duplicate_check = 1
        elif (duplicate_check==1 and len(line.strip()) != 0):
            if (line in help_lines):
                fouten.append((lineNumber,0,len(line),"style guide, duplicate line","Warning"))
            else:
                help_lines.append(line)
        if ('}' in line and duplicate_check==1):
            duplicate_check = 0
            help_lines = []
        lineNumber += 1
    return fouten

def extra_output(lijst) :
    """ Output of extra style guide warning in format 'warning: line .. - colStart .. - colEnd=> message' """
    print(f"\n---------- Extra Style Guide Check: aantal = {len(lijst)} ----------")
    for i in lijst:
        if argfilename :
            print(f"{filename}: {i[4]}: line {i[0]} - colStart {i[1]} - colEnd {i[2]} => {i[3]}")
        else:
            print(f"{i[4]}: line {i[0]} - colStart {i[1]} - colEnd {i[2]} => {i[3]}")


def main():
    parser = argparse.ArgumentParser(description='SCA')
    parser.add_argument('FILE', help='path to the .idp file', type=argparse.FileType('r'))
    parser.add_argument('--no-timing', help='don\'t display timing information',
                        dest='timing', action='store_false', default=True)
    parser.add_argument('--print-AST', help='gives the AST as output',
                        dest='AST', action='store_true', default=False)
    parser.add_argument('--Add-filename', help='Add filename to warning/error output',
                        dest='filename', action='store_true', default=False)
    parser.add_argument('--Add-extraStyle', help='Gives extra style guide warnings',
                        dest='extra', action='store_true', default=False)
    args = parser.parse_args()

    start_time = time.time()
    try:
        global filename
        global argfilename
        totaal = 0
        filename = sys.argv[1]
        argfilename = args.filename
        if sys.argv[1].endswith(".idp"):
            idp = IDP.from_file(sys.argv[1])    # parse idp file to AST
            if args.AST:
                idp.printAST(0)                 # print AST van file
            totaal += sca(idp)                            # Voer SCA uit
            if args.extra:
                totaal += extra(filename)                 # Extra style guide checking
            print(f"\n---------- Totaal aantal fouten {totaal} ----------")
        else:
            print("Expected an .idp file")
    except IDPZ3Error as e1:
        res1 = e1.args[0].split(': ', 1)
        res = res1[0].split()
        print("\n---------- Syntax Error ----------")
        if args.filename :
            print(f"{filename}: {res[0]}: line {res[3].strip(',')} - colStart {res[5].strip(':')} - colEnd {res[5].strip(':')} => {res1[1]}")
        else:
            print(f"{res[0]}: line {res[3].strip(',')} - colStart {res[5].strip(':')} - colEnd {res[5].strip(':')} => {res1[1]}")
    except KeyError as e2: # Bij een KeyError
        if args.filename :
            print(f"{filename}: Error: line {0} - colStart {0} - colEnd {0} => Key Error {e2}")
        else :
            print(f"Error: line {0} - colStart {0} - colEnd {0} => Key Error {e2}")
    except Exception as e:
        print(e)
        print("\n---------- Syntax Error ----------")
        try:
            if args.filename :
                print(f"{filename}: Error: line {e.line} - colStart {e.col} - colEnd {e.col} => {e.args}")
            else :
                print(f"Error: line {e.line} - colStart {e.col} - colEnd {e.col} => {e.args}")
        except: # Bij een error zonder lijn nummer
            if args.filename :
                print(f"{filename}: Error: line {0} - colStart {0} - colEnd {10} => {e}")
            else :
                print(f"Error: line {0} - colStart {0} - colEnd {10} => {e}")

    if args.timing:
        print(f"\nElapsed time: {format(time.time() - start_time)} seconds")

if __name__ == "__main__":
    main()
