import json,sys
dev,tax=sys.argv[1],sys.argv[2]
names=sys.argv[3:]
with open('queue_C.jsonl','a') as f: f.write(json.dumps({"dev":dev,"names":names,"tax_id":None if tax=='null' else tax},ensure_ascii=False)+"\n")
