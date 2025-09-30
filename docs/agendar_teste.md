# Plano de Testes: Agendamento de Uso da Cortadora a Laser

## 1. Objetivo

Este documento detalha os cenários de teste e os scripts para o caso de uso "Agendar Uso da Cortadora a Laser". O objetivo é validar a funcionalidade de criação de agendamentos, garantindo que todas as regras de negócio, validações e fluxos de exceção sejam tratados corretamente pela API, com base no modelo de entrada `AgendamentoRequest`.

## 2. Cenários de Teste

| ID do Cenário | Título                                | Prioridade |
| :------------ | :------------------------------------ | :--------- |
| **CT-001** | Agendamento bem-sucedido              | Alta       |
| **CT-002** | Falha ao agendar com data de início no passado | Alta       |
| **CT-003** | Falha ao agendar com data de início posterior à data de término | Alta       |
| **CT-004** | Falha ao agendar por um aluno não existente | Média      |
| **CT-005** | Falha ao agendar em um horário já ocupado | Alta       |

---

## 3. Scripts de Teste

### **Cenário CT-001: Agendamento bem-sucedido**

* **Script:**
    * **Preparação:**
        * O usuário com login `ana.souza` deve estar autenticado no sistema.
        * O usuário `ana.souza` deve estar associado ao aluno com `aluno_id = 15`.
        * O aluno com `aluno_id = 15` deve estar cadastrado no banco de dados e pertencer ao curso com `curso_id = 3` (Engenharia de Produção).
        * Não deve existir nenhum agendamento para o dia **15 de Outubro de 2025, entre 14:00 e 15:00**.

    * **Passos:**
        1.  O usuário envia uma requisição `POST` para o endpoint `/agendamentos`.
        2.  No corpo da requisição, envia o seguinte JSON, conforme o modelo `AgendamentoRequest`:
            ```json
            {
              "startTime": "2025-10-15T14:00:00",
              "endTime": "2025-10-15T15:00:00"
            }
            ```

    * **Resultado Esperado:**
        * O sistema retorna o status code `HTTP 201 Created`.
        * O corpo da resposta contém o objeto JSON do agendamento criado, que inclui `"aluno_id": 15`, `"curso_id": 3`, e os horários enviados.
        * Um novo registro é criado na tabela `agendamentos` do banco de dados.

---

### **Cenário CT-002: Falha ao agendar com data de início no passado**

* **Script:**
    * **Preparação:**
        * O usuário com login `ana.souza` deve estar autenticado no sistema.
        * A data e hora atual do sistema é **30 de Setembro de 2025, 19:50**.

    * **Passos:**
        1.  O usuário envia uma requisição `POST` para o endpoint `/agendamentos`.
        2.  No corpo da requisição, envia o seguinte JSON com uma `startTime` no passado:
            ```json
            {
              "startTime": "2025-09-30T10:00:00",
              "endTime": "2025-09-30T11:00:00"
            }
            ```

    * **Resultado Esperado:**
        * O sistema retorna o status code `HTTP 400 Bad Request` (ou `422 Unprocessable Entity`).
        * O corpo da resposta contém uma mensagem de erro clara, como: `"A data de início não pode ser no passado"`.
        * Nenhum novo agendamento é criado no banco de dados.

---

### **Cenário CT-003: Falha ao agendar com data de início posterior à data de término**

* **Script:**
    * **Preparação:**
        * O usuário com login `ana.souza` deve estar autenticado no sistema.

    * **Passos:**
        1.  O usuário envia uma requisição `POST` para o endpoint `/agendamentos`.
        2.  No corpo da requisição, envia o seguinte JSON onde `startTime` é maior que `endTime`:
            ```json
            {
              "startTime": "2025-11-10T11:00:00",
              "endTime": "2025-11-10T10:00:00"
            }
            ```

    * **Resultado Esperado:**
        * O sistema retorna o status code `HTTP 400 Bad Request` (ou `422`).
        * O corpo da resposta contém uma mensagem de erro clara, como: `"A data de início deve ser anterior à data de término"`.
        * Nenhum novo agendamento é criado no banco de dados.

---

### **Cenário CT-004: Falha ao agendar por um aluno não existente**

* **Script:**
    * **Preparação:**
        * O usuário com login `fantasma` está autenticado (possui um token válido), mas seu `aluno_id` associado (`999`) **não corresponde** a nenhum registro na tabela de `alunos`.

    * **Passos:**
        1.  O usuário `fantasma` envia uma requisição `POST` para o endpoint `/agendamentos`.
        2.  No corpo da requisição, envia um JSON válido:
            ```json
            {
              "startTime": "2025-12-01T09:00:00",
              "endTime": "2025-12-01T10:00:00"
            }
            ```

    * **Resultado Esperado:**
        * O sistema retorna o status code `HTTP 404 Not Found`.
        * O corpo da resposta contém a mensagem de erro: `"Aluno não encontrado"`.
        * Nenhum novo agendamento é criado no banco de dados.

---

### **Cenário CT-005: Falha ao agendar em um horário já ocupado**

* **Observação:** Este cenário presume que a lógica de negócio para verificar conflitos de horário foi implementada (não está presente no código de exemplo, mas é essencial para o caso de uso real).

* **Script:**
    * **Preparação:**
        * O usuário com login `carlos.lima` deve estar autenticado no sistema.
        * Já existe um agendamento no banco de dados para o dia **20 de Outubro de 2025, das 10:00 às 11:00**.
    
    * **Passos:**
        1.  O usuário `carlos.lima` envia uma requisição `POST` para o endpoint `/agendamentos`.
        2.  No corpo da requisição, envia um JSON com um horário que se sobrepõe ao existente:
            ```json
            {
              "startTime": "2025-10-20T10:30:00",
              "endTime": "2025-10-20T11:30:00"
            }
            ```

    * **Resultado Esperado:**
        * O sistema retorna o status code `HTTP 409 Conflict`.
        * O corpo da resposta contém uma mensagem de erro clara, como: `"O horário solicitado já está ocupado"`.
        * Nenhum novo agendamento é criado no banco de dados.