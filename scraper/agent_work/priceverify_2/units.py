import re,glob,sys
def show(items,label=''):
    items=[(p,a,*r) for p,a,*r in items if a>0]
    items.sort(key=lambda x:x[0]/x[1])
    print(label,len(items),'units')
    for x in items[:6]: print('   per m2 %.0f'%(x[0]/x[1]),x)
    if items: print('   cheapest total',min(items))
