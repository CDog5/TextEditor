import re
langs = {
    "python": ["if","elif","else","from","import","yield","with","def","for","while"],
    "javascript":["let","var","const"],
    "html":["<[^>]*>"]
}
def highlight(inptext,mode=None):
        

    patterns = {
        "FLOAT" : r'(-\d+\.\d+|\d+\.\d+)',
        "INT" : r'(-\d+|\d+)',
        "STR" : r"(\".*\"|\'.*\')",
        "COMMENT" : r'(#.*|//.*)'
    }
    if mode:
        tmp = {mode:langs[mode]}
        tmp.update(patterns)
        patterns = tmp
    matchranges = []
    matchranges2 = []
    newmatches = []
    for k,v in patterns.items():
        if type(v) is list:
            for thing in v:
                for match in re.finditer(thing,inptext):
                    s = match.start()
                    e = match.end()
                    matchranges.append(("KEYWORD",s,e,inptext[s:e]))
            continue
        for match in re.finditer(v,inptext):
            s = match.start()
            e = match.end()
            matchranges.append((k,s,e,inptext[s:e]))
    matchranges = sorted(matchranges,key=lambda x: x[1])
    #pass one to fix strings
    for i,match in enumerate(matchranges):
        if i == 0 or match[1] > matchranges[i-1][2]:
            matchranges2.append(match)
    matchranges=[]
    #pass two to fix floats
    for i,match in enumerate(matchranges2):
        if i == 0 or match[1] > matchranges2[i-1][2]:
            matchranges.append(match)
    matchranges = sorted(matchranges,key=lambda x: x[1])
    for i,it in enumerate(matchranges):
        if i == 0 and it[1] > 0:
            newmatches.append(("DEFAULT",0,it[1]-1))
        elif i != 0 and it[1] - matchranges2[i-1][2] > 1:
            newmatches.append(("DEFAULT",matchranges[i-1][2]+1,it[1]-1))
        newmatches.append(it)
    return newmatches
