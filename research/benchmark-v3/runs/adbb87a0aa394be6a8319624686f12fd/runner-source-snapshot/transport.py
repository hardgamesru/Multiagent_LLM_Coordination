"""Serial SDK transport with pre-request reservation and durable response capture."""
import hashlib
import json
import re
import time
from .adapter import load_backend
from .ledger import IntegrityStop

load_backend()
from llm_client import BaseLLMClient

ENDPOINT='https://api.giga.chat/v1/'
MAX_OUTPUT=4096
INPUT_ENVELOPE=65536
MAX_PROMPT_BYTES=16384


def safe_error_metadata(exc):
    """Whitelist structural fields only. Never serialize str(exc) or its body."""
    safe={'exception_type':type(exc).__name__}
    status=getattr(exc,'status_code',None)
    if type(status) is int:
        safe['http_status']=status
    delay=getattr(exc,'retry_after',None)
    if type(delay) in (int,float) and 0<=delay<=86400:
        safe['retry_after_seconds']=delay
    headers=getattr(exc,'headers',None)
    request_id=headers.get('x-request-id') if headers else None
    if isinstance(request_id,str) and re.fullmatch(r'[A-Za-z0-9-]{1,100}',request_id):
        safe['provider_request_id']=request_id
    return safe


class MeteredClient(BaseLLMClient):
    def __init__(self,model,ledger,experiment,evaluation,send):
        super().__init__()
        self.model_name=model
        self.ledger,self.experiment,self.evaluation,self.send=ledger,experiment,evaluation,send
        self.returned_models=[]
        self.ordinal=0

    def generate(self,system_prompt,user_prompt):
        self.ordinal+=1
        messages=[{'role':'system','content':system_prompt},{'role':'user','content':user_prompt}]
        serialized=json.dumps(messages,ensure_ascii=False,separators=(',',':')).encode('utf-8')
        if len(serialized)>MAX_PROMPT_BYTES:
            raise IntegrityStop('Prompt exceeds prerequest byte envelope; do not truncate silently')
        # For text-only byte/subword tokenization: reserve at least 4x serialized
        # bytes, far above expected prompt framing. Conditional on tokenization and
        # max_tokens semantics; not a claim of protection against provider faults.
        key=f'{self.evaluation}:{self.ordinal}'
        response=self.ledger.reserve(key,self.experiment,self.evaluation,self.model_name,ENDPOINT,
                                     hashlib.sha256(serialized).hexdigest(),INPUT_ENVELOPE,MAX_OUTPUT)
        if response is None:
            started=time.perf_counter()
            try:
                response=self.send(self.model_name,messages,MAX_OUTPUT)
            except BaseException as exc:
                self.ledger.unknown(key,safe_error_metadata(exc),time.perf_counter()-started)
                raise IntegrityStop('Provider/transport failure; billing unknown, further calls blocked') from None
            self.ledger.settle(key,response,time.perf_counter()-started)
        usage=response['usage']
        self._record_usage(usage['prompt_tokens'],usage['completion_tokens'],usage['total_tokens'])
        self.returned_models.append(response.get('model'))
        if not response.get('model'):
            raise IntegrityStop('Returned model identifier missing')
        try:
            choice=response['choices'][0]
            content=choice['message']['content']
        except (KeyError,IndexError,TypeError):
            raise IntegrityStop('Invalid response content shape') from None
        if not isinstance(content,str) or not content.strip():
            raise IntegrityStop('Empty response content; preserved in ledger')
        return content


class SDKTransport:
    def __init__(self,credentials,verify_ssl=True,timeout=60):
        from gigachat import GigaChat
        self.client=GigaChat(credentials=credentials,base_url=ENDPOINT,
                             verify_ssl_certs=verify_ssl,timeout=timeout,max_retries=0)
        if self.client._settings.max_retries!=0:
            raise IntegrityStop('SDK automatic retries not disabled')

    def models(self):
        try:
            return [m.id_ for m in self.client.get_models().data]
        except Exception:
            raise IntegrityStop('Model-list/authentication request failed; credentials not logged') from None

    def __call__(self,model,messages,max_output):
        from gigachat.models import Chat
        response=self.client.chat(Chat(model=model,messages=messages,max_tokens=max_output,n=1,stream=False))
        return response.model_dump(mode='json',by_alias=True)

    def close(self):
        self.client.close()
