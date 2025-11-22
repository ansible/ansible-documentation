# Inventário de Arquivos Stub para Remoção

**Data:** 2025-11-22
**Status:** Identificação Completa
**Prioridade:** CRÍTICA

Este documento lista todos os arquivos "stub" (redirecionamento) encontrados na documentação do Ansible que devem ser removidos como parte do plano de melhorias.

---

## 📊 Sumário

- **Total de arquivos stub identificados:** 54
- **Diretório principal afetado:** `/docs/docsite/rst/user_guide/`
- **Tamanho médio:** 5-6 linhas
- **Impacto:** Alto - Experiência do usuário degradada

---

## 🗂️ Lista Completa de Arquivos Stub

### Categoria: Conceitos Básicos (4 arquivos)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/basic_concepts.rst` | 7 | `:ref:\`Getting started with Ansible<basic_concepts>\`` |
| `user_guide/intro.rst` | 15 | Múltiplos (índice vazio) |
| `user_guide/intro_patterns.rst` | 5 | `:ref:\`intro_patterns\`` |
| `user_guide/cheatsheet.rst` | 6 | `:ref:\`cheatsheet\`` |

---

### Categoria: Inventário (3 arquivos)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/intro_inventory.rst` | 6 | `:ref:\`intro_inventory\`` |
| `user_guide/intro_dynamic_inventory.rst` | 6 | `:ref:\`intro_dynamic_inventory\`` |
| `user_guide/intro_adhoc.rst` | 6 | `:ref:\`intro_adhoc\`` |

---

### Categoria: Comandos e Conexões (3 arquivos)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/command_line_tools.rst` | 6 | `:ref:\`command_line_tools\`` |
| `user_guide/connection_details.rst` | 6 | `:ref:\`connections\`` |
| `user_guide/become.rst` | 6 | `:ref:\`playbooks_privilege_escalation\`` |

---

### Categoria: Playbooks - Básico (8 arquivos)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/playbooks.rst` | 5 | `:ref:\`working_with_playbooks\`` |
| `user_guide/playbooks_intro.rst` | 6 | `:ref:\`playbooks_intro\`` |
| `user_guide/playbooks_best_practices.rst` | 6 | `:ref:\`tips_and_tricks\`` |
| `user_guide/playbooks_reuse.rst` | 6 | `:ref:\`playbooks_reuse\`` |
| `user_guide/playbooks_reuse_includes.rst` | 6 | `:ref:\`playbooks_reuse\`` |
| `user_guide/playbooks_reuse_roles.rst` | 7 | `:ref:\`playbooks_reuse_roles\`` |
| `user_guide/playbooks_advanced_syntax.rst` | 6 | `:ref:\`playbooks_advanced_syntax\`` |
| `user_guide/sample_setup.rst` | 6 | `:ref:\`sample_setup\`` |

---

### Categoria: Playbooks - Controle de Fluxo (8 arquivos)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/playbooks_conditionals.rst` | 6 | `:ref:\`playbooks_conditionals\`` |
| `user_guide/playbooks_loops.rst` | 6 | `:ref:\`playbooks_loops\`` |
| `user_guide/playbooks_blocks.rst` | 6 | `:ref:\`playbooks_blocks\`` |
| `user_guide/playbooks_handlers.rst` | 5 | `:ref:\`handlers\`` |
| `user_guide/playbooks_tags.rst` | 6 | `:ref:\`tags\`` |
| `user_guide/playbooks_delegation.rst` | 5 | `:ref:\`playbooks_delegation\`` |
| `user_guide/playbooks_async.rst` | 5 | `:ref:\`playbooks_async\`` |
| `user_guide/playbooks_strategies.rst` | 5 | `:ref:\`playbooks_strategies\`` |

---

### Categoria: Playbooks - Variáveis e Dados (6 arquivos)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/playbooks_variables.rst` | 6 | `:ref:\`playbooks_variables\`` |
| `user_guide/playbooks_vars_facts.rst` | 6 | `:ref:\`vars_and_facts\`` |
| `user_guide/playbooks_prompts.rst` | 6 | `:ref:\`playbooks_prompts\`` |
| `user_guide/playbooks_filters.rst` | 6 | `:ref:\`playbooks_filters\`` |
| `user_guide/playbooks_filters_ipaddr.rst` | 8 | `:ref:\`plugins_in_ansible.utils\`` |
| `user_guide/complex_data_manipulation.rst` | 5 | `:ref:\`complex_data_manipulation\`` |

