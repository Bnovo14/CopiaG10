# Casos de Uso do Sistema de Agendamento

Este documento descreve os casos de uso para o tema "Sistema de Agendamento".

## 1. Sistema de Agendamento das Cortadoras a Laser

### 1.1. Liberar Agendamentos para Outros Semestres

* **Nome:** Agendar horário vago por aluno de semestre não prioritário.
* **Atores:** Aluno.
* **Pré-condições:**
    1.  O aluno está autenticado no sistema.
    2.  Existe um horário disponível que não foi reservado por alunos dos semestres prioritários dentro do prazo de antecedência.
* **Fluxo Principal:**
    1.  O aluno acessa a grade de horários das cortadoras a laser.
    2.  O sistema exibe os horários vagos.
    3.  O aluno seleciona um horário disponível.
    4.  O sistema confirma que o aluno pertence a um semestre elegível para agendamento de vagas remanescentes.
    5.  O aluno confirma o agendamento.
    6.  O sistema registra o agendamento em nome do aluno e atualiza a grade de horários.
* **Fluxos Alternativos:**
    * **1.1a. Horário ocupado:** Se, no momento da confirmação, outro aluno agendar o mesmo horário, o sistema informa que o horário não está mais disponível e solicita que o aluno escolha outro.
* **Pós-condições:**
    * O horário selecionado está associado ao aluno.
    * O aluno recebe uma confirmação do agendamento (via sistema ou e-mail).

### 1.2. Permitir Agendamento Até o Início do Horário

* **Nome:** Agendar horário imediatamente antes do início.
* **Atores:** Aluno.
* **Pré-condições:**
    1.  O aluno está autenticado no sistema.
    2.  Existe um horário livre cujo período de início ainda não passou.
* **Fluxo Principal:**
    1.  O aluno visualiza a grade de horários.
    2.  O aluno seleciona um horário que está prestes a começar.
    3.  O aluno confirma o agendamento.
    4.  O sistema valida que o tempo atual é anterior ao tempo de início do slot e realiza o agendamento.
* **Pós-condições:**
    * O horário é agendado com sucesso em nome do aluno.

### 1.3. Permitir Inclusão de Suplente Após o Início do Horário

* **Nome:** Incluir suplente em agendamento em andamento.
* **Atores:** Aluno Titular.
* **Pré-condições:**
    1.  O aluno titular possui um agendamento que já foi iniciado e ainda não foi finalizado.
    2.  O aluno suplente está cadastrado no sistema.
* **Fluxo Principal:**
    1.  O aluno titular acessa os detalhes do seu agendamento atual.
    2.  Ele seleciona a opção "Adicionar Suplente".
    3.  Ele informa os dados do aluno suplente (TIA ou nome).
    4.  O sistema valida o suplente e o associa ao agendamento.
* **Fluxos Alternativos:**
    * **1.3a. Suplente não encontrado:** Se o suplente informado não for um usuário válido, o sistema exibe uma mensagem de erro.
* **Pós-condições:**
    * O nome do suplente fica registrado no agendamento.

### 1.4. Permitir Cancelamento de Agendamento

* **Nome:** Cancelar agendamento.
* **Atores:** Aluno.
* **Pré-condições:**
    1.  O aluno possui um agendamento futuro.
* **Fluxo Principal:**
    1.  O aluno acessa a lista de seus agendamentos.
    2.  Ele seleciona o agendamento que deseja cancelar.
    3.  Ele confirma a operação de cancelamento.
    4.  O sistema verifica se o cancelamento está sendo feito com a antecedência mínima requerida (1 hora).
    5.  O sistema remove o agendamento e libera o horário.
* **Fluxos Alternativos:**
    * **1.4a. Prazo de cancelamento expirado:** Se o aluno tentar cancelar a menos de uma hora do início, o sistema exibe uma mensagem informando que o cancelamento não é mais permitido.
* **Pós-condições:**
    * O agendamento é removido do sistema.
    * O horário volta a ficar disponível para outros alunos.

### 1.5. Liberar Novo Agendamento Após Conclusão da Atividade

* **Nome:** Realizar novo agendamento após término de uso.
* **Atores:** Aluno.
* **Pré-condições:**
    1.  O aluno tinha um agendamento que acabou de ser concluído (o tempo do slot terminou).
