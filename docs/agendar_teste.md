# Plano de Testes: UC04 - Agendar Atendimento Acadêmico

## 1. Objetivo

Este documento detalha os cenários de teste para o caso de uso "UC04 - Agendar atendimento". O objetivo é validar a funcionalidade de criação de agendamentos, garantindo que todas as regras de negócio (prioridades, horários de funcionamento, notificações) e fluxos de exceção sejam tratados corretamente pela API.

## 2. Cenários de Teste

| ID do Cenário | Título                                | Prioridade | Regra de Negócio |
| :------------ | :------------------------------------ | :--------- | :--------------- |
| **CT-001** | Agendamento bem-sucedido (Aluno Comum) | Alta       | RB2, RB5         |
| **CT-002** | Falha ao agendar com data de início no passado | Alta       | RB2              |
| **CT-003** | Falha ao agendar com data de início posterior à de término | Alta       | -                |
| **CT-004** | Falha ao agendar por um aluno não existente | Média      | -                |
| **CT-005** | Falha ao agendar em um horário já ocupado | Alta       | -                |
| **CT-006** | Agendamento bem-sucedido (Aluno Prioritário - TCC) | Alta       | RB3, RB5         |
| **CT-007** | Falha ao agendar fora do horário de funcionamento | Alta       | RB2              |
| **CT-008** | Validação de envio de e-mail após agendamento | Alta       | RB5, UC06        |

---

## 3. Scripts de Teste

### **Cenário CT-001: Agendamento bem-sucedido (Aluno Comum)**
* **Preparação:**
    * O usuário `joana.silva@mackenzista.com.br` (aluno comum, sem prioridade) está autenticado. Seu `aluno_id = 10409516`.
* **Passos:** (Idêntico ao anterior, mas o contexto muda)
    1.  O usuário envia uma requisição `POST` para o endpoint `/agendamentos`.
    2.  No corpo da requisição, envia o JSON: `{"startTime": "2025-10-20T10:00:00", "endTime": "2025-10-20T10:30:00"}`
    3.  O sistema identifica o aluno pelo token quando cria o agendamento.
* **Resultado Esperado:**
    * O sistema retorna `HTTP 201 Created` com os dados do agendamento.
    * **O sistema dispara um evento para o serviço de e-mail (UC06) com os detalhes para o aluno `joana.silva@mackenzista.com.br`.**

---
*(Os cenários CT-002, CT-003, CT-004 e CT-005 permanecem os mesmos, pois validam lógicas fundamentais)*
---

### **Cenário CT-006: Agendamento bem-sucedido (Aluno Prioritário - TCC)**
* **Script:**
    * **Preparação:**
        * O usuário `maria.tcc@mackenzista.com.br` está autenticado. Seu `matricula = 10409999`.
        * O aluno com `matricula = 10409999` está marcado no sistema como `status = 3` (RB3).
    * **Passos:**
        1.  O usuário envia uma requisição `POST` para o endpoint `/agendamentos`.
        2.  No corpo da requisição, envia o JSON: `{"startTime": "2025-10-21T11:00:00", "endTime": "2025-10-21T11:30:00"}`
    * **Resultado Esperado:**
        * O sistema retorna `HTTP 201 Created`.
        * O agendamento é criado e o registro no banco de dados deve conter uma flag ou indicação de que foi um atendimento prioritário.
        * O sistema dispara o envio de e-mail de confirmação (UC06).

---

### **Cenário CT-007: Falha ao agendar fora do horário de funcionamento**
* **Script:**
    * **Preparação:**
        * O usuário `carlos.gomes@mackenzista.com.br` está autenticado.
        * A configuração de horários de funcionamento (UC01) define o atendimento como "Seg–Sex 09:00–12:00 e 14:00–18:00".
    * **Passos:**
        1.  O usuário envia uma requisição `POST` para o endpoint `/agendamentos`.
        2.  No corpo da requisição, tenta agendar para `13:00` (horário de almoço): `{"startTime": "2025-10-22T13:00:00", "endTime": "2025-10-22T13:30:00"}`
    * **Resultado Esperado:**
        * O sistema retorna `HTTP 400 Bad Request`.
        * A resposta contém uma mensagem de erro clara: "Fora do horário de expediente" ou similar.
        * Nenhum agendamento é criado.

---

### **Cenário CT-008: Validação de envio de e-mail após agendamento**
* **Script:**
    * **Preparação:**
        * O usuário `ana.souza@mackenzista.com.br` está autenticado.
        * O serviço de e-mail está configurado e um sistema de mock ou log de e-mails está ativo para o ambiente de testes.
    * **Passos:**
        1.  Executar os passos do cenário de sucesso `CT-001`.
    * **Resultado Esperado:**
        * Após o sistema retornar `HTTP 201 Created`, deve ser possível verificar no log do serviço de e-mail (ou no mock) que uma requisição de envio foi feita para o e-mail de `ana.souza`, contendo os dados corretos do agendamento (data, hora).

