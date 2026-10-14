import re,sys
s=open(sys.argv[1]).read()
for i,m in enumerate(re.finditer(r'<g fill="(#\w+)" transform="translate\(([\d.]+) ([\d.]+)\) scale\(([\d.]+) -[\d.]+\)">(.*?)</g>',s)):
    fill,x,y,sc,body=m.groups(); sc=float(sc)
    a=sc*2048; b=sc*1000
    fs = f"A{a:.1f}" if abs(a-round(a))<0.01 else f"S{b:.1f}"
    xs=[float(t) for t in re.findall(r'transform="translate\(([\d.-]+) 0\)"',body)]
    n=len(xs); w=(xs[-1]*sc) if xs else 0
    print(i,fill,x,y,fs,'n=',n,'w~',round(w))
