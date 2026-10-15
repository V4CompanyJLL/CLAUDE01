# Superpowers no Claude Code — Cola de comandos

Repo: https://github.com/obra/superpowers (v7, licença MIT)

## Instalação (rode dentro do Claude Code)

```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

Alternativa (marketplace oficial da Anthropic):

```
/plugin install superpowers@claude-plugins-official
```

Depois de instalar, feche e abra o Claude Code de novo.

> Neste repositório (CLAUDE01) já está configurado em `.claude/settings.json`:
> ao abrir o projeto, o Claude Code pede para confiar na pasta e instala o plugin.

## Gerenciar o plugin

| Comando | O que faz |
|---|---|
| `/plugin` | Abre o menu de plugins (instalar, ativar, desativar) |
| `/plugin marketplace update superpowers-marketplace` | Atualiza para a versão mais nova |
| `/plugin disable superpowers@superpowers-marketplace` | Desliga temporariamente |
| `/plugin enable superpowers@superpowers-marketplace` | Liga de novo |
| `/plugin uninstall superpowers@superpowers-marketplace` | Remove |
| `/skills` | Lista as skills instaladas |

## Skills (chame com `/superpowers:<nome>` ou só peça em português)

O Superpowers ativa as skills sozinho quando o assunto combina.
Se quiser forçar, digite o comando ou diga "use a skill X".

| Comando | Quando usar |
|---|---|
| `/superpowers:brainstorming` | Antes de criar qualquer coisa nova: refina a ideia com perguntas |
| `/superpowers:writing-plans` | Transformar a ideia/especificação em plano passo a passo |
| `/superpowers:executing-plans` | Executar o plano você mesmo, por etapas |
| `/superpowers:subagent-driven-development` | Executar o plano com subagentes, revisando cada tarefa |
| `/superpowers:dispatching-parallel-agents` | Várias tarefas independentes ao mesmo tempo |
| `/superpowers:test-driven-development` | Escrever o teste antes do código (vermelho → verde → refatora) |
| `/superpowers:systematic-debugging` | Investigar bug pela causa raiz antes de corrigir |
| `/superpowers:verification-before-completion` | Provar que funciona (rodar testes) antes de dizer "pronto" |
| `/superpowers:requesting-code-review` | Pedir revisão do código antes do merge |
| `/superpowers:receiving-code-review` | Avaliar o feedback de revisão com rigor |
| `/superpowers:using-git-worktrees` | Criar espaço isolado (worktree) para a nova feature |
| `/superpowers:finishing-a-development-branch` | Fechar a branch: merge, PR ou descartar |
| `/superpowers:writing-skills` | Criar ou editar suas próprias skills |
| `/superpowers:diagnosing-superpowers` | Descobrir por que uma sessão deu errado / relatar bug |
| `/superpowers:using-superpowers` | Carregado no início; ensina o Claude a usar as skills |

## Fluxo recomendado

1. `/superpowers:brainstorming` → descreva o que quer
2. `/superpowers:using-git-worktrees` → isola o trabalho
3. `/superpowers:writing-plans` → gera o plano
4. `/superpowers:subagent-driven-development` (ou `executing-plans`) → executa
5. `/superpowers:requesting-code-review` → revisa
6. `/superpowers:finishing-a-development-branch` → finaliza

Frases que funcionam direto: "vamos fazer um brainstorm sobre…",
"escreva um plano para…", "execute o plano", "debugue isso sistematicamente".
