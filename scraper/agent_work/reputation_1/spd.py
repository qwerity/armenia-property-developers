import sys,re
from spy import page
for p in sys.argv[1:]:
    t=page(p)
    a=t.find('Ղեկավար'); b=t.find('Որոշ բանալի բառեր')
    print('##',p); print('  ',t[a:a+300]); 
    for k in ['Հիմնադրման տարի','Աշխատողների','Գործընկեր','նախկին անվանում','հին անվանում']:
        i=t.find(k); 
        if i>=0: print('   ',t[i:i+160])
    print('   KW:',t[b:b+250])
