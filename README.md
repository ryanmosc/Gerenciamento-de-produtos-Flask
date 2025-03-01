# CRUD de Produtos com Flask e MySQL

Este projeto é um CRUD de produtos implementado utilizando **Flask**, **MySQL** e **Flask-Login**. Ele permite realizar operações de criação, leitura, atualização e exclusão (CRUD) de produtos em um banco de dados MySQL, além de um sistema simples de login e registro de usuários.

## Funcionalidades

- **Login de usuários**: Autenticação de usuários via nome de usuário e senha, utilizando o Flask-Login.
- **Cadastro de usuários**: Os usuários podem se cadastrar fornecendo um nome, e-mail e senha (que será armazenada de forma segura usando bcrypt).
- **Gestão de produtos**: O administrador pode adicionar, listar, atualizar e remover produtos.
- **Proteção por login**: As páginas de gerenciamento de produtos (adicionar, listar, atualizar, remover) só podem ser acessadas por usuários autenticados.
- **Logout**: Permite que o usuário faça logout da aplicação.

## Tecnologias Utilizadas

- **Flask**: Framework web para construção do backend.
- **MySQL**: Banco de dados relacional para armazenamento de usuários e produtos.
- **bcrypt**: Biblioteca para hash de senhas.
- **Flask-Login**: Extensão para gerenciamento de sessões de usuário.
- **HTML/CSS**: Para a criação da interface do usuário.

## Como Executar

### Pré-requisitos

- Python 3.x
- MySQL instalado e configurado

### Passos para rodar o projeto

1. **Clonar o repositório:**

   ```bash
   git clone https://github.com/ryanmosc/Gerenciamento-de-produtos-Flask.git
- **Ryan Moscardini**,ryanoliveiramosc.com.098@gmail.com.
