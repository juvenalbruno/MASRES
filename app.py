#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# ==============================================================================
# Inicialização do Banco de Dados (incluindo curso e disciplina)
# ==============================================================================
def init_db():
    conn = sqlite3.connect('alunos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS desempenho (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            score REAL,
            classificacao TEXT,
            codigo TEXT,
            curso TEXT,
            disciplina TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ==============================================================================
# Função de classificação (Base de Regras Atualizada)
# ==============================================================================
def classify_performance(score):
    """
    Classifica o desempenho do aluno com base na nota (score):
      - código: 'baixo' / classificação: Desempenho baixo / faixa: score < 5.0
      - código: 'médio' / classificação: Desempenho intermediário / faixa: 5.0 <= score < 7.0
      - código: 'alto' / classificação: Desempenho alto / faixa: 7.0 <= score < 9.0
      - código: 'excel' / classificação: Desempenho excelente / faixa: 9.0 <= score <= 10.0
    """
    if score < 5.0:
        return 'baixo', 'Desempenho baixo'
    elif score < 7.0:
        return 'médio', 'Desempenho intermediário'
    elif score < 9.0:
        return 'alto', 'Desempenho alto'
    else:
        return 'excel', 'Desempenho excelente'

# ==============================================================================
# Definição dos Agentes com base nas tabelas PEAS atualizadas
# ==============================================================================

class AvaliadorAgent:
    """
    Agente Avaliador
    -------------------------
    PEAS:
      - Performance Measure: Precisão na avaliação das dificuldades do aluno;
                              Taxa de sucesso nas recomendações.
      - Environment: Parcialmente observável, não determinístico.
      - Actuators: Interface de avaliação, gera feedbacks com base no desempenho.
      - Sensors: Registros de notas e interações do aluno.
    """
    def evaluate(self, score, interacoes=None):
        codigo, classificacao = classify_performance(score)
        feedback = f"O aluno apresenta {classificacao} (código: {codigo})."
        return codigo, classificacao, feedback

class RecomendadorAgent:
    """
    Agente Recomendador
    -------------------------
    PEAS:
      - Performance Measure: Precisão e relevância das recomendações, tempo de resposta.
      - Environment: Parcialmente observável, não determinístico, sequencial.
      - Actuators: Interface de recomendação (exibe os materiais sugeridos).
      - Sensors: Dados sobre as dificuldades do aluno e seu histórico de interações.
    """
    def recommend(self, codigo, classificacao, historico_interacoes=None):
        if codigo == 'baixo':
            recomendacao = "Reforço básico, exercícios extras"
            frequencia = "5-7 vezes por semana"
        elif codigo == 'médio':
            recomendacao = "Atividades de prática moderada"
            frequencia = "3-5 vezes por semana"
        elif codigo == 'alto':
            recomendacao = "Desafios adicionais avançados"
            frequencia = "1-3 vezes por semana"
        elif codigo == 'excel':
            recomendacao = "Projetos especiais, mentorias"
            frequencia = "1 vez por semana"
        else:
            recomendacao = "Nenhuma recomendação disponível"
            frequencia = "N/A"
        return recomendacao, frequencia

class MonitoramentoAgent:
    """
    Agente de Monitoramento
    -------------------------
    PEAS:
      - Performance Measure: Eficiência em ajustar as recomendações conforme o progresso do aluno.
      - Environment: Dinâmico, discretizado, multiagente.
      - Actuators: Interface para ajustar recomendações conforme o progresso do aluno.
      - Sensors: Dados do desempenho contínuo do aluno e sua interação com o sistema.
    """
    def monitorar(self, nome, novo_score):
        # Consultar o último registro do aluno no banco de dados
        conn = sqlite3.connect('alunos.db')
        c = conn.cursor()
        c.execute("""
            SELECT score, timestamp FROM desempenho
            WHERE nome = ?
            ORDER BY timestamp DESC LIMIT 1
        """, (nome,))
        resultado = c.fetchone()
        conn.close()
        
        # Obter a frequência recomendada com base no novo score
        codigo, _ = classify_performance(novo_score)
        if codigo == 'baixo':
            freq = "5-7 vezes por semana"
        elif codigo == 'médio':
            freq = "3-5 vezes por semana"
        elif codigo == 'alto':
            freq = "1-3 vezes por semana"
        elif codigo == 'excel':
            freq = "1 vez por semana"
        else:
            freq = "N/A"
            
        if resultado:
            score_anterior, timestamp = resultado
            if novo_score != score_anterior:
                ajuste = (f"Progresso detectado: o score anterior era {score_anterior} e "
                          f"agora é {novo_score}. Recomenda-se monitoramento: {freq}.")
            else:
                ajuste = f"Nenhuma mudança significativa no desempenho detectada. Recomenda-se monitoramento: {freq}."
        else:
            ajuste = f"Primeira avaliação registrada. Recomenda-se monitoramento: {freq}."
        return ajuste

# ==============================================================================
# Instanciação dos Agentes
# ==============================================================================
avaliador = AvaliadorAgent()
recomendador = RecomendadorAgent()
monitoramento = MonitoramentoAgent()

# ==============================================================================
# Templates HTML (utilizando render_template_string)
# ==============================================================================
template_form = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Sistema Multiagente de Recomendação</title>
    <script>
        // Mapeamento de disciplinas para cada curso
        const disciplinesByCourse = {
            "desenvolvimento": ["Programação Orientada a Objetos", "Desenvolvimento Web", "Banco de Dados"],
            "analise": ["Estatística", "Machine Learning", "Data Mining"]
        };

        function updateDisciplineOptions() {
            var courseSelect = document.getElementById('course');
            var disciplineSelect = document.getElementById('discipline');
            var selectedCourse = courseSelect.value;
            var disciplines = disciplinesByCourse[selectedCourse];
            disciplineSelect.innerHTML = "";
            for (var i = 0; i < disciplines.length; i++) {
                var option = document.createElement("option");
                option.value = disciplines[i];
                option.text = disciplines[i];
                disciplineSelect.appendChild(option);
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            updateDisciplineOptions();
            document.getElementById('course').addEventListener('change', updateDisciplineOptions);
        });
    </script>
</head>
<body>
    <h1>Sistema de Recomendação de Disciplinas</h1>
    <form method="post">
        Nome do Aluno: <input type="text" name="nome" required><br><br>
        Score (Nota): <input type="text" name="score" required><br><br>
        Curso:
        <select id="course" name="course">
            <option value="desenvolvimento">Desenvolvimento de Sistema</option>
            <option value="analise">Análise de Dados</option>
        </select>
        <br><br>
        Disciplina:
        <select id="discipline" name="discipline">
            <!-- Opções serão atualizadas via JavaScript -->
        </select>
        <br><br>
        <input type="submit" value="Enviar">
    </form>
</body>
</html>
'''

template_resultado = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Resultado da Avaliação</title>
</head>
<body>
    <h1>Resultado para {{ nome }}</h1>
    <p><strong>Score:</strong> {{ score }}</p>
    <p><strong>Classificação:</strong> {{ classificacao }}</p>
    <p><strong>Feedback do Avaliador:</strong> {{ feedback }}</p>
    <p><strong>Curso:</strong> {{ curso }}</p>
    <p><strong>Disciplina:</strong> {{ disciplina }}</p>
    <p><strong>Recomendação principal:</strong> {{ recomendacao }}</p>
    <p><strong>Frequência de monitoramento:</strong> {{ frequencia }}</p>
    <p><strong>Ajuste Monitorado:</strong> {{ ajuste }}</p>
    <br>
    <a href="/">Voltar</a>
</body>
</html>
'''

# ==============================================================================
# Rotas do Flask
# ==============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        try:
            score = float(request.form.get('score'))
        except (ValueError, TypeError):
            return "<p>Score inválido. Por favor, insira um número.</p><a href='/'>Voltar</a>"
        
        # Obtém os novos campos: curso e disciplina
        curso = request.form.get('course')
        disciplina = request.form.get('discipline')
        
        # Agente Avaliador: Avalia o desempenho do aluno
        codigo, classificacao, feedback = avaliador.evaluate(score)
        
        # Agente Recomendador: Gera recomendação e frequência com base na classificação
        recomendacao, frequencia = recomendador.recommend(codigo, classificacao)
        
        # Agente de Monitoramento: Verifica o progresso e sugere ajustes
        ajuste = monitoramento.monitorar(nome, score)
        
        # Armazenar os dados da avaliação no banco de dados
        conn = sqlite3.connect('alunos.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO desempenho (nome, score, classificacao, codigo, curso, disciplina)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, score, classificacao, codigo, curso, disciplina))
        conn.commit()
        conn.close()
        
        return render_template_string(template_resultado,
                                      nome=nome,
                                      score=score,
                                      classificacao=classificacao,
                                      feedback=feedback,
                                      curso=curso,
                                      disciplina=disciplina,
                                      recomendacao=recomendacao,
                                      frequencia=frequencia,
                                      ajuste=ajuste)
    return render_template_string(template_form)

# ==============================================================================
# Execução do Servidor Flask
# ==============================================================================
if __name__ == '__main__':
    app.run(debug=True)
