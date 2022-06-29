# ASTprint.py
import sys
from ast_engine import IDP
# from ast_engine import IDP

def main():
    # start :
    idp = IDP.from_file(sys.argv[1])
    blocks = []

    for v in idp.vocabularies:  # get all vocabularies
        blocks.append(v)
    for s in idp.structures:  # get all structures
        blocks.append(s)
    for t in idp.theories:  # get all theories
        blocks.append(t)
    for p in idp.procedures:  # get all procedures
        blocks.append(p)

    try:
        i = True
        while i:
            print("\nChoose block out of ", blocks, " or 'idp' for whole AST")
            block = input("Enter block name or stop : ")
        if block in blocks:
            B = idp.get_blocks(block)
            B[0].mijnAST(0)
        elif block == "idp":
            idp.mijnAST(0)
        elif block == "stop":
            i = False
        else:
            print(block, "is not a block!")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
