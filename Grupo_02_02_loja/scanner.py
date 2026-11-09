import json, requests, re
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape
BASE='http://127.0.0.1:5302'
SCENARIO='02'
APP_NAME='Vértice Commerce'
checks=[]
def check(title,severity,path,method='GET',params=None,indicator=None,recommendation='Revisar o controle no servidor.'):
 try:
  r=requests.get(BASE+path,params=params,timeout=5)
  detected=indicator(r) if indicator else r.status_code==200
  checks.append({'title':title,'severity':severity if detected else 'informativo','status':'indicador_detectado' if detected else 'nao_detectado','route':path,'http_status':r.status_code,'evidence':f'HTTP {r.status_code}; resposta={r.text[:180]}','recommendation':recommendation})
 except Exception as e:checks.append({'title':title,'severity':'erro_execucao','status':'nao_avaliado','route':path,'evidence':str(e),'recommendation':'Confirme se a aplicação está ativa na porta 5302.'})
def main():
 check('Rota administrativa acessível sem autenticação','alto','/admin',indicator=lambda r:r.status_code==200,recommendation='Exigir autenticação e autorização no servidor.')
 check('Consulta de registro sem validação de titularidade','alto','/pedido',params={'PED-2048':'PED-2048'},indicator=lambda r:r.status_code==200,recommendation='Validar identidade, titularidade e perfil antes de retornar o registro.')
 check('Exposição de dados na listagem','medio','/registros',indicator=lambda r:r.status_code==200 and 'detail' in r.text,recommendation='Minimizar os campos retornados e aplicar autorização por perfil.')
 check('Cabeçalhos HTTP de segurança ausentes','baixo','/',indicator=lambda r:any(h not in r.headers for h in ['Content-Security-Policy','X-Content-Type-Options','X-Frame-Options']),recommendation='Configurar cabeçalhos de segurança adequados.')
 marker='CYBERLAB-MARCADOR-TESTE'
 check('Marcador de busca refletido na resposta','medio','/search',params={'q':marker},indicator=lambda r:marker in r.text,recommendation='Aplicar escape contextual de saída; reflexão isolada não comprova XSS.')
 report={'metadata':{'scenario':SCENARIO,'application':APP_NAME,'generated_at':datetime.now(timezone.utc).isoformat(),'target':'localhost only','scope':'ambiente local fictício'},'summary':{'total_checks':len(checks),'indicators':sum(x['status']=='indicador_detectado' for x in checks)},'findings':checks,'logs':[{'timestamp':datetime.now(timezone.utc).isoformat(),'event':'scanner_completed'}]}
 out=Path('relatorios');out.mkdir(exist_ok=True)
 slug=re.sub(r'[^a-z0-9]+','_',APP_NAME.lower()).strip('_')
 json_name=f'{SCENARIO}_{slug}.json'
 pdf_name=f'{SCENARIO}_{slug}.pdf'
 (out/json_name).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 try:
  from reportlab.lib.pagesizes import A4
  from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
  from reportlab.lib import colors
  from reportlab.lib.styles import getSampleStyleSheet
  st=getSampleStyleSheet(); story=[Paragraph('Relatório CyberLab — '+APP_NAME,st['Title']),Paragraph('Escopo: aplicação local fictícia. Indicadores precisam de validação manual.',st['BodyText']),Spacer(1,14)]
  rows=[['Achado','Severidade','Status']]+[[escape(x['title']),escape(x['severity']),escape(x['status'])] for x in checks]
  t=Table(rows,repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#142b45')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.4,colors.grey),('FONTSIZE',(0,0),(-1,-1),8),('VALIGN',(0,0),(-1,-1),'TOP')]));story.append(t)
  for x in checks:story += [Spacer(1,10),Paragraph(escape(x['title']),st['Heading3']),Paragraph('Evidência: '+escape(x['evidence']),st['BodyText']),Paragraph('Recomendação: '+escape(x['recommendation']),st['BodyText'])]
  SimpleDocTemplate(str(out/pdf_name),pagesize=A4).build(story)
  aviso=out/'AVISO_PDF.txt'
  if aviso.exists(): aviso.unlink()
 except Exception as e:(out/'AVISO_PDF.txt').write_text(str(e),encoding='utf-8')
 print(json.dumps(report['summary'],ensure_ascii=False));print(f'Relatórios gerados: {json_name} e {pdf_name}')
if __name__=='__main__':main()
