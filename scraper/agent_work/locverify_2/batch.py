import sys,subprocess
# lines: label|street|hn|bbox
for line in open(sys.argv[1]):
    line=line.strip()
    if not line: continue
    lab,st,hn,bb=line.split("|")
    out=subprocess.run(["python3","ovp.py","addr",st,hn,bb],capture_output=True,text=True).stdout
    print("=====",lab,flush=True); print(out,flush=True)
