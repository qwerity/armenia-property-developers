import json,sys
D='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/reputation_4/'
dev=sys.argv[1]; tax=None if sys.argv[2]=='null' else sys.argv[2]
with open(D+'queue_B.jsonl','a',encoding='utf8') as f: f.write(json.dumps({"dev":dev,"names":sys.argv[3:],"tax_id":tax},ensure_ascii=False)+"\n")
