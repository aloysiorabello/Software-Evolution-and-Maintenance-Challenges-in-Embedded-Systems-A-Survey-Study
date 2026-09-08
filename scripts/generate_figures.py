#!/usr/bin/env python3
"""Regenerate all manuscript figures from the anonymized analytical dataset."""

from pathlib import Path
import csv
import collections
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "analytical_dataset_anonymized.csv"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)

with DATA.open("r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

assert len(rows) == 36, f"Expected 36 analytical responses, found {len(rows)}"

def vals(sq, subset=None):
    subset = rows if subset is None else subset
    return [r[sq].strip() for r in subset]

def exact(sq, mapping=None, subset=None):
    c = collections.Counter()
    for x in vals(sq, subset):
        x = mapping.get(x, x) if mapping else x
        c[x] += 1
    return collections.OrderedDict(c)

def contains(sq, labels, subset=None):
    return collections.OrderedDict(
        (label, sum(label in x for x in vals(sq, subset))) for label in labels
    )

def barh(name, data, xlabel="Count"):
    labels = list(data.keys())[::-1]
    numbers = list(data.values())[::-1]
    fig, ax = plt.subplots(figsize=(10.8, max(4.6, 0.52 * len(labels) + 1.2)))
    bars = ax.barh(labels, numbers)
    ax.set_xlabel(xlabel)
    ax.grid(axis="x", linestyle="--", alpha=.45)
    ax.set_axisbelow(True)
    ax.bar_label(bars, padding=4)
    ax.margins(x=.08)
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight")
    plt.close(fig)

def bar(name, data, ylabel="Participants"):
    fig, ax = plt.subplots(figsize=(10.8, 6))
    bars = ax.bar(list(data.keys()), list(data.values()))
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", linestyle="--", alpha=.45)
    ax.set_axisbelow(True)
    ax.bar_label(bars, padding=3)
    ax.tick_params(axis="x", rotation=22)
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight")
    plt.close(fig)

def pie(name, data):
    labels, numbers = list(data.keys()), list(data.values())
    total = sum(numbers)
    def fmt(pct):
        n = int(round(pct * total / 100))
        return f"{pct:.1f}%\n(n={n})"
    fig, ax = plt.subplots(figsize=(6.8, 6.8))
    ax.pie(numbers, labels=labels, autopct=fmt, startangle=90)
    ax.axis("equal")
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight")
    plt.close(fig)

T = {
"Estabilidade":"Stability","Segurança":"Security","Legibilidade do código":"Code Readability",
"Facilidade de Integração":"Ease of Integration","Flexibilidade":"Flexibility","Eficiência":"Efficiency",
"Revisão de código":"Code Review","Refatoração de código":"Code Refactoring",
"Gerenciamento de configuração":"Configuration Management","Testes automatizados":"Automated Testing",
"Análise de obsolescência":"Obsolescence Analysis","Falta de documentação":"Lack of Documentation",
"Integração de novas tecnologias":"Integration of New Technologies","Limitações de hardware":"Hardware Limitations",
"Retrabalho frequente":"Frequent Rework","Complexidade do design":"Design Complexity",
"Inspeção de código":"Code Inspection","Revisão da dívida técnica":"Technical Debt Review",
"Melhoria na qualidade do software":"Improved Software Quality","Maior eficiência":"Greater Efficiency",
"Redução de defeitos":"Defect Reduction","Redução de custos":"Cost Reduction",
"Melhoria na coordenação de processos":"Improved Process Coordination",
"Colaboração com outros especialistas":"Collaboration with Specialists",
"Treinamento adicional":"Additional Training","Melhoria na documentação":"Improved Documentation",
"Ferramentas especializadas":"Specialized Tools","Automação de processos":"Process Automation",
"Implementação":"Implementation","Testes":"Testing","Descontinuação":"Discontinuation",
"Design":"Design","Planejamento":"Planning","Requisitos":"Requirements",
"Previsão de problemas futuros":"Forecasting Future Issues","Coordenação entre equipes":"Team Coordination",
"Identificação de requisitos":"Requirements Identification","Alocação de recursos":"Resource Allocation",
"Desempenho em tempo real":"Real-Time Performance","Qualidade do código":"Code Quality",
"Tempo de manutenção":"Maintenance Time","Consumo de energia":"Energy Consumption",
"Eficácia das ferramentas":"Tool Effectiveness","Ferramentas de monitoramento":"Monitoring Tools",
"Testes específicos":"Specific Tests","Avaliação manual":"Manual Evaluation","Benchmarking":"Benchmarking",
"Resistência da equipe":"Team Resistance","Complexidade das métricas":"Metric Complexity",
"Variedade de sistemas":"System Variety","Falta de ferramentas":"Lack of Tools",
"Customização de sprints":"Sprint Customization","Ajustes na documentação":"Documentation Adjustments",
"Integração contínua":"Continuous Integration","Redefinição de papéis":"Role Redefinition"
}
tr = lambda d: collections.OrderedDict((T.get(k,k),v) for k,v in d.items())

# Demographics
exp = exact("SQ03", {
"Menos de 1 ano":"Less than 1 year","1-3 anos":"1--3 years","3-5 anos":"3--5 years",
"5-10 anos":"5--10 years","Mais de 10 anos":"More than 10 years"})
exp = collections.OrderedDict((k,exp[k]) for k in
["1--3 years","3--5 years","More than 10 years","Less than 1 year","5--10 years"])
bar("1timeXP.png", exp)

roles = exact("SQ04", {
"Engenheiro de Software":"Software Engineer","Pesquisador":"Researcher","Gerente de Projetos":"Project Manager",
"Coordenador de TI":"IT Coordinator","Engenheiro de Dados":"Data Engineer",
"Engenheiro de Manufatura":"Manufacturing Engineer","Analista de Infraestrutura":"Infrastructure Analyst",
"CTO":"CTO","Engenheiro de Desenvolvimento do Produto":"Product Development Engineer","Professor":"Professor"})
barh("2funcAtual.png", collections.OrderedDict(sorted(roles.items(),key=lambda x:(-x[1],x[0]))),"Participants")

domains = exact("SQ05", {
"Educação":"Education","Saúde":"Healthcare","Utilities":"Utilities","Telecomunicações":"Telecommunications",
"Educação e Treinamento":"Education & Training","Ensino e Pesquisa Espacial":"Space R&D",
"Aeroespacial":"Aerospace","Robótica":"Robotics","Energia":"Energy","Meios de Pagamento":"Payment Systems",
"segurança":"Security","Automotivo":"Automotive","Finanças":"Finance","Financeiro":"Finance",
"Monitoramento ambiental":"Environmental Monitoring"})
barh("3dominioAtual.png", collections.OrderedDict(sorted(domains.items(),key=lambda x:(-x[1],x[0]))),"Participants")

sq07 = tr(contains("SQ07",["Estabilidade","Segurança","Legibilidade do código","Facilidade de Integração","Flexibilidade","Eficiência"]))
barh("4caracteristicas.png",sq07,"Selections")

sq08 = tr(contains("SQ08",["Revisão de código","Refatoração de código","Gerenciamento de configuração","Testes automatizados","Análise de obsolescência"]))
sq08["Other"]=2
sq09 = tr(contains("SQ09",["Falta de documentação","Integração de novas tecnologias","Limitações de hardware","Retrabalho frequente","Complexidade do design"]))
barh("14Dificuldades.png",sq09,"Selections")

sq10 = exact("SQ10",{"Sim":"Yes","Não":"No"})
pie("19utilModUnificado.png",collections.OrderedDict([("No",sq10["No"]),("Yes",sq10["Yes"])]))

# SQ11/SQ12 figures intentionally use only respondents without prior unified-model experience.
no_model = [r for r in rows if r["SQ10"].strip()=="Não"]
sq11 = tr(contains("SQ11",["Testes automatizados","Refatoração de código","Inspeção de código",
"Análise de obsolescência","Gerenciamento de configuração","Revisão da dívida técnica"],no_model))
barh("20componentes.png",sq11,"Selections among respondents without prior model use (n=34)")

sq12 = tr(contains("SQ12",["Melhoria na qualidade do software","Maior eficiência","Redução de defeitos",
"Redução de custos","Melhoria na coordenação de processos"],no_model))
sq12["Other: Time-Based Tracking"] = sum("Rastreamento de evolução temporal do projeto" in r["SQ12"] for r in no_model)
barh("21beneficios.png",sq12,"Selections among respondents without prior model use (n=34)")

tools=collections.Counter()
for field in vals("SQ13"):
    for x in [s.strip() for s in field.split(",") if s.strip()]:
        tools["Redmine" if x.upper()=="REDMINE" else x]+=1
barh("30ferramentasTotal.png",collections.OrderedDict(sorted(tools.items(),key=lambda x:(-x[1],x[0]))),
     "Participants reporting tool")

combined=collections.OrderedDict()
for k,v in sq09.items(): combined["Difficulty: "+k]=v
for k,v in sq08.items(): combined["Strategy: "+k]=v
barh("36dificuldadeEstrategiaTotal.png",combined,"Selections")

sq18=tr(contains("SQ18",["Colaboração com outros especialistas","Treinamento adicional","Melhoria na documentação",
"Ferramentas especializadas","Automação de processos"]))
sq18["Other / no mitigation reported"]=1
barh("37metodoEstrategiaTotal.png",sq18,"Selections")

sq19=exact("SQ19",{"Depende das tecnologias":"Depends on the Technology","Facilita":"Facilitates",
"Dificulta":"Hinders","Não tenho certeza":"Not Sure"})
barh("38tecEstrategiaTotal.png",collections.OrderedDict([
("Depends on the Technology",sq19["Depends on the Technology"]),("Facilitates",sq19["Facilitates"]),
("Hinders",sq19["Hinders"]),("Not Sure",sq19["Not Sure"])]),"Participants")

sq20=tr(contains("SQ20",["Implementação","Testes","Descontinuação","Design","Planejamento","Requisitos"]))
barh("39impactoCicloTotal.png",sq20,"Selections")

sq22=tr(contains("SQ22",["Previsão de problemas futuros","Integração de novas tecnologias",
"Coordenação entre equipes","Identificação de requisitos","Alocação de recursos"]))
sq22["Other"]=2
barh("44desafioPlanejamentoTotal.png",sq22,"Selections")

sq23=exact("SQ23",{"Sim":"Yes","Não":"No"})
pie("45retrabalhoTotal.png",collections.OrderedDict([("Yes",sq23["Yes"]),("No",sq23["No"])]))

def code_sq24(txt):
    t=txt.strip().lower()
    if not t: return "Not specified / not classifiable"
    if t in {"alta","muita"} or "quase todos os projetos" in t or ("toda empresa" in t and "todas as vezes" in t): return "High"
    if "frequência moderada" in t or t in {"as vezes","às vezes","algumas vezes"}: return "Moderate"
    if "frequência baixa" in t or t in {"baixa","raramente"}: return "Low"
    return "Not specified / not classifiable"

c=collections.Counter()
for r in rows:
    if r["SQ23"].strip()=="Sim": c[code_sq24(r["SQ24"])]+=1
sq24=collections.OrderedDict((k,c[k]) for k in ["Not specified / not classifiable","High","Moderate","Low"])
barh("46retrabalhoFreqTotal.png",sq24,"Respondents reporting rework (n=32)")

sq25=tr(contains("SQ25",["Desempenho em tempo real","Redução de defeitos","Qualidade do código",
"Tempo de manutenção","Consumo de energia","Eficácia das ferramentas"]))
sq25["Other"]=2
barh("47MetAvaliarManuTotal.png",sq25,"Selections")

sq26=tr(contains("SQ26",["Ferramentas de monitoramento","Testes específicos","Avaliação manual","Benchmarking"]))
sq26["Other"]=2
barh("48metTempoRealTotal.png",sq26,"Selections")

sq27=tr(contains("SQ27",["Resistência da equipe","Complexidade das métricas","Variedade de sistemas","Falta de ferramentas"]))
sq27["Other"]=2
barh("49metDificuldadeTotal.png",sq27,"Selections")

sq28=exact("SQ28",{"Sim":"Yes","Não":"No"})
pie("50utilizacaoXP.png",collections.OrderedDict([("Yes",sq28["Yes"]),("No",sq28["No"])]))

sq29=tr(contains("SQ29",["Customização de sprints","Ajustes na documentação","Integração contínua","Redefinição de papéis"]))
sq29["Other"]=5
barh("51adapXP.png",sq29,"Selections")

print(f"Generated 21 figures in {OUT}")
