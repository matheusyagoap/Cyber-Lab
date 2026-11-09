from flask import Flask, request, jsonify, session, redirect, url_for, render_template_string
from markupsafe import escape
import re, unicodedata
from pathlib import Path
from dashboard_integration import create_local_dashboard
app=Flask(__name__)

def slugify(value):
    value = unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')

app.jinja_env.globals['slugify'] = slugify
app.secret_key='cyberlab-demo-only-change-me'
PORT=5305
APP_NAME='Atlas Logistics'

create_local_dashboard(
    app,
    report_dir=Path(__file__).parent / "relatorios",
    scenario="05",
    application=APP_NAME
)
BRAND='ATLAS'
ACCENT='#fb923c'
DATA=[{'id': 'TRK-551', 'name': 'Entrega SP-551', 'owner': 'Carlos Mendes', 'status': 'Em rota', 'value': 'Previsão 16:40', 'detail': 'Remessa fictícia'}, {'id': 'TRK-552', 'name': 'Entrega SP-552', 'owner': 'Juliana Costa', 'status': 'Entregue', 'value': '14:12', 'detail': 'Comprovante simulado'}, {'id': 'VEI-018', 'name': 'Veículo V-018', 'owner': 'Frota', 'status': 'Disponível', 'value': 'Van — ABC1D23', 'detail': 'Veículo fictício'}, {'id': 'VEI-022', 'name': 'Veículo V-022', 'owner': 'Frota', 'status': 'Manutenção', 'value': 'Caminhão — DEF4G56', 'detail': 'Registro demonstrativo'}, {'id': 'CLI-091', 'name': 'Cliente Loja Central', 'owner': 'Comercial', 'status': 'Ativo', 'value': '12 remessas/mês', 'detail': 'Cliente fictício'}, {'id': 'ROT-070', 'name': 'Rota metropolitana 070', 'owner': 'Torre de controle', 'status': 'Monitorada', 'value': '6 paradas', 'detail': 'Rota simulada'}]
DATA.extend([{'id': 'TRK-552', 'name': 'Entrega TRK-552', 'owner': 'Campinas → São Paulo', 'status': 'Em rota', 'value': 'ETA 16:40', 'detail': 'Rastreamento logístico fictício'}, {'id': 'TRK-553', 'name': 'Entrega TRK-553', 'owner': 'Santos → São Paulo', 'status': 'No prazo', 'value': 'ETA 18:10', 'detail': 'Rastreamento logístico fictício'}, {'id': 'TRK-554', 'name': 'Entrega TRK-554', 'owner': 'Jundiaí → Sorocaba', 'status': 'Atenção', 'value': 'ETA 17:20', 'detail': 'Rastreamento logístico fictício'}])
TITLE='Logística'
KPI=["Entregas em rota", "Veículos ativos", "No prazo", "Ocorrências"]
SECTIONS=["Torre de controle", "Entregas", "Frota", "Clientes"]
BASE_STYLE="""
:root{--navy:#182b3c;--accent:#fb923c;--ink:#172338;--muted:#738096;--line:#e8edf3;--bg:#f4f7fb}*{box-sizing:border-box}body{margin:0;background:var(--bg);font:14px Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink)}.shell{display:grid;grid-template-columns:248px 1fr;min-height:100vh}aside{background:var(--navy);color:#dbe7f5;padding:25px 16px}.brand{display:flex;align-items:center;gap:12px;font-size:17px;font-weight:800;letter-spacing:.2px;margin:0 8px 8px}.mark{width:38px;height:38px;border-radius:12px;background:var(--accent);display:grid;place-items:center;color:#092033;font-weight:900}.subbrand{font-size:11px;color:#9db0c7;margin:0 8px 34px}.navlabel{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#8197b2;margin:25px 10px 10px}.nav a{display:block;color:#c8d6e8;text-decoration:none;padding:11px 12px;border-radius:9px;margin:3px 0}.nav a.active,.nav a:hover{background:#ffffff18;color:white}main{padding:30px 36px;max-width:1600px;width:100%;margin:auto}.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:30px}.crumb{color:var(--muted);font-size:12px}.user{display:flex;align-items:center;gap:10px;background:white;border:1px solid var(--line);padding:8px 12px;border-radius:30px}.avatar{width:30px;height:30px;border-radius:50%;background:#e4edf8;display:grid;place-items:center;font-weight:800;color:var(--navy)}h1{font-size:27px;margin:0 0 7px;letter-spacing:-.7px}.lead{color:var(--muted);margin:0 0 26px}.actions{display:flex;gap:9px}.btn{border:0;background:var(--navy);color:white;border-radius:9px;padding:10px 15px;text-decoration:none;font-weight:650;cursor:pointer}.btn.secondary{background:white;color:var(--ink);border:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:22px 0}.card{background:white;border:1px solid var(--line);border-radius:14px;padding:19px;box-shadow:0 4px 14px #10243b06}.klabel{font-size:12px;color:var(--muted)}.kvalue{font-size:25px;font-weight:800;margin:10px 0 5px}.delta{font-size:11px;color:#14956e}.content{display:grid;grid-template-columns:1.45fr 1fr;gap:17px}.cardhead{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}h2{font-size:15px;margin:0}.pill{background:#e8f8f2;color:#13815e;padding:5px 9px;border-radius:20px;font-size:11px;font-weight:700}table{width:100%;border-collapse:collapse}th{font-size:10px;text-transform:uppercase;letter-spacing:.8px;color:#8793a5;text-align:left;padding:11px 8px;border-bottom:1px solid var(--line)}td{padding:14px 8px;border-bottom:1px solid #eff2f6;font-size:12px}.muted{color:var(--muted)}.barrow{margin:17px 0}.barlabel{display:flex;justify-content:space-between;font-size:12px;margin-bottom:8px}.bar{height:8px;border-radius:20px;background:#edf1f6;overflow:hidden}.bar i{display:block;height:100%;background:var(--accent);border-radius:20px}.notice{background:#fff8e9;border:1px solid #f6e4bb;border-radius:11px;padding:14px;color:#805b15;font-size:12px;margin-top:16px}.footer{color:#9aa5b5;font-size:11px;margin-top:28px}.detail{margin-top:18px}input{border:1px solid var(--line);border-radius:8px;padding:10px}@media(max-width:900px){.shell{grid-template-columns:1fr}aside{padding:15px}.nav{display:flex;flex-wrap:wrap}.navlabel{display:none}main{padding:22px}.grid{grid-template-columns:repeat(2,1fr)}.content{grid-template-columns:1fr}}@media(max-width:520px){.grid{grid-template-columns:1fr 1fr}main{padding:16px}h1{font-size:22px}}
"""
LAYOUT="""<!doctype html><html lang='pt-br'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{{title}} | {{brand}}</title><style>"""+BASE_STYLE+"""</style></head><body><div class='shell'><aside><div class='brand'><div class='mark'>{{brand[:1]}}</div>{{brand}}</div><div class='subbrand'>{{subtitle}}</div><div class='navlabel'>Workspace</div><nav class='nav'><a class='active' href='/'>▦ &nbsp; Visão geral</a>{% for s in sections %}<a href='/{{slugify(s)}}'>◈ &nbsp; {{s}}</a>{% endfor %}</nav><div class='navlabel'>Sistema</div><nav class='nav'><a href='/admin'>⚙ &nbsp; Administração</a><a href='/health'>● &nbsp; Status do serviço</a></nav></aside><main><div class='top'><div class='crumb'>Workspace / {{domain}} / Visão geral</div><div class='user'><div class='avatar'>FO</div><div><b>Fabio Oliveira</b><div class='muted' style='font-size:10px'>Administrador de demonstração</div></div></div></div>{{body|safe}}<div class='footer'>{{brand}} · Ambiente demonstrativo · Dados fictícios · CyberLab Estácio</div></main></div></body></html>"""
@app.get('/')
def home():
 body=render_template_string("""<h1>{{name}}</h1><p class='lead'>{{subtitle}} · Ambiente de demonstração com dados sintéticos</p><div class='actions'><a class='btn' href='{{url_for("records")}}'>Abrir registros</a><a class='btn secondary' href='/health'>Verificar serviço</a></div><div class='grid'>{% for k in kpis %}<div class='card'><div class='klabel'>{{k}}</div><div class='kvalue'>{{loop.index*127+38}}</div><div class='delta'>↗ Indicador simulado</div></div>{% endfor %}</div><div class='content'><section class='card'><div class='cardhead'><h2>Atividade recente</h2><span class='pill'>Atualizado agora</span></div><table><thead><tr><th>Identificador</th><th>Registro</th><th>Status</th><th>Responsável</th></tr></thead><tbody>{% for x in data %}<tr><td><b>{{x.id}}</b></td><td>{{x.name}}</td><td><span class='pill'>{{x.status}}</span></td><td>{{x.owner|capitalize}}</td></tr>{% endfor %}</tbody></table><div class='notice'>Área de laboratório: os dados são fictícios e as rotas de investigação estão limitadas a este ambiente.</div></section><section class='card'><div class='cardhead'><h2>Áreas do produto</h2><span class='muted'>Visão operacional</span></div>{% for s in sections %}<div class='barrow'><div class='barlabel'><span>{{s}}</span><b>{{72+loop.index*4}}%</b></div><div class='bar'><i style='width:{{72+loop.index*4}}%'></i></div></div>{% endfor %}<p class='muted' style='font-size:11px'>Indicadores ilustrativos para a atividade acadêmica.</p></section></div>""",name=APP_NAME,subtitle='Inteligência logística e gestão de entregas',kpis=KPI,sections=SECTIONS,data=DATA)
 return render_template_string(LAYOUT,title=APP_NAME,brand=BRAND,subtitle='Inteligência logística e gestão de entregas',domain=TITLE,sections=SECTIONS,body=body)
