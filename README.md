# Gestão e Comercialização de Vinhos

## Sobre o Projeto

Este projeto é uma aplicação moderna desenvolvida para facilitar a gestão e comercialização de vinhos. A aplicação é direcionada tanto para administradores, que necessitam de uma interface robusta para gerir o stock e analisar vendas, como para utilizadores finais, que podem navegar por um catálogo de vinhos, adicionar itens ao carrinho de compras e finalizar compras de forma simples e intuitiva.

O sistema foi desenvolvido com foco na experiência do utilizador, apresentando uma interface gráfica moderna, eficiente e fácil de usar, utilizando a biblioteca `customtkinter`.

---

## Funcionalidades

### Funcionalidades para Administradores
- **Gestão de Stock**: Possibilidade de criar, editar e eliminar registos de vinhos com informações detalhadas como marca, preço, região, ano e descrição.
- **Análise de Vendas**: Exibição de vendas mensais detalhadas numa tabela, com opção de exportar os dados para CSV.

### Funcionalidades para Utilizadores
- **Registo e Login**: Sistema seguro de autenticação e gestão de contas de utilizadores.
- **Catálogo de Vinhos**: Visualização de todos os vinhos disponíveis com informações detalhadas.
- **Carrinho de Compras**: Adicionar produtos ao carrinho e processar compras de forma simples.

---

## Como Executar o Projeto

### Pré-requisitos
Para executar o projeto, é necessário garantir que o Python está instalado no seu sistema. Recomendamos a versão **3.10 ou superior**. Além disso, é essencial que a biblioteca `customtkinter` esteja instalada no ambiente virtual do projeto.

### Instalação de Dependências
1. Certifique-se de que está no diretório raiz do projeto.
2. Ative o ambiente virtual:
   ```bash
   # Em sistemas UNIX
   source .venv/bin/activate

   # Em sistemas Windows
   .venv\Scripts\activate
   ```
3. Instale a biblioteca `customtkinter`:
   ```bash
   pip install customtkinter
   ```

### Executar o Projeto
Para iniciar a aplicação, execute o ficheiro principal:
```bash
python main.py
```

---

## Bibliotecas Utilizadas

As bibliotecas principais utilizadas neste projeto incluem:

- **`customtkinter`**: Usada para criar a interface gráfica moderna e intuitiva.
- **`sqlite3`**: Para gerir e armazenar os dados do projeto numa base de dados local.
- **`csv`**: Para exportar os dados de vendas mensais num formato compatível com outras aplicações.
- **`datetime`**: Para lidar com datas relacionadas a vendas e outros registos.

---

## Estrutura do Projeto

```plaintext
Loja_vinhos/
├── main.py            # Ficheiro principal para execução da aplicação
├── ui/                # Interfaces gráficas da aplicação
│   ├── main_panel.py
│   ├── login_and_register.py
│   └── admin_interface.py
├── logic/             # Lógica da aplicação
│   ├── wine_management.py
│   ├── sales_management.py
│   └── user_auth.py
├── data/              # Base de dados e scripts de inicialização
│   ├── database.db
│   └── database.py
└── .venv/             # Ambiente virtual com as dependências do projeto
```

---

## Autores

Este projeto foi desenvolvido por:
- **João Moura**
- **Rodrigo Jorão**
- **Daniel Vitória**
- **Bruno Pataias**

Cada um contribuiu significativamente para o sucesso deste projeto, desempenhando papéis fundamentais no desenvolvimento, design da interface e integração de funcionalidades.

---

## Notas Finais

Agradecemos por utilizares este sistema de gestão de vinhos. Se tiveres dúvidas ou sugestões, entra em contacto com os autores. Continuamos comprometidos em melhorar esta aplicação para proporcionar a melhor experiência possível aos seus utilizadores.

