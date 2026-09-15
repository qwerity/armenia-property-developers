import re,sys,html
def txt(f):
    t=open(f,errors='ignore').read()
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',t)))
if __name__=='__main__':
    f=sys.argv[1]; s=txt(f)
    for pat in sys.argv[2:]:
        for m in re.finditer(pat,s,flags=re.I):
            print('>>',s[max(0,m.start()-250):m.end()+250]); print()
