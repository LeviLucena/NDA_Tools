<p align="center"> <a href="https://www.python.org/"> <img src="https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python Badge" /> </a> <a href="https://flask.palletsprojects.com/en/2.3.x/"> <img src="https://img.shields.io/badge/-Flask-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask Badge" /> </a> <a href="https://openai.com/"> <img src="https://img.shields.io/badge/-OpenAI-000000?style=flat-square&logo=openai&logoColor=white" alt="OpenAI Badge" /> </a> <a href="https://getbootstrap.com/"> <img src="https://img.shields.io/badge/-Bootstrap-563D7C?style=flat-square&logo=bootstrap&logoColor=white" alt="Bootstrap Badge" /> </a> <a href="https://python-docx.readthedocs.io/en/latest/"> <img src="https://img.shields.io/badge/-python--docx-3776AB?style=flat-square&logo=python&logoColor=white" alt="python-docx Badge" /> </a> </p>

# NDA Comparison Tools

## Descrição

O **NDA Comparison Tools** é uma aplicação web construída em Flask que compara dois arquivos de Contratos de Não Divulgações (NDAs) e gera um novo documento com as diferenças realçadas. Usando a API da OpenAI, a aplicação analisa as discrepâncias entre um NDA padrão e o NDA de um cliente, realçando modificações em amarelo e listando as inconsistências.

![image](https://github.com/user-attachments/assets/f953c2f6-65f6-4045-b610-a4fd41260264)

## Funcionalidades

- Upload de dois arquivos DOCX de NDAs (padrão e cliente).
- Comparação dos documentos usando a API da OpenAI.
- Geração de um novo documento DOCX com as modificações destacadas.
- Realce em amarelo para palavras que foram alteradas ou adicionadas no NDA do cliente.
- Possibilidade de download do NDA ajustado.

## Tecnologias e Bibliotecas Utilizadas

- **Python 3.8+**
- **Flask**: Framework web para o backend.
- **OpenAI API**: Para realizar a análise comparativa dos NDAs.
- **docx (python-docx)**: Para manipulação e criação de arquivos DOCX.
- **Werkzeug**: Para upload seguro de arquivos.
- **WTForms**: Para validação e gerenciamento de formulários.
- **HTML, CSS (Bootstrap)**: Para interface do usuário.

## Pré-requisitos

Antes de iniciar, é necessário ter instalado:

- **Python 3.8+**
- Pip para instalação de dependências.

## Instalação

1. Clone o repositório:

```
git clone https://github.com/seu-usuario/NDA-Comparison-Tools.git
cd NDA-Comparison-Tools
```

2. Crie e ative um ambiente virtual:
```
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```
pip install -r requirements.txt
```
4. Crie um diretório uploads no diretório raiz do projeto:
```
mkdir uploads
```
5. Configure sua chave da API OpenAI no arquivo `app.py`:
Como Usar
1. Inicie a aplicação:
```
flask run
```
2. Acesse a aplicação no navegador através de `http://127.0.0.1:5000/`.

3. Faça o upload dos dois arquivos DOCX de NDAs `(um NDA padrão e um NDA do cliente`).

4. O aplicativo irá comparar os documentos e gerar um novo NDA ajustado com as modificações realçadas, pronto para download.

## Estrutura do Projeto
```
.NDA Tools
├── app.py                # Arquivo principal do Flask
├── templates/
│   └── index6.html       # Template HTML para a interface de upload
├── uploads/              # Diretório para armazenar os arquivos enviados
├── static/
│   └── images/
│       └── logo.png      # Logotipo a ser exibido no cabeçalho do documento
├── requirements.txt      # Lista de dependências do projeto
└── README.md             # Este arquivo

```

## Dependências
```
pip install -r requirements.txt
```

## Licença
Este projeto está licenciado sob os termos da licença MIT. Veja o arquivo LICENSE para mais detalhes.
