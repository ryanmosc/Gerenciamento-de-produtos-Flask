# README - Sistema de Vendas com Flask

Este é um sistema de vendas simples desenvolvido com **Flask** e **MySQL**. O objetivo do sistema é gerenciar informações sobre produtos vendidos, com funcionalidades como cadastro de usuário, login, visualização de produtos, criação, atualização, exclusão e relatórios detalhados das vendas.

## Funcionalidades

- **Cadastro de Usuários**: Permite o registro de novos usuários com verificação de e-mail e senha.
- **Login de Usuários**: Possibilita a autenticação de usuários com senha criptografada.
- **Gestão de Produtos**:
  - **Criação de Produtos**: Permite adicionar novos produtos à base de dados.
  - **Listagem de Produtos**: Exibe os produtos cadastrados no banco de dados.
  - **Atualização de Produtos**: Permite editar as informações de um produto.
  - **Exclusão de Produtos**: Permite remover produtos existentes.
- **Relatórios**:
  - Exibe relatórios detalhados com informações sobre os produtos vendidos, como média de preço, total de vendas e os produtos mais e menos vendidos.
  - Possibilidade de exportar relatórios em formato CSV.
- **Exportação de Relatórios**: Gera um arquivo CSV com os dados das vendas para exportação.

## Tecnologias Utilizadas

- **Flask**: Framework web para Python.
- **MySQL**: Banco de dados relacional para armazenar informações de usuários e produtos.
- **Flask-Login**: Extensão para gerenciar sessões de login de usuários.
- **bcrypt**: Biblioteca para criptografia de senhas.
- **Pandas**: Biblioteca para manipulação de dados, utilizada na geração de relatórios.
- **HTML/CSS**: Linguagens para criação da interface do usuário.

## Pré-requisitos

- Python 3.6 ou superior.
- MySQL 5.7 ou superior.

## Instalação

### Passo 1: Clone o repositório

```bash
git clone https://github.com/seu-usuario/sistema-de-vendas.git
cd sistema-de-vendas