---

### Categoria: Playbooks - Testes e Lookups (3 arquivos)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/playbooks_tests.rst` | 6 | `:ref:\`playbooks_tests\`` |
| `user_guide/playbooks_lookups.rst` | 6 | `:ref:\`playbooks_lookups\`` |
| `user_guide/playbooks_module_defaults.rst` | 5 | `:ref:\`module_defaults\`` |

---

### Categoria: Playbooks - Debugging e Execução (4 arquivos)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/playbooks_debugger.rst` | 6 | `:ref:\`playbook_debugger\`` |
| `user_guide/playbooks_error_handling.rst` | 6 | `:ref:\`playbooks_error_handling\`` |
| `user_guide/playbooks_checkmode.rst` | 6 | `:ref:\`check_mode_dry\`` |
| `user_guide/playbooks_startnstep.rst` | 6 | `:ref:\`playbooks_start_and_step\`` |

---

### Categoria: Playbooks - Ambiente (1 arquivo)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/playbooks_environment.rst` | 5 | `:ref:\`playbooks_environment\`` |

---

### Categoria: Módulos e Plugins (4 arquivos)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/modules.rst` | 5 | `:ref:\`modules_plugins_index\`` |
| `user_guide/modules_intro.rst` | 5 | `:ref:\`modules_plugins_index\`` |
| `user_guide/modules_support.rst` | 6 | `:ref:\`modules_plugins_index\`` |
| `user_guide/plugin_filtering_config.rst` | 6 | `:ref:\`modules_plugins_index\`` |

---

### Categoria: Collections (1 arquivo)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/collections_using.rst` | 7 | `:ref:\`collections_index\`` |

---

### Categoria: Vault (1 arquivo)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/vault.rst` | 6 | `:ref:\`vault_guide_index\`` |

---

### Categoria: Windows (8 arquivos)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/intro_windows.rst` | 4 | `:ref:\`os_guide_index\`` |
| `user_guide/windows.rst` | 6 | `:ref:\`os_guide_index\`` |
| `user_guide/windows_setup.rst` | 5 | `:ref:\`working_with_windows\`` |
| `user_guide/windows_usage.rst` | 5 | `:ref:\`windows_usage\`` |
| `user_guide/windows_winrm.rst` | 5 | `:ref:\`windows_winrm\`` |
| `user_guide/windows_faq.rst` | 5 | `:ref:\`working_with_windows\`` |
| `user_guide/windows_dsc.rst` | 5 | `:ref:\`windows_dsc\`` |
| `user_guide/windows_performance.rst` | 5 | `:ref:\`windows_performance\`` |

---

### Categoria: BSD (1 arquivo)

| Arquivo | Linhas | Redireciona Para |
|---------|--------|------------------|
| `user_guide/intro_bsd.rst` | 5 | `:ref:\`working_with_bsd\`` |

---

## 📋 Análise por Categoria

### Distribuição de Stubs

```
Playbooks (Controle/Vars/Testes/Debug): 21 arquivos (39%)
Windows: 8 arquivos (15%)
Conceitos Básicos: 4 arquivos (7%)
Módulos/Plugins: 4 arquivos (7%)
Inventário: 3 arquivos (6%)
Comandos/Conexões: 3 arquivos (6%)
Outras: 11 arquivos (20%)
```

### Tamanho dos Arquivos

```
4 linhas: 1 arquivo
5 linhas: 19 arquivos (35%)
6 linhas: 31 arquivos (57%)
7 linhas: 2 arquivos
8 linhas: 1 arquivo
15 linhas: 1 arquivo (intro.rst - caso especial)
```

---

## 🔍 Padrões Identificados

### Padrão 1: Redirecionamento Simples
**Estrutura típica:**
```rst
:orphan:

*************
Título do Documento
*************

This page has moved to :ref:`new_location`.
```

**Quantidade:** 52 arquivos
**Nota:** Todos usam `:orphan:` directive (não aparece em toctree)

---

### Padrão 2: Redirecionamento com Contexto
**Estrutura:**
```rst
:orphan:

Título
======

You can find documentation for [topic] at :ref:`new_location`.
```

**Quantidade:** 2 arquivos (Windows)
**Exemplos:** `intro_windows.rst`, `windows.rst`

---

