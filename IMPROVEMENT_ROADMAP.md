# Roadmap de Melhorias da Documentação Ansible

**Status:** Em Planejamento
**Última Atualização:** 2025-11-22
**Versão:** 1.0

Este documento apresenta o roadmap executivo para melhorias da documentação do Ansible nos próximos 6 meses.

---

## 🎯 Visão Geral

### Objetivo Principal
Consolidar e melhorar a documentação do Ansible, eliminando redundâncias, completando lacunas e facilitando navegação para usuários de todos os níveis.

### Metas Mensuráveis
- ✅ Eliminar 100% dos arquivos stub (25+ arquivos)
- ✅ Reduzir arquivos com 1000+ linhas em 60%
- ✅ Completar documentação de instalação e troubleshooting
- ✅ Consolidar documentação fragmentada (Windows, Collections)
- ✅ Criar learning paths para 5 personas diferentes

---

## 📅 Timeline Executivo

```
Sprint 1-2 (Semanas 1-4)    → Correções Críticas
Sprint 3-4 (Semanas 5-8)    → Consolidação Estrutural
Sprint 5-8 (Semanas 9-16)   → Expansão de Conteúdo
Sprint 9-12 (Semanas 17-24) → Polimento e Novos Formatos
```

---

## 🚀 FASE 1: Correções Críticas (Semanas 1-4)

### Sprint 1 (Semanas 1-2)

**Objetivo:** Eliminar problemas mais urgentes que afetam experiência do usuário

#### Tarefas

**Semana 1**
- [ ] ✅ Criar documentos de análise e guias *(CONCLUÍDO)*
- [ ] Auditar todos os links internos que apontam para stubs
- [ ] Criar lista completa de arquivos stub para remoção
- [ ] Atualizar links internos para apontar diretamente ao destino
- [ ] Configurar redirecionamentos HTTP 301 no `conf.py`

**Semana 2**
- [ ] Deletar arquivos stub após validação
- [ ] Testar build completo da documentação
- [ ] Validar todos os links internos (zero broken links)
- [ ] Criar documento explicativo sobre nova estrutura em `/about/`
- [ ] Adicionar avisos de depreciação em `user_guide/index.rst`

**Entregáveis Sprint 1:**
- ✅ Documentação sem stubs
- ✅ Guia de estrutura publicado
- ✅ Zero broken links
- ✅ Avisos de depreciação claros

**Responsável:** Equipe de Documentação
**Review:** Final da semana 2

---

### Sprint 2 (Semanas 3-4)

**Objetivo:** Finalizar consolidação da estrutura user_guide

#### Tarefas

**Semana 3**
- [ ] Verificar migração completa de conteúdo de `user_guide/`
- [ ] Criar página de mapeamento (old path → new path)
- [ ] Atualizar índice principal com estrutura clara
- [ ] Adicionar breadcrumbs de navegação
- [ ] Documentar decisões de arquitetura

**Semana 4**
- [ ] Implementar redirecionamentos permanentes
- [ ] Adicionar nota de depreciação em todas as páginas antigas
- [ ] Criar timeline de remoção (ex: após Ansible 13)
- [ ] Comunicar mudanças para comunidade
- [ ] Atualizar links em repos externos conhecidos

**Entregáveis Sprint 2:**
- ✅ User guide completamente consolidado
- ✅ Mapeamento de paths publicado
- ✅ Comunicação para comunidade enviada

**Responsável:** Equipe de Documentação + Core Team
**Review:** Final da semana 4

---

## 🏗️ FASE 2: Consolidação Estrutural (Semanas 5-8)

### Sprint 3 (Semanas 5-6)

**Objetivo:** Consolidar documentação Windows e dividir arquivos grandes

#### Tarefas

**Semana 5 - Windows Documentation**
- [ ] Criar nova estrutura `/os_guide/windows/`
- [ ] Mapear todo conteúdo Windows existente
- [ ] Mover conteúdo de `/user_guide/windows_*`
- [ ] Mover conteúdo de `/dev_guide/developing_modules_general_windows.rst`
- [ ] Eliminar duplicações
- [ ] Criar hierarquia clara (básico → avançado → dev)

