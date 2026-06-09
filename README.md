# SIGMA

Sistema de manutencao em Flask.

## Requisitos

- Python 3.14 ou superior
- Git

## Configuracao local

1. Crie o ambiente virtual dentro da pasta do projeto:

	```powershell
	python -m venv .venv
	```

2. Ative o ambiente virtual:

	```powershell
	.\.venv\Scripts\Activate.ps1
	```

3. Instale as dependencias:

	```powershell
	pip install -r requirements.txt
	```

4. Rode os testes:

	```powershell
	pytest
	```

5. Rode a aplicacao:

	```powershell
	python app.py
	```

6. Se precisar de variaveis locais, copie o exemplo:

	```powershell
	Copy-Item .env.example .env
	```

## Rodar em outro PC ou na rede

Para abrir o projeto em outro computador, basta levar o codigo pelo GitHub, recriar o ambiente com `python -m venv .venv`, instalar as dependencias com `pip install -r requirements.txt` e copiar o `.env.example` para `.env`.

Para expor a aplicacao na rede local, defina `HOST=0.0.0.0` no `.env` e execute `python app.py`. O acesso deve ser feito pelo IP da maquina que esta rodando o sistema, por exemplo `http://192.168.0.10:5000`.

Se houver firewall no Windows ou na rede, a porta `5000` precisa estar liberada para acesso entre os computadores.

## Estrutura

- `app.py`: ponto de entrada da aplicacao
- `sigma_app/`: pacote principal com factory e rotas
- `templates/`: paginas HTML
- `static/`: arquivos CSS e futuros assets
- `tests/`: testes automatizados do projeto