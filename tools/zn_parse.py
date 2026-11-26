import json,re,sys
def parse(p,rows):
    L=open(p,encoding="utf-8-sig").read().split("\n")
    reg=L[3].split(";"); cat=[l.split(";") for l in L[6:6+rows]]
    out={}
    n=len(reg)
    for j in range(2,n,4):
        r=reg[j] if j<n else ""
        m=re.match(r"(\d{12})\s",r)
        if not m: continue
        rs=m.group(1); ags=rs[:5]+rs[9:12]
        d={}
        for c in cat:
            if j+2>=len(c): continue
            # columns: 0 date,1 label for first block; offset: first block cols 2..5
            off=j
            lab=c[1].strip()
            def num(s):
                s=s.strip().replace(".","").replace(",",".")
                try:return float(s)
                except:return None
            d[lab]=(num(c[off]),num(c[off+2]))
        out[ags]=d
    return out
a=parse("zn/a/1000A-1019_de.csv",3)
b=parse("zn/b/2000S-1003_de.csv",6)
print(len(a),len(b))
k=next(iter(a));print(k,a[k]);k=next(iter(b));print(k,b[k])
# check Deutschland column offset: first region 'Deutschland' not matched (no 12 digits) -> offsets use j; check alignment
L=open("zn/a/1000A-1019_de.csv",encoding="utf-8-sig").read().split("\n")
reg=L[3].split(";");print(reg[:6],L[6].split(";")[:10])
json.dump({"a":a,"b":b},open("zn_parsed.json","w"),ensure_ascii=False)