@app.get('/registros')
def records():
 return jsonify({'items':DATA,'total':len(DATA),'notice':'Dados sintéticos do CyberLab'})
@app.get('/registro')
def record():
 ident=request.args.get('id','')
 item=next((x for x in DATA if x['id']==ident),None)
 if not item:return jsonify(error='Registro não encontrado'),404
 # PONTO DE INVESTIGAÇÃO: falta validar a autorização do titular/responsável.
 return jsonify(item)
@app.get('/rastreio')
def business_record():
 ident=request.args.get('id','')
 item=next((x for x in DATA if x['id']==ident),DATA[0])
 # PONTO DE INVESTIGAÇÃO: controle de autorização propositalmente incompleto.
 return jsonify(item)
@app.get('/search')
def search():
 term=request.args.get('q','')
 # Reflexão proposital para análise; não execute scripts ou payloads externos.
 return '<h2>Busca do sistema</h2><p>Resultado para: '+term+'</p>'
@app.get('/admin')
def admin():
 # PONTO DE INVESTIGAÇÃO: rota administrativa demonstrativa sem autenticação.
 return jsonify(area='administrativa',mensagem='Conteúdo interno fictício',usuarios=['ana','bruno'])
@app.get('/health')
def health():return jsonify(status='ok',application=APP_NAME)