**Semana 6 - Dividir Arquivos Grandes**
- [ ] Dividir `playbooks_filters.rst` (2.205 linhas) em 5-6 arquivos
  - `playbooks_filters.rst` (índice)
  - `playbooks_filters_basic.rst`
  - `playbooks_filters_text.rst`
  - `playbooks_filters_list.rst`
  - `playbooks_filters_math.rst`
  - `playbooks_filters_network.rst`
- [ ] Atualizar toctree e referências
- [ ] Testar build

**Entregáveis Sprint 3:**
- ✅ Documentação Windows unificada em `/os_guide/windows/`
- ✅ `playbooks_filters.rst` dividido e organizado
- ✅ Build testado e funcionando

**Responsável:** Equipe de Documentação
**Review:** Final da semana 6

---

### Sprint 4 (Semanas 7-8)

**Objetivo:** Expandir installation guide e começar consolidação de collections

#### Tarefas

**Semana 7 - Installation Guide**
- [ ] Criar `installation_guide/troubleshooting.rst`
- [ ] Criar `installation_guide/special_environments.rst` (Docker, venv, WSL)
- [ ] Criar `installation_guide/upgrade_guide.rst`
- [ ] Criar `installation_guide/post_installation.rst`
- [ ] Criar `installation_guide/verification.rst`
- [ ] Criar `installation_guide/faq_installation.rst`
- [ ] Atualizar índice

**Semana 8 - Collections (Início)**
- [ ] Mapear toda documentação sobre collections
- [ ] Criar nova estrutura em `/collections_guide/`
  - `using_collections/`
  - `developing_collections/`
  - `maintaining_collections/`
- [ ] Começar migração de conteúdo de `/dev_guide/developing_collections_*`

**Entregáveis Sprint 4:**
- ✅ Installation guide completo e abrangente
- ✅ Nova estrutura de collections criada
- ✅ 50% do conteúdo de collections migrado

**Responsável:** Equipe de Documentação
**Review:** Final da semana 8

---

## 📚 FASE 3: Expansão de Conteúdo (Semanas 9-16)

### Sprint 5 (Semanas 9-10)

**Objetivo:** Completar consolidação de collections e dividir porting guides

#### Tarefas

**Semana 9 - Collections (Conclusão)**
- [ ] Completar migração de todo conteúdo sobre collections
- [ ] Organizar por persona (usar/desenvolver/manter)
- [ ] Atualizar referências em toda documentação
- [ ] Deletar duplicações
- [ ] Criar exemplos práticos

**Semana 10 - Porting Guides**
- [ ] Dividir `porting_guide_7.rst` (1.290 linhas)
- [ ] Dividir `porting_guide_12.rst` (1.523 linhas)
- [ ] Organizar por categoria (Breaking Changes, Deprecations, New Features)
- [ ] Mover guides para versão <2.9 para `/porting_guides/legacy/`
- [ ] Atualizar índice

**Entregáveis Sprint 5:**
- ✅ Documentação de collections completamente consolidada
- ✅ Porting guides divididos e organizados
- ✅ Guides legados arquivados

**Responsável:** Equipe de Documentação
**Review:** Final da semana 10

---

### Sprint 6 (Semanas 11-12)

**Objetivo:** Criar learning paths e melhorar navegação

#### Tarefas

**Semana 11 - Learning Paths**
- [ ] Criar learning path para Iniciantes
- [ ] Criar learning path para Intermediários
- [ ] Criar learning path para Avançados/Desenvolvedores
- [ ] Criar learning path para Network Engineers
- [ ] Criar learning path para Windows Admins
- [ ] Adicionar checkboxes de progresso
- [ ] Adicionar tempo estimado

**Semana 12 - Melhorias de Navegação**
- [ ] Criar índices por persona
- [ ] Adicionar breadcrumbs em todas as páginas
- [ ] Melhorar sidebar de navegação
- [ ] Criar mapa visual da documentação
- [ ] Adicionar "Related Topics" em páginas principais