## 🎯 Plano de Remoção

### Fase 1: Preparação (Semana 1)

**Tarefas:**
1. [x] Identificar todos os arquivos stub
2. [ ] Auditar links que apontam para stubs
3. [ ] Criar mapeamento completo (old → new)
4. [ ] Identificar links externos conhecidos

**Comando para encontrar referências:**
```bash
# Para cada stub, encontrar referências
grep -r "user_guide/playbooks.rst" docs/docsite/rst/

# Ou buscar por referências do tipo :doc:
grep -r ":doc:\`.*user_guide/" docs/docsite/rst/
```

---

### Fase 2: Atualização de Links (Semana 1-2)

**Tarefas:**
1. [ ] Atualizar links internos na documentação
2. [ ] Atualizar links em `index.rst` files
3. [ ] Atualizar links em toctrees
4. [ ] Verificar links em comentários/exemplos

**Script auxiliar:**
```bash
# Substituir referências
find docs/docsite/rst -name "*.rst" -exec sed -i 's/:doc:`user_guide\/playbooks`/:doc:`playbook_guide\/playbooks_intro`/g' {} \;
```

---

### Fase 3: Configurar Redirecionamentos (Semana 2)

**Local:** `docs/docsite/rst/conf.py`

**Adicionar ao conf.py:**
```python
# HTTP 301 redirects para arquivos movidos
html_additional_pages = {}

# Ou usar extensão sphinx-reredirects
extensions.append('sphinx_reredirects')

redirects = {
    "user_guide/playbooks": "../playbook_guide/playbooks_intro.html",
    "user_guide/modules": "../module_plugin_guide/modules_plugins_index.html",
    # ... (adicionar todos os 54)
}
```

**Alternativa - Arquivo htaccess:**
```apache
# .htaccess ou configuração nginx
Redirect 301 /user_guide/playbooks.html /playbook_guide/playbooks_intro.html
```

---

### Fase 4: Validação (Semana 2)

**Tarefas:**
1. [ ] Build completo da documentação
2. [ ] Verificar zero broken links
3. [ ] Testar redirecionamentos
4. [ ] Verificar search index
5. [ ] Testar navegação

**Comandos de validação:**
```bash
# Build com linkcheck
nox -s "checkers(docs-build)"

# Ou
sphinx-build -b linkcheck docs/docsite/rst/ build/linkcheck/

# Verificar warnings
sphinx-build -W -b html docs/docsite/rst/ build/html/
```

---

### Fase 5: Remoção (Semana 3)

**Tarefas:**
1. [ ] Backup de arquivos (git já faz isso)
2. [ ] Deletar todos os 54 arquivos stub
3. [ ] Atualizar `.gitignore` se necessário
4. [ ] Commit com mensagem clara

**Comando de remoção:**
```bash
# Remover todos os stubs (CUIDADO!)
# Executar apenas após validação completa

cd docs/docsite/rst/user_guide/
rm -f basic_concepts.rst intro.rst intro_patterns.rst cheatsheet.rst \
      intro_inventory.rst intro_dynamic_inventory.rst intro_adhoc.rst \
      command_line_tools.rst connection_details.rst become.rst \
      playbooks.rst playbooks_*.rst \
      modules.rst modules_*.rst plugin_filtering_config.rst \
      collections_using.rst vault.rst \
      intro_windows.rst windows*.rst intro_bsd.rst \
      complex_data_manipulation.rst sample_setup.rst

# Verificar o que foi removido
git status
```

---

### Fase 6: Comunicação (Semana 3)

**Tarefas:**
1. [ ] Criar blog post sobre mudanças
2. [ ] Comunicar em mailing list
3. [ ] Atualizar changelog
4. [ ] Adicionar nota em release notes

**Template de comunicação:**
```markdown
# Documentation Structure Cleanup

As part of ongoing improvements, we've removed redirect-only stub files
from the user_guide/ directory. All content has been migrated to the new
structure (playbook_guide/, inventory_guide/, etc.).

If you have bookmarked links, they will automatically redirect to the
new locations. External documentation may need to be updated.

Old structure: /user_guide/playbooks.rst
New structure: /playbook_guide/playbooks_intro.rst

Full mapping: [link to DOCUMENTATION_GUIDE.md]
```

---

## 🚨 Riscos e Mitigações

