## 1. Visão Geral do Domínio
O sistema permite que **Alunos** solicitem **Atendimentos** por
**Agendamento** (slot de horário) ou **Fila do Dia** (entrada com posição). Há
**prioridades** (TCC, Formando), **Regras de Funcionamento**
(expediente/feriados) e **Notificações** por e-mail. A **Administração** configura
horários, sincroniza a lista de **Formandos** via o **Sistema de Matrículas** e
encerra o dia (reset da fila).
---
## 2. Diagrama de Classes (PlantUML)
```plantuml
@startuml
class Aluno {
+id: UUID
+ra: string
+nome: string
+email: string
+statusPrioridade: Prioridade?
+ehFormando: bool
+ehTCCAtivo: bool
}
class Admin {
+id: UUID
+nome: string
+email: string
}
abstract class Atendimento {
+id: UUID
+situacao: SituacaoAtendimento
+dataCriacao: DateTime
+dataAtendimento: DateTime?
+canceladoEm: DateTime?
+motivoCancelamento: string?
+noShow: bool
+canalSolicitacao: Canal
+prioridadeEfetiva: Prioridade
}
class Agendamento {
+slotInicio: DateTime
+slotFim: DateTime
}
class FilaDoDia {
+dataFila: Date
+posicao: int
+dataEntrada: DateTime
+dataSaida: DateTime?
}
class DoacaoPosicao {
+id: UUID
+dataHora: DateTime
+observacao: string?
}
class RegrasFuncionamento {
+id: UUID
+nomeCalendario: string
+zona: string
}
class FaixaHorario {
+id: UUID
+diaSemana: DiaSemana
+inicio: Time
+fim: Time
+ativo: bool
}
class Feriado {
+id: UUID
+data: Date
+descricao: string
}
class NotificacaoEmail {
+id: UUID
+tipo: TipoEmail
+enviadoEm: DateTime?
+statusEnvio: StatusEnvio
+destinatario: string
+assunto: string
}
class IntegracaoMatriculas {
+id: UUID
+ultimaSincronizacao: DateTime?
+fonte: string
+status: StatusIntegracao
}
enum Prioridade {
TCC
FORMANDO
NORMAL
}
enum SituacaoAtendimento {
NOVO
CONFIRMADO
EM_ATENDIMENTO
CONCLUIDO
CANCELADO
}
enum Canal {
WEB
PRESENCIAL
}
enum DiaSemana {
SEG
TER
QUA
QUI
SEX
SAB
DOM
}
enum TipoEmail {
CONF_AGENDAMENTO
CONF_FILA
LEMBRETE
FALHA_ENVIO
}
enum StatusEnvio {
PENDENTE
ENVIADO
FALHA
}
enum StatusIntegracao {
OK
FALHA
PARCIAL
}
Atendimento <|-- Agendamento
Atendimento <|-- FilaDoDia
Aluno "1" -- "0..*" Atendimento : solicita
Agendamento "1" -- "1" FaixaHorario : reserva >
FilaDoDia "1" -- "1" RegrasFuncionamento : valida >
RegrasFuncionamento "1" -- "1..*" FaixaHorario : contém >
RegrasFuncionamento "1" -- "0..*" Feriado : contém >
Atendimento "1" -- "0..*" NotificacaoEmail : gera >
Admin "1" -- "1" RegrasFuncionamento : configura >
Admin "1" -- "0..*" DoacaoPosicao : audita >
DoacaoPosicao "1" -- "1" FilaDoDia : origem >
DoacaoPosicao "1" -- "1" FilaDoDia : destino >
IntegracaoMatriculas "1" -- "0..*" Aluno : marca Formando >
Admin "1" -- "1" IntegracaoMatriculas : opera/sincroniza >

@enduml
```