@app.get('/detalhe/<record_id>')
def detail_page(record_id):
    item = next((row for row in DATA if str(row.get('id')) == str(record_id)), None)
    if item is None:
        return render_template_string(LAYOUT, title=APP_NAME, brand=BRAND, subtitle="Ambiente demonstrativo", domain=TITLE, sections=SECTIONS, body="<section class='card'><h1>Registro não encontrado</h1><a class='btn' href='/'>Voltar</a></section>"), 404
    body = render_template_string("""<section class='card'><h1>{{ item.name }}</h1><p class='lead'>Detalhes do registro sintético · {{ app_name }}</p><div class='grid'><div class='card'><div class='klabel'>Identificador</div><div class='kvalue' style='font-size:20px'>{{ item.id }}</div></div><div class='card'><div class='klabel'>Status</div><div class='kvalue' style='font-size:20px'>{{ item.status }}</div></div><div class='card'><div class='klabel'>Informação</div><div class='kvalue' style='font-size:20px'>{{ item.value }}</div></div></div><h2>Dados do registro</h2><table><tbody><tr><th>Responsável / contexto</th><td>{{ item.owner }}</td></tr><tr><th>Descrição</th><td>{{ item.detail }}</td></tr></tbody></table><div class='actions'><a class='btn' href='/'>Voltar ao painel</a><a class='btn secondary' href='/registros'>Consultar dados JSON</a></div><div class='notice'>Registro inteiramente fictício, criado para atividade acadêmica.</div></section>""", item=item, app_name=APP_NAME)
    return render_template_string(LAYOUT, title=APP_NAME, brand=BRAND, subtitle="Ambiente demonstrativo", domain=TITLE, sections=SECTIONS, body=body)

