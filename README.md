# 📚 BookTracker

## Visão Geral

O **BookTracker** é uma aplicação web que permite aos usuários organizar e acompanhar sua jornada de leitura. Com ela, é possível pesquisar livros usando a Google Books API, adicioná-los à sua biblioteca pessoal e gerenciar o status de leitura como Para Ler, Lendo ou Finalizado.

O projeto foi inicialmente desenvolvido como Projeto Final do CS50, e posteriormente evoluído para compor meu portfólio pessoal, recebendo melhorias de UI, UX e internacionalização.

---

## Funcionalidades

* Autenticação de usuários (registro, login e logout)
* Pesquisa de livros via Google Books API
* Biblioteca pessoal por usuário
* Organização dos livros por status:

  * Para Ler
  * Lendo
  * Finalizado
* Atualização do status de leitura
* Remoção de livros da biblioteca
* Suporte a dois idiomas (Inglês e Português)
* Interface moderna com Tailwind CSS

---

## Tecnologias Utilizadas

* **Python**
* **Flask**
* **SQLite**
* **Jinja2**
* **Tailwind CSS**
* **Google Books API**
* **JavaScript**

---

## 📂 Estrutura do Projeto

```
BookTracker/
│
├── app.py              # Aplicação principal Flask
├── init_db.py          # Script de inicialização do banco de dados
├── booktrack.db        # Banco de dados SQLite (local)
├── templates/          # Templates HTML (Jinja2)
├── static/             # Arquivos estáticos (CSS, imagens)
├── translations.py     # Arquivo de traduções (i18n)
├── requirements.txt    # Dependências do projeto
└── README.md
```

---

## Como Funciona

* Cada usuário possui sua própria biblioteca
* Os livros são buscados diretamente da Google Books API
* As informações são armazenadas em um banco SQLite
* O status dos livros pode ser atualizado a qualquer momento
* O idioma da interface pode ser alterado manualmente pelo usuário

---

## Autor

**Felipe Gomes** 

Projeto desenvolvido inicialmente para o **CS50** e aprimorado para portfólio pessoal.
