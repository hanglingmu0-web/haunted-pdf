from pathlib import Path
from io import BytesIO
import struct,json,hashlib,re
from cryptography import x509
from pypdf import PdfReader

def cbor(b):
    f=BytesIO(b)
    def read():
        first=f.read(1)
        if not first:raise ValueError('truncated CBOR')
        m=first[0]>>5;a=first[0]&31
        if a<24:n=a
        elif a in (24,25,26,27):n=int.from_bytes(f.read(1<<(a-24)),'big')
        else:raise ValueError('indefinite CBOR')
        if m==0:return n
        if m==1:return -1-n
        if m==2:return f.read(n)
        if m==3:return f.read(n).decode('utf-8')
        if m==4:return [read() for _ in range(n)]
        if m==5:return {read():read() for _ in range(n)}
        if m==6:return {'tag':n,'value':read()}
        if m==7:return {20:False,21:True,22:None}.get(n,n)
        raise ValueError(m)
    result=read(); assert f.tell()==len(b),(f.tell(),len(b));return result

def safe(v):
    if isinstance(v,bytes):
        try:return {'certificate_subject':x509.load_der_x509_certificate(v).subject.rfc4514_string()}
        except ValueError:pass
        try:return {'nested_cbor':safe(cbor(v))}
        except (ValueError,AssertionError,TypeError,UnicodeDecodeError,IndexError):pass
        return {'binary_length':len(v),'sha256':hashlib.sha256(v).hexdigest()}
    if isinstance(v,dict):return {str(k):safe(val) for k,val in v.items()}
    if isinstance(v,list):return [safe(val) for val in v]
    return v

def boxes(b,path=''):
    at=0; label=''
    while at<len(b):
        size=int.from_bytes(b[at:at+4],'big');kind=b[at+4:at+8].decode('ascii');assert size>=8
        payload=b[at+8:at+size];assert at+size<=len(b)
        if kind=='jumd':label=payload[17:].split(b'\0')[0].decode('utf-8')
        elif kind=='jumb':yield from boxes(payload,path+'/'+label)
        elif kind=='cbor':yield {'path':path+'/'+label,'data':safe(cbor(payload))}
        at+=size
    assert at==len(b)

ROOT=Path(__file__).resolve().parents[1]
for d in [ROOT/'work/audit/ningyo_halloween_pumpkin',ROOT/'work/audit/Ningyo_Halloween_Poster']:
    b=next(d.glob('attachment-*.bin')).read_bytes()
    result=list(boxes(b));certs=[]
    for m in re.finditer(b'\x30\x82',b):
        i=m.start();size=int.from_bytes(b[i+2:i+4],'big')+4
        try:
            cert=x509.load_der_x509_certificate(b[i:i+size]);certs.append({'subject':cert.subject.rfc4514_string(),'issuer':cert.issuer.rfc4514_string(),'extensions':str(cert.extensions)})
        except ValueError:pass
    (d/'credentials-decoded.json').write_text(json.dumps({'boxes':result,'certificates':certs},ensure_ascii=False,indent=2),encoding='utf-8')
    print(d.name,json.dumps(result,ensure_ascii=False));print('CERTIFICATES',json.dumps(certs,ensure_ascii=False))

p=ROOT/'samples/Ningyo_Halloween_Poster.pdf';b=p.read_bytes();first=b.index(b'%%EOF')+5
r=PdfReader(BytesIO(b[:first]));print('PREVIOUS_REVISION',r.metadata,r.trailer['/Root'],len(r.pages))
