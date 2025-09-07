import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.core import engine
from sqlmodel import Session, select
from src.entities.curso import Curso

def add_cursos():
    with Session(engine) as session:
        cursos = [
            Curso(nome="Arquitetura e Urbanismo", duracao=5),
            Curso(nome="Engenharia de Software", duracao=4),
            Curso(nome="Design Gráfico", duracao=4),
        ]
        session.add_all(cursos)
        session.commit()

if __name__ == "__main__":
    add_cursos()
    print("Cursos adicionados com sucesso!")