**Entregáveis Sprint 6:**
- ✅ 5 learning paths completos e publicados
- ✅ Navegação melhorada com breadcrumbs
- ✅ Índices por persona funcionais

**Responsável:** Equipe de Documentação + UX
**Review:** Final da semana 12

---

### Sprint 7 (Semanas 13-14)

**Objetivo:** Expandir FAQ e melhorar Vault documentation

#### Tarefas

**Semana 13 - FAQ**
- [ ] Coletar perguntas comuns de issues/discussions
- [ ] Organizar FAQ por tópico
- [ ] Adicionar seção de Common Issues
- [ ] Adicionar seção de Troubleshooting
- [ ] Integrar com reference_appendices
- [ ] Adicionar links para documentação completa

**Semana 14 - Vault Guide**
- [ ] Reorganizar em estrutura clara (básico/usar/gerenciar/desenvolver)
- [ ] Adicionar mais exemplos práticos
- [ ] Integrar com security best practices
- [ ] Adicionar troubleshooting section
- [ ] Documentar integração com secret managers externos

**Entregáveis Sprint 7:**
- ✅ FAQ abrangente e organizada
- ✅ Vault documentation reorganizada e expandida
- ✅ Seção de troubleshooting completa

**Responsável:** Equipe de Documentação
**Review:** Final da semana 14

---

### Sprint 8 (Semanas 15-16)

**Objetivo:** Integrar/melhorar documentação de network

#### Tarefas

**Semana 15 - Análise e Decisão**
- [ ] Avaliar audiência e necessidades de network docs
- [ ] Decidir: integrar ou manter separado
- [ ] Documentar decisão e razões
- [ ] Comunicar para comunidade network

**Semana 16 - Implementação**
- [ ] Se integrar: mover para `/scenario_guides/network/`
- [ ] Se separar: melhorar cross-references
- [ ] Adicionar links claros no índice principal
- [ ] Explicar por que está separado (se aplicável)
- [ ] Melhorar navegação entre seções

**Entregáveis Sprint 8:**
- ✅ Documentação de network integrada ou melhorada
- ✅ Decisão documentada e comunicada
- ✅ Cross-references funcionais

**Responsável:** Equipe de Documentação + Network Team
**Review:** Final da semana 16

---

## 🎨 FASE 4: Polimento e Novos Formatos (Semanas 17-24)

### Sprint 9 (Semanas 17-18)

**Objetivo:** Documentar scenario guides e arquivar conteúdo legacy

#### Tarefas

**Semana 17 - Scenario Guides**
- [ ] Criar página explicando migração para collections
- [ ] Fornecer mapa de correspondência (old guide → new collection)
- [ ] Adicionar timeline de remoção
- [ ] Arquivar conteúdo legacy
- [ ] Adicionar avisos claros em cada guia descontinuado

**Semana 18 - Plugins Documentation**
- [ ] Criar guia para cada tipo de plugin
- [ ] Adicionar exemplos práticos
- [ ] Comparação entre tipos de plugins
- [ ] Quando usar cada tipo
- [ ] Desenvolver custom plugins

**Entregáveis Sprint 9:**
- ✅ Status de scenario guides clarificado
- ✅ Mapa de migração publicado
- ✅ Plugin documentation expandida

**Responsável:** Equipe de Documentação
**Review:** Final da semana 18

---

### Sprint 10 (Semanas 19-20)

**Objetivo:** Adicionar novos formatos de conteúdo

#### Tarefas

**Semana 19 - Quick References**
- [ ] Criar quick reference cards (PDFs)
  - Ansible Commands Cheat Sheet
  - Playbook Syntax Quick Reference
  - Module Common Parameters
  - Best Practices Checklist
- [ ] Criar troubleshooting decision trees
- [ ] Criar flowcharts para processos comuns

**Semana 20 - Interactive Content**
- [ ] Curar lista de video tutorials (YouTube)
- [ ] Criar links para interactive examples
- [ ] Adicionar "Try It Yourself" sections
- [ ] Criar exemplos executáveis (se possível)