### Risco 1: Links Externos Quebrados
**Probabilidade:** Alta
**Impacto:** Médio
**Mitigação:**
- Implementar HTTP 301 redirects permanentes
- Manter por pelo menos 2 major releases (1+ ano)
- Comunicar mudanças amplamente

---

### Risco 2: Search Engine Indexing
**Probabilidade:** Média
**Impacto:** Médio
**Mitigação:**
- Usar 301 redirects (preserva SEO)
- Submeter sitemap atualizado ao Google
- Aguardar reindexação natural

---

### Risco 3: Documentação de Terceiros
**Probabilidade:** Alta
**Impacto:** Baixo
**Mitigação:**
- Redirects automáticos resolvem
- Comunidade pode abrir PRs em repos conhecidos
- Adicionar aviso em release notes

---

### Risco 4: Usuários com Docs Offline
**Probabilidade:** Baixa
**Impacto:** Baixo
**Mitigação:**
- Incluir mapeamento em README
- Adicionar ao changelog
- Versão antiga ainda disponível em tags

---

## ✅ Checklist de Validação

**Antes da Remoção:**
- [ ] Todos os links internos atualizados
- [ ] Redirecionamentos configurados
- [ ] Build completo sem erros
- [ ] Zero broken links
- [ ] Mapeamento documentado
- [ ] Equipe informada

**Após a Remoção:**
- [ ] Build completo sem erros
- [ ] Redirecionamentos funcionando
- [ ] Navegação testada
- [ ] Search funcionando
- [ ] Comunicação enviada
- [ ] PR revisado e aprovado

---

## 📊 Métricas de Sucesso

### Antes da Limpeza
- Arquivos stub: 54
- Redirecionamentos: 0
- Estrutura: Duplicada (old + new)
- Confusão de usuários: Alta

### Após a Limpeza
- Arquivos stub: 0
- Redirecionamentos: 54 (automáticos)
- Estrutura: Única e clara
- Confusão de usuários: Baixa

### KPIs a Monitorar
- Broken links: deve ser 0
- User satisfaction: +20%
- Time to find info: -30%
- Documentation issues: -40%

---

## 🔗 Recursos Relacionados

- [Análise Detalhada](DOCUMENTATION_ANALYSIS.md)
- [Guia de Navegação](DOCUMENTATION_GUIDE.md)
- [Roadmap de Melhorias](IMPROVEMENT_ROADMAP.md)
- [Sphinx Redirects Extension](https://github.com/wpilibsuite/sphinxext-rediraffe)

---

## 📝 Comandos Úteis

### Análise de Stubs
```bash
# Listar todos os arquivos pequenos
find docs/docsite/rst/user_guide -name "*.rst" -size -500c

# Contar linhas de cada arquivo
find docs/docsite/rst/user_guide -name "*.rst" -exec wc -l {} \; | sort -n

# Ver conteúdo de arquivos pequenos
for f in docs/docsite/rst/user_guide/*.rst; do
  [ $(wc -l < "$f") -lt 10 ] && echo "=== $f ===" && cat "$f" && echo ""
done
```

### Busca de Referências
```bash
# Procurar referências a user_guide
grep -r "user_guide/" docs/docsite/rst/ --include="*.rst" | wc -l

# Procurar por tipo de link
grep -r ":doc:\`.*user_guide" docs/docsite/rst/ --include="*.rst"
grep -r ":ref:\`.*user_guide" docs/docsite/rst/ --include="*.rst"
```

### Validação
```bash
# Build e verificação de links
nox -s make
nox -s "checkers(docs-build)"

# Verificar warnings
sphinx-build -W -b html docs/docsite/rst/ build/html/ 2>&1 | grep -i warning
```

---

## 🎯 Próximos Passos Imediatos

**Esta Semana:**
1. ✅ Inventário completo criado
2. [ ] Auditar links que apontam para stubs
3. [ ] Começar atualização de links internos
4. [ ] Planejar configuração de redirects

**Próximas 2 Semanas:**
1. [ ] Completar atualização de links
2. [ ] Configurar redirecionamentos
3. [ ] Validar build completo
4. [ ] Remover stubs

**Próximo Mês:**
1. [ ] Monitorar redirecionamentos
2. [ ] Coletar feedback
3. [ ] Ajustar se necessário

---

**Documento mantido por:** Equipe de Documentação Ansible
**Última atualização:** 2025-11-22
**Status:** Identificação Completa - Pronto para Fase 1
