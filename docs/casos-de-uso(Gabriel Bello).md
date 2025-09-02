# Casos de Uso — Sistema de Atendimento Acadêmico

## 1. Visão Geral do Sistema
O sistema gerencia atendimentos acadêmicos por agendamento e por fila diária, aplicando prioridades (alunos em TCC e formandos) e enviando notificações por e-mail.

### 1.1 Atores
- **Aluno** — solicita atendimento (agendamento ou fila), consulta status, cancela e pode doar posição.
- **Aluno Prioritário** — especialização de Aluno (está em TCC e/ou é Formando); participa dos mesmos casos com tratamento prioritário.
- **Admin (Atendente)** — configura horários, sincroniza lista de formandos, valida TCC, encerra o dia.
- **Serviço de E-mail** — provê envio de confirmações e notificações.
- **Sistema de Matrículas** — fonte para a lista de formandos do ano.

### 1.2 Regras de Negócio (RB)
- **RB1 — Fila é diária**: a fila zera ao final do expediente.
- **RB2 — Horário de funcionamento**: só é possível agendar/entrar na fila dentro das faixas definidas.
- **RB3 — Prioridade TCC**: alunos em TCC têm prioridade sobre os demais.
- **RB4 — Prioridade Formando**: formandos do ano têm prioridade acima dos demais (e abaixo/empatados com TCC, conforme política).
- **RB5 — Confirmação por e-mail**: toda criação de agendamento ou entrada na fila dispara e-mail.
- **RB6 — Doação de posição**: um aluno pode doar sua posição para outro aluno já na mesma fila, sem quebrar a política de prioridade.
- **RB7 — No-show**: o não comparecimento pode bloquear novo agendamento em janela definida (parâmetro).

### 1.3 Política de Ordenação da Fila
1) **Prioridade 1**: Alunos em TCC (RB3).  
2) **Prioridade 2**: Formandos do ano (RB4).  
3) **Prioridade 3**: Demais alunos (ordem de chegada).  
Empates são resolvidos por **timestamp de entrada**. Doação (RB6) não permite ultrapassar usuários de prioridade superior.


