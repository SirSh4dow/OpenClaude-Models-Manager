# OpenClaude Models Manager ⚙️

Uma ferramenta com interface gráfica moderna desenvolvida para simplificar e gerenciar facilmente as configurações de ambiente do seu ecossistema **OpenClaude**. Edite chaves de API, escolha modelos dinamicamente e integre tudo de forma prática sem tocar diretamente nos arquivos locais do sistema.

## 🚀 Funcionalidades Principais

* **Interface Premium (GUI):** Desenvolvida com `customtkinter`, utilizando uma estética *Pitch Black / OLED Minimalista* para conforto visual e foco.
* **Automação de Arquivos:** Totalmente autônomo. Ele gerencia as rotas e automaticamente cria e direciona o arquivo físico `settings.json` pro seu caminho nativo de usuário (`~/.claude/`), prevenindo exclusões acidentais ou acessos falhos.
* **Internacionalização (i18n) Dinâmica:** Suporte nativo e troca em tempo-real (sem resetar aplicativo) entre Inglês (EN) e Português (PT-BR).
* **OpenRouter Integrado:** Acesso direto nativo com botões embarcados `Models Free` e `Gerar API Key`, impulsionando você direto para as páginas oficiais do OpenRouter.
* **Facilitadores Práticos:** Botões de Clipboard (`📋`) prontos para colar suas chaves de API com um clique, e modo de visibilidade seguro (máscara de senha) embutido.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Bibliotecas:** `customtkinter`, `json`, `os`, `webbrowser`, `sys`

## 📦 Como Usar

**1. Instale as dependências:**
Antes de iniciar, certifique-se de que a biblioteca principal de interface visual gráfica está presente na sua máquina:
```bash
pip install customtkinter
```

**2. Execute o Gerenciador:**
Dentro da pasta do projeto, inicie o arquivo Python padrão:
```bash
python config_manager.py
```

**3. Navegue:**
Apenas selecione o seu modelo favorito, cole sua chave de API e clique em **Salvar Modificações**. O aplicativo processará para o ambiente nativo e o deixará invisível rodando por debaixo dos panos, pronto para ser consumido pelos seus processos do terminal.

<br/>

> **Nota:** Não é necessário ter um arquivo `.json` previamente criado. O aplicativo foi programado para criar automaticamente um novo esqueleto limpo compatível na primeira vez que for aberto.