* **Fluxo Principal:**
    1.  O sistema identifica que o horário do agendamento anterior do aluno foi finalizado.
    2.  O sistema remove qualquer bloqueio que impedia o aluno de agendar um novo horário.
    3.  O aluno acessa a grade e consegue agendar um novo horário normalmente.
* **Pós-condições:**
    * O aluno está apto a realizar um novo agendamento.

### 1.6. Enviar Notificação de Agendamento

* **Nome:** Notificar aluno sobre agendamento.
* **Atores:** Sistema.
* **Pré-condições:**
    1.  Um aluno possui um agendamento confirmado para o dia corrente.
* **Fluxo Principal:**
    1.  O sistema, em um horário pré-determinado (ex: início do dia), verifica todos os agendamentos do dia.
    2.  Para cada agendamento, o sistema envia um e-mail de lembrete para o endereço de e-mail cadastrado do aluno.
* **Pós-condições:**
    * O aluno recebe um e-mail com os detalhes do seu agendamento.

### 1.7. Incluir Alunos do 3º Semestre no Sistema

* **Nome:** Permitir agendamento por alunos do 3º semestre.
* **Atores:** Aluno (3º Semestre).
* **Pré-condições:**
    1.  O aluno está autenticado no sistema.
    2.  O sistema tem o registro de que o aluno cursa o 3º semestre de Arquitetura.
* **Fluxo Principal:**
    1.  O aluno do 3º semestre acessa a tela de agendamento.
    2.  O sistema valida suas permissões com base em seu semestre.
    3.  O sistema exibe os horários disponíveis para ele, de acordo com as regras de negócio.
    4.  O aluno realiza o agendamento.
* **Pós-condições:**
    * O agendamento é criado em nome do aluno do 3º semestre.

---

## 2. Sistema de Agendamento das Impressoras 3D

### 2.1. Casos de Uso Gerais e do Aluno

#### 2.1.1. Submeter Arquivo para Fila de Impressão

* **Nome:** Entrar na fila de espera para impressão 3D.
* **Atores:** Aluno.
* **Pré-condições:**
    1.  O aluno está autenticado.
    2.  O aluno pertence a um curso e semestre com permissão para usar as impressoras (Arquitetura, Urbanismo ou Design).
    3.  O aluno possui o arquivo de impressão (.stl, .obj, etc.) pronto.
* **Fluxo Principal:**
    1.  O aluno acessa a área de impressão 3D.
    2.  Ele seleciona a opção "Submeter para Impressão".
    3.  Ele preenche as informações solicitadas (ex: material, urgência).
    4.  Ele faz o upload do arquivo de impressão.
    5.  O sistema recebe o arquivo e cria um novo pedido de impressão com o status "Aguardando Análise".
    6.  O sistema adiciona o pedido à fila de espera.
* **Fluxos Alternativos:**
    * **2.1.1a. Aluno sem permissão:** Se o aluno não pertencer a um curso/semestre elegível, o sistema nega o acesso e informa o motivo.
    * **2.1.1b. Arquivo em formato inválido:** Se o formato do arquivo for incorreto, o sistema recusa o upload e informa os formatos aceitos.
* **Pós-condições:**
    * Um novo pedido de impressão é criado e visível para os laboratoristas.
    * O aluno pode visualizar seu pedido na fila com o status inicial.

#### 2.1.2. Visualizar Status da Impressão

* **Nome:** Consultar andamento do pedido de impressão.
* **Atores:** Aluno.
* **Pré-condições:**
    1.  O aluno possui um ou mais pedidos de impressão submetidos.
* **Fluxo Principal:**
    1.  O aluno acessa sua área pessoal no sistema.
    2.  Ele visualiza uma lista de seus pedidos de impressão.
    3.  O sistema exibe o status de cada pedido (ex: "Na Fila", "Apto para Impressão", "Em Impressão", "Finalizada", "Cancelado").
    4.  Para impressões em andamento, o sistema pode exibir o tempo estimado para conclusão.
* **Pós-condições:**
    * O aluno está ciente do estado atual de sua solicitação.

#### 2.1.3. Cancelar Pedido de Impressão