@app.get('/<path:section_slug>')
def section_page(section_slug):
    # Resolve every visible sidebar entry to a real, data-backed page.
    section = next((s for s in SECTIONS if slugify(s) == slugify(section_slug)), None)
    if section is None:
        return render_template_string(LAYOUT, title=APP_NAME, brand=BRAND,
            subtitle="Ambiente demonstrativo", domain=TITLE, sections=SECTIONS,
            body=render_template_string("""<section class='card'><h1>Página não encontrada</h1><p>O endereço solicitado não corresponde a uma área deste sistema.</p><a class='btn' href='/'>Voltar ao painel</a></section>""")), 404
    rows = DATA
    body = render_template_string("""
      <h1>{{ section }}</h1>
      <p class='lead'>{{ name }} · Área funcional com registros sintéticos para navegação e análise</p>
      <div class='actions'><a class='btn' href='/'>Voltar à visão geral</a><a class='btn secondary' href='/registros'>Consultar API de dados</a></div>
      <div class='grid'>
        <div class='card'><div class='klabel'>Registros disponíveis</div><div class='kvalue'>{{ rows|length }}</div><div class='delta'>Dados fictícios</div></div>
        <div class='card'><div class='klabel'>Área</div><div class='kvalue' style='font-size:20px'>{{ section }}</div><div class='delta'>Módulo do sistema</div></div>
        <div class='card'><div class='klabel'>Ambiente</div><div class='kvalue' style='font-size:20px'>Laboratório</div><div class='delta'>Uso acadêmico local</div></div>
      </div>
      <section class='card'><div class='cardhead'><h2>{{ section }} — registros</h2><span class='pill'>{{ rows|length }} itens</span></div>
      <div style='overflow-x:auto'><table><thead><tr><th>Identificador</th><th>Descrição</th><th>Responsável / contexto</th><th>Status</th><th>Informação</th><th>Ação</th></tr></thead><tbody>
      {% for row in rows %}<tr><td><b>{{ row.id }}</b></td><td>{{ row.name }}</td><td>{{ row.owner }}</td><td><span class='pill'>{{ row.status }}</span></td><td>{{ row.value }}</td><td><a href='/detalhe/{{ row.id }}'>Detalhes</a></td></tr>{% endfor %}
      </tbody></table></div><div class='notice'>Todos os registros são sintéticos. Não utilize dados pessoais ou sistemas externos neste laboratório.</div></section>
      """, section=section, name=APP_NAME, rows=rows)
    return render_template_string(LAYOUT, title=APP_NAME, brand=BRAND,
        subtitle="Ambiente demonstrativo", domain=TITLE, sections=SECTIONS, body=body)

@app.errorhandler(404)
def not_found(error):
    body = render_template_string("""<section class='card'><h1>Página não encontrada</h1><p>O endereço não existe neste ambiente de demonstração.</p><a class='btn' href='/'>Voltar à visão geral</a></section>""")
    return render_template_string(LAYOUT, title=APP_NAME, brand=BRAND,
        subtitle="Ambiente demonstrativo", domain=TITLE, sections=SECTIONS, body=body), 404

if __name__=='__main__':app.run(host='0.0.0.0',port=PORT,debug=False)