**Entregáveis Sprint 10:**
- ✅ 4-5 quick reference PDFs
- ✅ Decision trees para troubleshooting
- ✅ Lista curada de video tutorials
- ✅ Interactive examples

**Responsável:** Equipe de Documentação + Community
**Review:** Final da semana 20

---

### Sprint 11 (Semanas 21-22)

**Objetivo:** Revisar e atualizar conteúdo existente

#### Tarefas

**Semana 21 - Content Audit**
- [ ] Revisar top 50 páginas mais acessadas
- [ ] Identificar conteúdo desatualizado
- [ ] Atualizar exemplos para versões atuais
- [ ] Verificar screenshots (se aplicável)
- [ ] Atualizar links externos

**Semana 22 - Best Practices Update**
- [ ] Revisar best practices em todas as seções
- [ ] Atualizar para refletir práticas atuais
- [ ] Adicionar exemplos modernos
- [ ] Incluir anti-patterns comuns
- [ ] Atualizar security recommendations

**Entregáveis Sprint 11:**
- ✅ Top 50 páginas revisadas e atualizadas
- ✅ Best practices atualizadas
- ✅ Conteúdo desatualizado identificado e corrigido

**Responsável:** Equipe de Documentação + SMEs
**Review:** Final da semana 22

---

### Sprint 12 (Semanas 23-24)

**Objetivo:** Finalização e lançamento

#### Tarefas

**Semana 23 - Testing & Validation**
- [ ] Build completo da documentação
- [ ] Validação de todos os links (interno e externo)
- [ ] Teste de navegação (UX testing)
- [ ] Verificação de spelling e gramática
- [ ] Review final por stakeholders

**Semana 24 - Launch & Communication**
- [ ] Publicar todas as mudanças
- [ ] Criar blog post anunciando melhorias
- [ ] Comunicar para mailing lists
- [ ] Apresentar em community meeting
- [ ] Coletar feedback inicial

**Entregáveis Sprint 12:**
- ✅ Documentação completamente revisada e publicada
- ✅ Blog post de lançamento
- ✅ Comunicação para comunidade
- ✅ Plano de coleta de feedback

**Responsável:** Equipe de Documentação + Marketing
**Review:** Final da semana 24

---

## 📊 Métricas e KPIs

### Métricas de Progresso

| Métrica | Baseline | Q1 Target | Q2 Target | Status |
|---------|----------|-----------|-----------|--------|
| Arquivos stub | 25+ | 0 | 0 | 🟡 Em Progresso |
| Arquivos 1000+ linhas | 5 | 2 | 0 | ⚪ Pendente |
| Diretórios deprecados | 2 | 0 | 0 | ⚪ Pendente |
| Links quebrados | ? | 0 | 0 | ⚪ Pendente |
| Seções de troubleshooting | 3 | 10 | 15 | ⚪ Pendente |
| Learning paths | 0 | 5 | 5 | ⚪ Pendente |
| Quick references | 0 | 4 | 8 | ⚪ Pendente |

### Métricas de Qualidade

**A serem medidas trimestralmente:**

- User satisfaction score (survey)
- Time to find information (UX testing)
- Documentation issues reported
- Community contributions
- Page views e engagement

### Critérios de Sucesso

✅ **Completo:**
- [ ] Zero arquivos stub
- [ ] Zero links quebrados
- [ ] Todas as seções principais completas
- [ ] Learning paths para 5 personas
- [ ] User satisfaction > 4.0/5.0

---

## 👥 Responsabilidades

### Core Documentation Team
- Execução de tasks
- Reviews de PRs
- Manutenção de roadmap
- Coordenação com stakeholders

### Subject Matter Experts (SMEs)
- Review técnico de conteúdo
- Validação de best practices
- Input sobre prioridades

### Community Contributors
- Contribuições de conteúdo
- Feedback e testing
- Translation (se aplicável)

### UX Team
- Design de navegação
- User testing
- Feedback de usabilidade