* **Nome:** Aluno cancela um pedido de impressão.
* **Atores:** Aluno.
* **Pré-condições:**
    1.  O aluno possui um pedido de impressão cujo status ainda permite cancelamento (ex: não está "Em Impressão" ou "Finalizada").
* **Fluxo Principal:**
    1.  O aluno visualiza seus pedidos.
    2.  Ele seleciona a opção "Cancelar" no pedido desejado.
    3.  Ele confirma o cancelamento.
    4.  O sistema altera o status do pedido para "Cancelado pelo Aluno".
* **Pós-condições:**
    * O pedido é removido da fila ativa de impressão.

#### 2.1.4. Acessar Manual de Preparação

* **Nome:** Consultar manual de preparação de arquivos.
* **Atores:** Aluno.
* **Pré-condições:** Nenhuma.
* **Fluxo Principal:**
    1.  O aluno acessa a área de impressão 3D.
    2.  Ele clica no link ou botão "Manual de Preparação de Arquivos".
    3.  O sistema exibe as informações ou redireciona para o documento com as instruções.
* **Pós-condições:**
    * O aluno tem acesso às diretrizes para preparar seu modelo para impressão.

### 2.2. Interface Administrativa (Laboratoristas)

#### 2.2.1. Gerenciar Fila de Impressão

* **Nome:** Analisar e gerenciar pedidos na fila.
* **Atores:** Laboratorista.
* **Pré-condições:**
    1.  O laboratorista está autenticado no sistema com permissões de administrador.
* **Fluxo Principal:**
    1.  O laboratorista acessa o painel de gerenciamento de impressão 3D.
    2.  O sistema exibe a lista de todos os pedidos, ordenados por chegada ou prioridade.
    3.  O laboratorista seleciona um pedido com status "Aguardando Análise".
    4.  Ele faz o download do arquivo enviado pelo aluno para checagem.
    5.  Após a análise, ele atualiza o status do pedido (ex: "Apto para Impressão", "Excede Tempo Máximo", "Arquivo com Erro").
    6.  Ele preenche informações adicionais, como tempo de impressão estimado e material necessário.
    7.  O sistema salva as alterações e notifica o aluno sobre a mudança de status.
* **Pós-condições:**
    * O pedido do aluno é avaliado e seu status é atualizado.

#### 2.2.2. Acessar Dados do Aluno

* **Nome:** Consultar informações de contato do aluno.
* **Atores:** Laboratorista.
* **Pré-condições:**
    1.  O laboratorista está visualizando um pedido de impressão.
* **Fluxo Principal:**
    1.  Dentro dos detalhes de um pedido, o laboratorista clica para ver as informações do solicitante.
    2.  O sistema exibe os dados do aluno: TIA, nome completo, curso e e-mail.
* **Pós-condições:**
    * O laboratorista tem as informações necessárias para contatar o aluno se houver alguma pendência.

#### 2.2.3. Atualizar Status do Processo de Impressão

* **Nome:** Alterar status de uma impressão em andamento.
* **Atores:** Laboratorista.
* **Pré-condições:**
    1.  Existe um pedido com status "Apto para Impressão".
* **Fluxo Principal:**
    1.  O laboratorista inicia a impressão da peça na impressora física.
    2.  No sistema, ele altera o status do pedido para "Em Impressão".
    3.  Quando a impressão é concluída, ele altera o status para "Finalizada - Aguardando Retirada".
    4.  O sistema notifica o aluno a cada mudança de status.
* **Pós-condições:**
    * O status do pedido reflete o estado real do processo de impressão.

#### 2.2.4. Cancelar Agendamento do Aluno

* **Nome:** Laboratorista cancela um pedido de impressão.
* **Atores:** Laboratorista.
* **Pré-condições:**
    1.  Existe um pedido de impressão ativo.
* **Fluxo Principal:**
    1.  O laboratorista localiza o pedido que precisa ser cancelado.
    2.  Ele seleciona a opção "Cancelar".
    3.  Ele informa um motivo para o cancelamento (ex: "Arquivo corrompido", "Falta de material").
    4.  O sistema altera o status para "Cancelado pelo Laboratório" e notifica o aluno, incluindo o motivo.
* **Pós-condições:**
    * O pedido é removido da fila ativa.