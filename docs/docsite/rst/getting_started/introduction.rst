.. _introduction_to_ansible:

***********************
Introdução ao Ansible
***********************

O Ansible oferece automação de código aberto que reduz a complexidade e funciona em qualquer lugar.
Usar o Ansible permite automatizar praticamente qualquer tarefa.
Aqui estão alguns casos de uso comuns para o Ansible:

    Eliminar repetição e simplificar fluxos de trabalho
    Gerenciar e manter a configuração do sistema
    Implantar continuamente software complexo
    Realizar atualizações contínuas sem tempo de inatividade

O Ansible utiliza scripts simples e legíveis por humanos, chamados playbooks, para automatizar suas tarefas.
Você declara o estado desejado de um sistema local ou remoto em seu playbook.
O Ansible garante que o sistema permaneça nesse estado.

Como tecnologia de automação, o Ansible é projetado com base nos seguintes princípios:

Arquitetura Agent-less
    Baixo excesso de manutenção ao evitar a instalação de software adicional em toda a infraestrutura de TI.

Simplicidade
    Os playbooks de automação utilizam uma sintaxe YAML direta para código que é legível como documentação. O Ansible também é descentralizado, usando as credenciais existentes do sistema operacional via SSH para acessar máquinas remotas.

Escalabilidade e flexibilidade
      Dimensione facilmente e rapidamente os sistemas que você automatiza por meio de um design modular que suporta uma ampla variedade de sistemas operacionais, plataformas de nuvem e dispositivos de rede.

Idempotência e previsibilidade
Quando o sistema está no estado descrito pelo seu playbook(Livro de Receita), o Ansible não altera nada, mesmo que o playbook seja executado várias vezes.

Está pronto para começar a utilizar o Ansible?
:ref:`Get up and running in a few easy steps<get_started_ansible>`.