## 2. Diagrama de Casos de Uso (PlantText)
<details>
<summary>Ver código PlantUML</summary>
```
@startuml
left to right direction
skinparam actorStyle awesome
skinparam usecase {
  BackgroundColor #F9F9F9
  BorderColor #999999
  ArrowColor #666666
}
actor "Aluno" as Aluno
actor "Aluno Prioritário" as AlunoP
actor "Admin" as Admin
actor "Serviço de E-mail" as Email
actor "Sistema de Matrículas" as Matriculas

package "Sistema de Atendimento" {
  usecase "UC01\nConfigurar horários de funcionamento" as UC01
  usecase "UC02\nSincronizar/Validar lista de formandos" as UC02
  usecase "UC03\nComprovar status TCC" as UC03
  usecase "UC04\nAgendar atendimento" as UC04
  usecase "UC05\nEntrar na fila do dia" as UC05
  usecase "UC06\nEnviar e-mail de confirmação" as UC06
  usecase "UC07\nConsultar posição e status" as UC07
  usecase "UC08\nDoar posição na fila" as UC08
  usecase "UC09\nCancelar agendamento/saída da fila" as UC09
  usecase "UC10\nEncerrar dia e reiniciar fila" as UC10
}

'Aluno Prioritário é uma especialização de Aluno
AlunoP -|> Aluno

'Associações
Admin --> UC01
Admin --> UC02
Admin --> UC10

Aluno --> UC04
Aluno --> UC05
Aluno --> UC07
Aluno --> UC08
Aluno --> UC09

AlunoP --> UC03
AlunoP --> UC04
AlunoP --> UC05
AlunoP --> UC07
AlunoP --> UC08
AlunoP --> UC09

'Relações include
UC04 --> UC06 : <<include>>
UC05 --> UC06 : <<include>>

'Integrações
Matriculas --> UC02
Email --> UC06

note right of UC05
Política de fila:
1) TCC
2) Formando
3) Demais (chegada)
Doação não quebra prioridades
end note
@enduml
</details>

![text](https://uml.planttext.com/plantuml/png/TLJDRjim3BxhAOZkqEKGjFbFYY9ebhR03WEATTif5yvcNA6ob4boYstTmmmx53lqk2VmYusIxRJsi0H8HEhxI7uKfJFdqVeYLqBHreCtO6Lsuo6LbX8lZHRkLkeTMim14s_ijV-g2F2UdCdfnMRXA457y5q0lC7aDhEcqEdQA6FXrUKYVCEEiIdPshk87_Qkh3NtjNCQF-A7YDdWOAKARGu07SHLomrNLXehVVcJ_vynLtjGcajT-SEgSL-JlPFbeu6KuAAVerGHSn5MUunqdd8Ca7VeRVcK50fTn0LRHbE87Il5Z5hubIUTofoqvvf2EvhM77nS7mysUctqLcQ5HGitniRQNU1j2vrmmx5cSgQ0x_276tqjTMADbj_G7dr29LCEf3XzJBurDaUT6jS467O2Z481-SwQEwOnoHSEFgpN3NpKWOytUfMn7WRZIrqLUjn1JpRwGlkWJ2DifUAIkCiI6_oaWvy6_9raFCLp20gIq1uMKJwMl_Q9fXtYBBRH5Ogd5tR6oOW6gXKrj5c7Dj_eSzDYr7KsX7c7iE0yg1DIGN_iGzH_vB1yIbbTcxreimV7GLv2DZI4ky3bMP9Q9a7m2zxWcCTT7Fuxqb3-XeA7YjoEcAJuoAkgmvJ5sr3DE_GVbhM3mpXd6Cp0F-H477pezvVLCBNCOSlaAgfmpVQuRKxQvgnjpjlcGknBgnoZZZtks9EEFUlOyuxD2GxVyx5KCe6lX2fI4Y5o0vd22PoUrZlBPTYR_6zF7BxLdZBRjEtvZZytAxuF-m12QEEfVYtDjj9mPLJvv6LINKK-uHCnw8Nh9OOzkAolfXZru9pV2kdWTN936QRO4poMzK26doy5VRO8kpWBAQPS4SyUX8pYZ5VyNly5)


## 3. Casos de Uso (descrição detalhada)

### UC01 — Configurar horários de funcionamento
**Atores:** Admin  
**Objetivo:** Definir faixas de atendimento válidas (diárias/semanais, feriados).  
**Pré-condições:** Admin autenticado.  
**Pós-condições:** Faixas persistidas e aplicadas em validações de agenda/fila.  
**Cenário de sucesso principal:**
1. Admin acessa a tela de configuração de horários.
2. Informa faixas (ex.: Seg–Sex 09:00–12:00 e 14:00–18:00) e exceções (feriados).
3. Sistema valida sobreposições e formato.
4. Sistema salva e publica as faixas.
**Extensões/Exceções:**
- 1a. Faixa inválida/sobreposta → sistema rejeita e informa inconsistências.
**Regras:** RB2.

### UC02 — Synchronizar/Validar lista de formandos
**Atores:** Admin, Sistema de Matrículas  
**Objetivo:** Manter atualizada a lista de alunos formandos do ano.  
**Pré-condições:** Integração ativa ou carga manual.  
**Pós-condições:** Lista consolidada; alunos marcados como “Formando”.  
**Cenário de sucesso principal:**
1. Admin inicia sincronização.
2. Sistema consulta o Sistema de Matrículas.
3. Sistema reconcilia diferenças e atualiza marcação de Formando.
4. Log de sincronização é registrado.
**Extensões/Exceções:**
- 2a. Falha de integração → sistema mantém lista anterior e alerta Admin.  
**Regras:** RB4.

### UC03 — Comprovar status TCC
**Atores:** Aluno (Prioritário), Admin  
**Objetivo:** Habilitar prioridade para aluno em TCC.  
**Pré-condições:** Aluno autenticado.  
**Pós-condições:** Aluno marcado como “TCC ativo”.  
**Cenário de sucesso principal:**
1. Aluno solicita prioridade TCC (anexa comprovação, se exigido).
2. Admin revisa comprovação/registro acadêmico.
3. Sistema marca aluno como “TCC ativo” (com validade/semestre).  
**Extensões/Exceções:**
- 2a. Evidência insuficiente → pedido negado, aluno permanece sem prioridade.  
**Regras:** RB3.

### UC04 — Agendar atendimento
**Atores:** Aluno / Aluno Prioritário  
**Objetivo:** Reservar um horário disponível dentro do expediente.  
**Pré-condições:** Horários configurados (UC01); usuário autenticado.  
**Pós-condições:** Agendamento criado; e-mail enviado (UC06).  
**Cenário de sucesso principal:**
1. Aluno escolhe data e slot disponível.
2. Sistema valida expediente (RB2) e conflitos.
3. Sistema aplica prioridade (se for o caso) para regras internas (ex.: overbooking controlado, lista de espera).
4. Sistema confirma e **inclui UC06** (envio de e-mail).
**Extensões/Exceções:**
- 1a. Slot indisponível → sistema sugere alternativas.
- 2a. Fora do expediente → rejeita e exibe horários válidos.
**Regras:** RB1, RB2, RB3, RB4, RB5, RB7.

### UC05 — Entrar na fila do dia
**Atores:** Aluno / Aluno Prioritário  
**Objetivo:** Ingressar na fila de atendimento do dia corrente.  
**Pré-condições:** Dentro do horário de funcionamento.  
**Pós-condições:** Posição atribuída; e-mail enviado (UC06).  
**Cenário de sucesso principal:**
1. Aluno solicita entrada na fila.
2. Sistema valida expediente (RB2).
3. Sistema calcula posição conforme política (prioridade/chegada).
4. Sistema confirma e **inclui UC06** (envio de e-mail).
**Extensões/Exceções:**
- 2a. Fila encerrada/expediente próximo do fim → rejeita com mensagem.
**Regras:** RB1, RB2, RB3, RB4, RB5.

### UC06 — Enviar e-mail de confirmação
**Atores:** Serviço de E-mail  
**Objetivo:** Notificar aluno sobre criação de agendamento/entrada na fila.  
**Pré-condições:** UC04 ou UC05 concluídos.  
**Pós-condições:** Mensagem enviada e logada.  
**Cenário de sucesso principal:**
1. Sistema compõe e-mail (data, hora, instruções).
2. Envia via serviço de e-mail.
3. Registra status (entregue/erro).  
**Extensões/Exceções:**
- 2a. Falha de envio → re-tentativas automáticas + botão de reenvio manual.  
**Regras:** RB5.

### UC07 — Consultar posição e status
**Atores:** Aluno / Aluno Prioritário  
**Objetivo:** Acompanhar posição na fila e/ou detalhes do agendamento.  
**Pré-condições:** Posição ou agendamento existente.  
**Pós-condições:** Nenhuma.  
**Cenário de sucesso principal:**
1. Usuário acessa “Meus atendimentos”.
2. Sistema mostra posição em tempo quase real e estimativa (ETA), se disponível.
3. Sistema exibe histórico e políticas aplicáveis.  
**Extensões/Exceções:**
- 2a. Fila encerrada → exibe status final do dia.
- 2b. Posição inexistente → mensagem orientativa.

### UC08 — Doar posição na fila
**Atores:** Aluno (doador) e Aluno (destinatário) — ambos na fila  
**Objetivo:** Transferir posição dentro da mesma fila diária.  
**Pré-condições:** Ambos possuem posição válida **na mesma fila**.  
**Pós-condições:** Posições atualizadas e auditadas.  
**Cenário de sucesso principal:**
1. Doador escolhe destinatário.
2. Sistema verifica elegibilidade (mesma fila; sem quebra de prioridade).
3. Sistema recalcula ordenação preservando prioridades globais.
4. Sistema registra auditoria e confirma.  
**Extensões/Exceções:**
- 2a. Destinatário não está na fila → operação negada.
- 2b. Troca implicaria ultrapassar prioridade superior → operação negada.
**Regras:** RB6.

### UC09 — Cancelar agendamento/saída da fila
**Atores:** Aluno / Admin  
**Objetivo:** Liberar slot/posição para redistribuição.  
**Pré-condições:** Agendamento/posição existente.  
**Pós-condições:** Posição/slot liberado; fila ajustada.  
**Cenário de sucesso principal:**
1. Usuário solicita cancelamento.
2. Sistema aplica política de janela (RB7).
3. Sistema libera recurso e realoca próximos conforme prioridade.  
**Extensões/Exceções:**
- 2a. Janela expirada → marca como no-show; pode aplicar bloqueio (RB7).

### UC10 — Encerrar dia e reiniciar fila
**Atores:** Admin  
**Objetivo:** Fechar operação diária e limpar a fila.  
**Pré-condições:** Fim do expediente.  
**Pós-condições:** Fila zerada; relatórios/estatísticas do dia arquivados.  
**Cenário de sucesso principal:**
1. Admin aciona “Encerrar dia”.
2. Sistema finaliza atendimentos abertos conforme regra institucional.
3. Sistema limpa fila e arquiva logs/estatísticas.  
**Extensões/Exceções:**
- 2a. Há atendimentos em execução → sistema alerta e permite encerramento forçado com registro.  
**Regras:** RB1.
