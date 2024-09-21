import os
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
import openai
import docx
from io import BytesIO
from docx.enum.text import WD_COLOR_INDEX  # Importando o WD_COLOR_INDEX corretamente
from docx.enum.text import WD_ALIGN_PARAGRAPH  # Alinhamento justificado do docx
from docx.shared import Inches  # Para definir o tamanho da imagem
from docx.shared import Pt

app = Flask(__name__)

# Configurações do diretório de upload
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

# Configure sua chave de API do OpenAI
openai.api_key = 'SUA CHAVE API OPENAI AQUI'

# Função para ler o conteúdo do arquivo DOCX
def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Função para realçar o texto no DOCX
def highlight_text(paragraph, text_to_highlight):
    for run in paragraph.runs:
        if text_to_highlight in run.text:
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW  # Realça com a cor amarela

# Função para aplicar a fonte e o tamanho
def set_font(run, font_name='Arial Nova Light', size=10):
    run.font.name = font_name
    run.font.size = Pt(size)

# Rota principal para carregar a página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar os arquivos e realizar a comparação
@app.route('/compare', methods=['POST'])
def compare_ndas():
    if 'standard_nda' not in request.files or 'user_nda' not in request.files:
        flash('Ambos os arquivos são obrigatórios para a comparação!', 'error')
        return redirect(url_for('index'))

    standard_nda_file = request.files['standard_nda']
    user_nda_file = request.files['user_nda']

    if standard_nda_file.filename == '' or user_nda_file.filename == '':
        flash('Por favor, selecione os dois arquivos para comparar.', 'error')
        return send_file(doc_io, as_attachment=True, download_name='nda_ajustado.docx', 
                     conditional=True)

    # Salvar os arquivos
    standard_nda_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(standard_nda_file.filename))
    user_nda_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_nda_file.filename))
    standard_nda_file.save(standard_nda_path)
    user_nda_file.save(user_nda_path)

    # Ler o conteúdo dos arquivos
    standard_nda_content = read_docx(standard_nda_path)
    user_nda_content = read_docx(user_nda_path)

    # Chamada para a API da OpenAI para comparar os NDAs e realçar as modificações
    messages = [
        {"role": "system", "content": "Você é um especialista em análise de NDAs."},
        {"role": "user", "content": f"Compare o seguinte NDA padrão com o NDA de um cliente e gere um novo NDA ajustado baseado no NDA padrão. Realce as palavras modificadas devido às inconformidades no NDA do cliente com a cor amarela e liste as inconsistências claramente.\n\nNDA Padrão:\n{standard_nda_content}\n\nNDA Cliente:\n{user_nda_content}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Pode ser gpt-4 ou outro modelo apropriado
        messages=messages,
        max_tokens=5000,
        temperature=0.5
    )

    # Processar a resposta da OpenAI
    result_text = response['choices'][0]['message']['content'].strip()

    # Criar o novo documento ajustado em DOCX baseado no NDA padrão
    doc = docx.Document()
    # Adicionar imagem no cabeçalho
    header = doc.sections[0].header
    header_para = header.paragraphs[0]
    run = header_para.add_run()

    # Defina o caminho para sua imagem
    image_path = os.path.abspath(os.path.join('static', 'images', 'logo.png'))

    # Adicione a imagem no cabeçalho com um tamanho ajustado (Inches define as dimensões)
    run.add_picture(image_path, width=Inches(1.5), height=Inches(0.75))
    doc.add_heading('NDA Ajustado com Inconformidades Realçadas', 0)

    # Adicionar o conteúdo do NDA ajustado e realçar as palavras modificadas
    for line in result_text.split('\n'):
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY  # Define o alinhamento para justificado
        if "**" in line:  # Supondo que as palavras modificadas sejam marcadas com ** para realce
            parts = line.split("**")
            for i, part in enumerate(parts):
                run = para.add_run(part)
                set_font(run)  # Aplica a fonte ao texto
                if i % 2 == 1:  # As palavras entre ** serão realçadas
                    highlight_text(para, part)
        else:
            run = para.add_run(line)
            set_font(run)  # Aplica a fonte ao texto

    # Salvar o documento em memória para download
    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)

    return send_file(doc_io, as_attachment=True, download_name='nda_ajustado.docx')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
