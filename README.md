# Analisador Léxico para OWL2 (Manchester Syntax)

Este projeto implementa um **analisador léxico** para a linguagem [*OWL2*](https://www.w3.org/TR/owl2-overview/) no formato [*Manchester Syntax*](https://www.w3.org/TR/owl2-manchester-syntax/), utilizando *Python* e a biblioteca *PLY*. O objetivo é identificar e categorizar os *tokens* presentes em uma ontologia descrita neste formato, produzindo uma tabela de símbolos como saída.

---

## 📖 Sobre o Projeto

O **Analisador Léxico para OWL2 (Manchester Syntax)** foi desenvolvido como parte de um estudo prático sobre a construção de compiladores e ferramentas de análise léxica. O projeto tem como objetivo o reconhecimento e categorização dos seguintes elementos da linguagem **OWL2** no formato **Manchester Syntax**:

- Palavras reservadas;
- Identificadores de classes e propriedades;
- Nomes de indivíduos;
- Tipos de dados;
- Cardinalidades;
- Símbolos especiais.

O resultado é uma **tabela de símbolos** e **relatórios detalhados** sobre os *tokens* encontrados, permitindo uma base sólida para análise sintática ou semântica posterior.

---

## Ferramentas Utilizadas

1. [**Python**](https://www.python.org/downloads/):

2. [**PLY (Python Lex-Yacc)**](https://www.dabeaz.com/ply/):

---

## Como Usar

### Pré-requisitos 

- [Python](https://www.python.org/downloads/)
- [Biblioteca PLY (Python Lex-Yacc)](https://pypi.org/project/ply/)

### Execução Lexico

1. Clone o repositório ou baixe o arquivo ZIP:

   ```bash
   git clone https://github.com/FabricioDangellis/ProjetoCompiladores
   ```

2. Acesse a pasta do repositório:

   ```bash
   cd lexical_analyzer
   ```

3. Instale a biblioteca PLY:

   ```bash
   pip install ply
   ```

4. Mude para a pasta `src`:

   ```bash
   cd src
   ```

5. Execute o código:

   ```bash
   python lexical_analyzer.py
   ```

6. Insira o nome do arquivo de teste (deve estar na pasta `src`):

   ```bash
   input.txt
   ```

7. Escolha as opções do menu interativo para:

   - Visualizar tokens processados;
   - Exibir a tabela de símbolos;
   - Consultar a contagem de tokens.

---

## Funcionalidades

- **Reconhecimento de Tokens:** palavras reservadas, classes, propriedades, indivíduos, tipos de dados, símbolos especiais e cardinalidades da linguagem **OWL2** no formato **Manchester Syntax**.

- **Geração de Tabela de Símbolos:** organiza e exibe todos os *tokens* identificados.

- **Registro de Erros Léxicos:** detecta e lista *tokens* inválidos encontrados durante o processamento.

- **Menu Interativo:** permite a navegação e visualização de resultados

---

## Descrição dos Tokens

### 1. `KEYWORD`

*Tokens* que representam as **palavras reservadas** da linguagem:

- *some, all, value, min, max, exactly, that*
- *not, and, or, only*
- *Class, EquivalentTo, Individuals, SubClassOf, DisjointClasses* 

   - Todos sucedidos por `:` (indicam tipos na linguagem OWL)

### 2. `CLASS_ID`

*Tokens* que representam **identificadores de classes** na ontologia:

- Começam com letra maiúscula, p.ex.: *Pizza*.
- Nomes compostos concatenados e com iniciais maiúsculas, p.ex.: *VegetarianPizza*.
- Nomes compostos separados por *underline*, p.ex.: *Margherita_Pizza*.

### 3. `PROPERTY_ID` 

*Tokens* que representam **identificadores de propriedades** das classes:

- Começam com `has`, seguidos de uma string simples ou composta, p.ex.: *hasTopping*, *hasBase*.
- Começam com `is`, seguidos de qualquer coisa, e terminam com `Of`, p.ex.: *isToppingOf*, *isBaseOf*.
- Nomes de propriedades geralmente começam com letra minúscula e são seguidos por qualquer outra sequência de letras, p.ex.: *ssn*, *numberOfPizzasPurchased*.

### 4. `INDIVIDUAL_NAME`

*Tokens* que identificam os **nomes de indivíduos** (instâncias específicas de classes):

- Começam com uma letra maiúscula, seguida de qualquer combinação de letras minúsculas e terminando com um número. Exemplo: *Customer1*, *Pizza1*, *Waiter2*.

### 5. `DATATYPE`

*Tokens* que representam os **tipos de dados** nativos das linguagens OWL, RDF, RDFs ou XML Schema:

- Exemplos: *owl:real*, *rdf:langString*, *rdfs:Literal*, *xsd:string*.

### 6. `SPECIAL_SYMBOL`

*Tokens* que representam **símbolos especiais** utilizados para estruturar expressões:

- Exemplos: *`[`, `]`, `{`, `}`, `(`, `)`, `<`, `>`, `=`,`,`.*

### 7. `CARDINALITY`

*Tokens* que especificam restrições numéricas para relações ou propriedades:

- Exemplo: *hasTopping min **3***

---

## Exemplos

### Entrada

```
Class: VegetarianPizza
EquivalentTo:
    Pizza
    and (hasTopping only
    (CheeseTopping or VegetableTopping))
```

### Saída Esperada

- Tokens Processados

|**Token**            | **Valor**               | **Linha** | **Posição** |
|-----------------------|-------------------------|-----------|-------------|
| KEYWORD              | Class:                 | 1         | 0           |
| CLASS_ID             | VegetarianPizza        | 1         | 7           |
| KEYWORD              | EquivalentTo:          | 2         | 23          |
| CLASS_ID             | Pizza                  | 3         | 41          |
| KEYWORD              | and                    | 4         | 51          |
| SPECIAL_SYMBOL       | (                      | 4         | 55          |
| PROPERTY_ID          | hasTopping             | 4         | 56          |
| KEYWORD              | only                   | 4         | 67          |
| SPECIAL_SYMBOL       | (                      | 5         | 76          |
| CLASS_ID             | CheeseTopping          | 5         | 77          |
| KEYWORD              | or                     | 5         | 91          |
| CLASS_ID             | VegetableTopping       | 5         | 94          |
| SPECIAL_SYMBOL       | )                      | 5         | 110         |
| SPECIAL_SYMBOL       | )                      | 5         | 111         |

<br>

- Tabela de Símbolos

| **Token**            | **Valor**              |
|-----------------------|------------------------|
| KEYWORD              | Class:                |
| CLASS_ID             | VegetarianPizza       |
| KEYWORD              | EquivalentTo:         |
| CLASS_ID             | Pizza                 |
| KEYWORD              | and                   |
| SPECIAL_SYMBOL       | (                     |
| PROPERTY_ID          | hasTopping            |
| KEYWORD              | only                  |
| CLASS_ID             | CheeseTopping         |
| KEYWORD              | or                    |
| CLASS_ID             | VegetableTopping      |
| SPECIAL_SYMBOL       | )                     |

<br>

- Contagem de Tokens

| **Token**            | **Quantidade**        |
|-----------------------|-----------------------|
| KEYWORD              | 5                     |
| CLASS_ID             | 4                     |
| PROPERTY_ID          | 1                     |
| SPECIAL_SYMBOL       | 4                     |

### Execução Sintático

1. Mude de branch

   ```bash
   git checkout SintaticAnalyzer
   ```

2. Mude para a pasta `src`:

   ```bash
   cd src
   ```

3. Execute o código:

   ```bash
   python main.py
   ```

4. Insira o nome do arquivo de teste (deve estar na pasta `src`):

   ```bash
   input.txt
   ```
---

## Analisador Sintático

- Validação da Estrutura Gramatical com regras formais da sintaxe Manchester

- Relatórios de Erros Sintáticos, com linha e sugestão de correção

- Classificação de Classes OWL:

   - Primitiva ou Definida

   - E também: Fechada, Enumerada, Aninhada ou Coberta

- Identificação de Padrões Compostos:

   - SubClassOf, EquivalentTo, DisjointClasses

   - Operadores: some, only, and, or, min, value, comparações como [< 400]

---

## Classificações Realizadas

Durante a análise sintática, as classes encontradas são classificadas automaticamente com base em seus construtores. Exemplo de saída:

```
====== CLASSIFICAÇÃO DAS CLASSES ======

Pizza: Primitiva & Fechada
HighCaloriePizza: Definida & Aninhada
Spiciness: Definida & Enumerada
SpicyPizza: Definida & Aninhada
VegetarianPizza: Definida & Fechada & Coberta
```
---

## Detecção de Erros Sintáticos

Em caso de erro, o sistema informa:

- A linha

- O token inesperado

- Uma dica de correção

Exemplo:

```
Erro Sintático na linha 45: token inesperado 'min'. Dica: verifique se a estrutura da classe está correta.
```
---


## Exemplo de Execução
Arquivo de entrada (input.txt):

```
Class: VegetarianPizza
EquivalentTo:
    Pizza
    and (hasTopping only
    (CheeseTopping or VegetableTopping))
```

- Saída esperada:

```
VegetarianPizza: Definida & Fechada & Coberta
```