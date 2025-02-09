# Sistema Multiagente de Recomendação de Disciplinas

Este sistema é um exemplo de **sistema multiagente inteligente** implementado em Python. Utiliza o framework Flask para a interface web e SQLite para o armazenamento dos dados. O sistema integra três agentes (Avaliador, Recomendador e Monitoramento) que trabalham de forma autônoma para:

- Avaliar o desempenho do aluno;
- Fornecer recomendações de disciplinas e a frequência ideal de monitoramento;
- Monitorar o progresso do aluno ao longo do tempo.

## Funcionalidades

- **Avaliação do Desempenho:**  
  O **Agente Avaliador** classifica o desempenho do aluno com base na nota informada, utilizando as seguintes regras:
  - **Código: baixo**  
    Desempenho baixo – *score < 5.0*
  - **Código: médio**  
    Desempenho intermediário – *5.0 ≤ score < 7.0*
  - **Código: alto**  
    Desempenho alto – *7.0 ≤ score < 9.0*
  - **Código: excel**  
    Desempenho excelente – *9.0 ≤ score ≤ 10.0*

- **Recomendações Personalizadas:**  
  O **Agente Recomendador** fornece recomendações de disciplinas e define a frequência de monitoramento conforme a classificação:
  - **Código: baixo:**  
    Reforço básico, exercícios extras – Monitoramento **5-7 vezes por semana**
  - **Código: médio:**  
    Atividades de prática moderada – Monitoramento **3-5 vezes por semana**
  - **Código: alto:**  
    Desafios adicionais avançados – Monitoramento **1-3 vezes por semana**
  - **Código: excel:**  
    Projetos especiais, mentorias – Monitoramento **1 vez por semana**

- **Monitoramento do Progresso:**  
  O **Agente de Monitoramento** compara o score atual do aluno com registros anteriores para detectar mudanças e sugere ajustes na frequência de acompanhamento.

## Requisitos

- **Python 3.x**  
  Certifique-se de ter o Python 3 instalado em sua máquina.

- **Flask**  
  Framework utilizado para a criação da interface web.
  ```bash
    pip install Flask

- **SQLite**  
  Banco de dados embutido no Python para armazenamento dos dados dos alunos.


## Instalação e Inicialização

1. **Clone o Repositório ou Baixe o Script**

   Caso você esteja utilizando um repositório, clone-o:
   ```bash
   git clone git@github.com:juvenalbruno/MASRES.git

2. **Siga os Passos:**  
   - Instale as dependências.
        pip install Flask

   - Inicie o servidor com o comando `python app.py`.
   - Acesse a aplicação via navegador em [http://127.0.0.1:5000/](http://127.0.0.1:5000/) e utilize a interface.

Com estas instruções, você estará pronto para iniciar e utilizar o sistema multiagente de recomendação de disciplinas.


