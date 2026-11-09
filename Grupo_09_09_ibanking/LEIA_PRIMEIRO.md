# CyberLab — Pacote do Grupo 09
## Aplicação: Orion Invest

Este pacote contém a aplicação web do cenário, o scanner de segurança, o desafio,
o roteiro de trabalho e um painel local para visualizar o relatório gerado.

## 1. O que fazer primeiro
1. Baixe e extraia este ZIP em uma pasta própria.
2. Abra a pasta extraída no GitHub Codespaces ou VS Code.
3. Abra o terminal na pasta do projeto.
4. Confira se o Python 3 está disponível.

## 2. Instalar dependências
Execute:

```bash
python -m pip install -r requirements.txt
```

Se estiver usando um ambiente virtual, ative-o antes de instalar:
- Linux/Codespaces: `source .venv/bin/activate`
- Windows PowerShell: `.venv\\Scripts\\Activate.ps1`

## 3. Executar a aplicação
No terminal, execute:

```bash
python app.py
```

A aplicação estará disponível na porta indicada no terminal (o cenário utiliza a porta configurada no próprio `app.py`).
No GitHub Codespaces, abra a aba **Ports/Portas** e clique na URL da porta da aplicação.

## 4. Executar o scanner
Mantenha a aplicação em execução. Abra um segundo terminal na mesma pasta do projeto e execute:

```bash
python scanner.py
```

O scanner analisa somente a aplicação de laboratório configurada para este cenário.
Ele gera arquivos JSON e PDF na pasta `relatorios/` (quando executado com sucesso).

## 5. Consultar o painel local
Depois de gerar o relatório, abra a URL da aplicação e acrescente:

```text
/dashboard/
```

O painel local lê os arquivos JSON da pasta `relatorios/`. Se ainda não houver relatório,
execute o scanner primeiro e atualize a página.

## 6. Entrega do relatório ao professor
1. Localize o arquivo JSON mais recente em `relatorios/`.
2. Acesse a Central do Professor (endereço disponibilizado pelo professor).
3. Selecione o arquivo JSON no formulário **Enviar relatório JSON**.
4. Clique em **Receber relatório**.
5. Confirme com o professor que o cenário aparece na tabela de equipes recebidas.

**Importante:** envie o JSON, não o PDF. O PDF pode ser usado como evidência complementar.

## 7. Organização do trabalho
- Leia `DESAFIO.md` para conhecer o problema e os objetivos.
- Siga `ROTEIRO_DO_GRUPO.md` para executar as etapas.
- Registre evidências, resultados, riscos e recomendações.
- Não teste sites, sistemas ou redes reais. Use exclusivamente o ambiente fornecido no laboratório.
- Não altere o scanner para forçar resultados. Analise as evidências que ele produzir.

## 8. Arquivos do pacote
| Arquivo/pasta | Finalidade |
|---|---|
| `app.py` | Aplicação web do cenário |
| `scanner.py` | Verificações automatizadas do laboratório |
| `requirements.txt` | Dependências Python |
| `DESAFIO.md` | Enunciado do desafio |
| `ROTEIRO_DO_GRUPO.md` | Orientações e etapas de execução |
| `dashboard_integration.py` | Integração do painel local |
| `templates/` e `static/` | Interface do painel |
| `relatorios/` | Criada pelo scanner para armazenar relatórios |

## 9. Checklist de entrega
- [ ] Aplicação executada e acessível.
- [ ] Scanner executado sem erros.
- [ ] JSON gerado na pasta `relatorios/`.
- [ ] Painel local consultado.
- [ ] JSON enviado à Central do Professor.
- [ ] Desafio e roteiro concluídos.
