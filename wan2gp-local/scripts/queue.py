"""Append a WanGP queue bundle through its public Gradio HTTP API."""
import argparse,json,uuid,urllib.request,urllib.parse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--base-url',required=True);p.add_argument('--bundle',required=True);p.add_argument('--log',required=True);a=p.parse_args()
base=a.base_url.rstrip('/');session=uuid.uuid4().hex
log=Path(a.log);log.parent.mkdir(parents=True,exist_ok=True)
def report(value):
    with log.open('a',encoding='utf-8') as f:f.write(json.dumps(value,ensure_ascii=False)+'\n')
    print(json.dumps(value,ensure_ascii=False),flush=True)
def request(route,data=None,ctype='application/json'):
    req=urllib.request.Request(base+route,data=data,headers={'Content-Type':ctype} if data else {})
    with urllib.request.urlopen(req,timeout=3600) as r:return json.load(r)
config=request('/config');deps=config['dependencies'];components={c['id']:c for c in config['components']}
def call(name,values=None,upload=False):
    dep=next(d for d in deps if d.get('api_name')==name)
    data=[];values=iter(values or [])
    for cid in dep['inputs']:
        data.append(None if components[cid]['type']=='state' else next(values))
    payload={'session_hash':session,'fn_index':dep['id'],'data':data}
    if upload:payload['trigger_id']=next(t[0] for t in dep['targets'] if t[1]=='upload')
    receipt=request('/gradio_api/queue/join',json.dumps(payload).encode());report({'operation':name,'receipt':receipt})
    event=receipt['event_id']; reported_error=None
    with urllib.request.urlopen(base+'/gradio_api/queue/data?session_hash='+session,timeout=3600) as stream:
        for raw in stream:
            if not raw.startswith(b'data:'):continue
            message=json.loads(raw[5:])
            if message.get('event_id')!=event:continue
            if message.get('msg') in ['log','process_completed']:
                # Do not log gallery base64 contents.
                output=message.get('output',{})
                report({'operation':name,'message':message.get('msg'),'success':message.get('success'),'error':output.get('error'),'log':message.get('log')})
            if message.get('msg')=='log':
                msg=str(message.get('log') or '')
                if msg.startswith(('Failed to load queue:', 'Error loading queue:')):reported_error=msg
            if message.get('msg')=='process_completed':
                if reported_error:raise RuntimeError(reported_error)
                if not message.get('success'):raise RuntimeError(message.get('output'))
                return message.get('output',{}).get('data')
    raise RuntimeError('Stream ended before completion: '+name)
bundle=Path(a.bundle);boundary='----WanQueue'+uuid.uuid4().hex
body=(f'--{boundary}\r\nContent-Disposition: form-data; name="files"; filename="{bundle.name}"\r\nContent-Type: application/octet-stream\r\n\r\n').encode()+bundle.read_bytes()+f'\r\n--{boundary}--\r\n'.encode()
uploaded=request('/gradio_api/upload',body,'multipart/form-data; boundary='+boundary)
result=call('load_queue_action',[{'path':uploaded[0],'orig_name':bundle.name,'meta':{'_type':'gradio.FileData'}}],True)
report({'operation':'load_result','received':result is not None})
call('init_process_queue_if_any')
call('process_tasks')
report({'complete':True})