---

## 🔄 Processo de Revisão

### Weekly Check-ins
- Toda segunda-feira, 15:00 UTC
- Review de progresso da semana anterior
- Planejamento da semana atual
- Identificação de blockers

### Sprint Reviews
- Final de cada sprint (2 semanas)
- Demo de entregáveis
- Retrospectiva
- Ajustes de roadmap se necessário

### Monthly Stakeholder Update
- Primeira sexta-feira do mês
- Apresentação de progresso
- Discussão de decisões importantes
- Coleta de feedback

---

## 🚧 Riscos e Mitigações

### Risco 1: Sobrecarga da Equipe
**Probabilidade:** Média
**Impacto:** Alto
**Mitigação:**
- Priorizar tasks críticas
- Envolver comunidade
- Ajustar timeline se necessário

### Risco 2: Mudanças no Core Ansible
**Probabilidade:** Alta
**Impacto:** Médio
**Mitigação:**
- Coordenação próxima com core team
- Buffer time em sprints
- Documentação modular para fácil atualização

### Risco 3: Falta de Feedback da Comunidade
**Probabilidade:** Baixa
**Impacto:** Alto
**Mitigação:**
- Comunicação proativa
- Surveys regulares
- Canais múltiplos de feedback

### Risco 4: Breaking Changes na Estrutura
**Probabilidade:** Baixa
**Impacto:** Alto
**Mitigação:**
- Redirecionamentos permanentes
- Período de transição (6+ meses)
- Comunicação clara e antecipada

---

## 📢 Comunicação

### Canais de Comunicação

**Para Equipe:**
- Slack: #docs-team
- GitHub: Project board
- Weekly meetings

**Para Comunidade:**
- Mailing list: ansible-project@googlegroups.com
- Forum: https://forum.ansible.com/
- Blog: Ansible.com/blog
- Twitter: @ansible

### Momentos de Comunicação

| Marco | Audiência | Canal |
|-------|-----------|-------|
| Início do projeto | Comunidade | Blog post, mailing list |
| Final FASE 1 | Comunidade | Forum post |
| Final FASE 2 | Comunidade + Stakeholders | Blog post |
| Final FASE 3 | Todos | Blog post, apresentação |
| Lançamento final | Todos | Blog post, social media, email |

---

## 📝 Próximos Passos Imediatos

### Esta Semana
1. ✅ Finalizar documentos de análise e guias
2. [ ] Criar issues no GitHub para cada task de Sprint 1
3. [ ] Apresentar roadmap para core team
4. [ ] Obter buy-in dos stakeholders
5. [ ] Começar Sprint 1

### Próximas 2 Semanas
1. [ ] Completar Sprint 1 (eliminação de stubs)
2. [ ] Validar todos os links
3. [ ] Criar documento de estrutura
4. [ ] Comunicar para comunidade

### Próximo Mês
1. [ ] Completar FASE 1 (Correções Críticas)
2. [ ] Começar FASE 2 (Consolidação Estrutural)
3. [ ] Primeira coleta de feedback
4. [ ] Ajustar roadmap baseado em feedback

---

## 🔗 Recursos Relacionados

- [Análise Detalhada](DOCUMENTATION_ANALYSIS.md)
- [Guia de Navegação](DOCUMENTATION_GUIDE.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [GitHub Project Board](https://github.com/ansible/ansible-documentation/projects)

---

## 📅 Histórico de Versões

### v1.0 - 2025-11-22
- ✅ Roadmap inicial criado
- ✅ 4 fases definidas (24 semanas)
- ✅ Métricas e KPIs estabelecidos
- ✅ Responsabilidades atribuídas
- ✅ Riscos identificados

---

**Mantido por:** Equipe de Documentação Ansible
**Última atualização:** 2025-11-22
**Próxima revisão:** 2025-12-06 (Bi-weekly)

**Status do Projeto:** 🟢 On Track | 🟡 At Risk | 🔴 Delayed
**Status Atual:** 🟢 On Track (Fase de Planejamento)
