# Analisador Semântico para OWL2 (Manchester Syntax)

Este projeto implementa um **analisador semântico** para a linguagem [*OWL2*](https://www.w3.org/TR/owl2-overview/) no formato [*Manchester Syntax*](https://www.w3.org/TR/owl2-manchester-syntax/), utilizando *Python*. O objetivo é identificar erros semânticos de precedência de operadores, coerção e sobrecarregamento.

---

## 📖 Sobre o Projeto

O **Analisador Semântico** foi desenvolvido como parte de um estudo prático sobre a construção de compiladores e ferramentas de análise semântica. O projeto realiza análise semântica sobre um código em uma linguagem ontológica baseada em classes e propriedades. Ela identifica erros semânticos que não são capturados pela análise léxica ou sintática, como:

- Ordem incorreta de seções;
- Sobrecarga indevida de propriedades;
- Uso de operadores inválidos;
- Coerção de tipo malformada;
- Uso de "only" antes de "some";
- Classifica propriedades em Object Property ou Data Property;

---

## Ferramentas Utilizadas

1. **Python**

2. **RE:** Serve para trabalhar com expressões regulares em Python. Ela permite buscar, validar, extrair ou substituir padrões de texto complexos com muito mais poder do que simples comparações de strings.

---

## Como Usar

### Pré-requisitos 

- [Python](https://www.python.org/downloads/)
- [Biblioteca PLY (Python Lex-Yacc)](https://pypi.org/project/ply/)

### Execução Semântico

1. Clone o repositório ou baixe o arquivo ZIP:

   ```bash
   git clone https://github.com/FabricioDangellis/ProjetoCompiladores
   ```

2. Acesse a pasta do repositório:

   ```bash
   cd ProjetoCompiladores
   ```

3. Instale a biblioteca PLY:

   ```bash
   pip install ply
   ```

4. Baixe todas as alterações de todas as branches remotas para o seu repositório local:

   ```bash
   git fetch --all
   ```

5. Altere para a branch semantic_analyzer:

   ```bash
   git checkout SemanticAnalyzer 
   ```
6. Atualize a branch:

   ```bash
   git pull origin SemanticAnalyzer 
   ```

7. Mude para a pasta `src`:

   ```bash
   cd src
   ```

8. Execute o código:

   ```bash
   python semantic_analyzer.py
   ```

9. Insira o nome do arquivo de teste (deve estar na pasta `src`):

   ```bash
   erros.txt
   ```

10. Escolha a opção "Análise Semântica" do menu interativo para:

   - Análise Léxica
   - Análise Sintática
   - Análise Semântica

   OBS: Também é possivel ver as implementações dos analisadores lexico e sintático, basta escolher a opção correspondente dos mesmos.
---

## Funcionalidades

- **Verificação de Semântica de Classes OWLs:** analisa construções de classes OWL2 escritas em Manchester Syntax e detecta inconsistências semânticas comuns.

- **Classificação de Propriedades:** oidentifica automaticamente o tipo de cada propriedade como ***Data Property*** ou ***Object Property***.

- **Detecção de Sobrecarga de Propriedades:** sinaliza propriedades indevidamente usadas como Data e Object simultaneamente.

- **Verificação de Ordem dos Cabeçalhos:** valida a sequência correta das seções "Class:", "EquivalentTo:", "SubClassOf:", "DisjointClasses:" e "Individuals:".

- **Verificação de Expressões de Fechamento:** garante que only só apareça após some na mesma propriedade.

- **Detecção de Coerção de Tipo:** identifica valores com operadores relacionais (>=, <=, etc.) sem tipos de dados explícitos.

- **Detecção de Operadores Inválidos:** localiza operadores não suportados pela sintaxe como <<, ==>, ===, entre outros.

- **Relatório Semântico Ordenado:** exibe todos os erros com indicação da linha e mensagens descritivas.

---

## Regras de Análise Semântica

### 1. Ordem dos Cabeçalhos

A sequência das seções dentro de uma classe deve seguir a ordem canônica:

```
Class:
EquivalentTo:
SubClassOf:
DisjointClasses:
Individuals:
```
A seção Individuals: não pode aparecer antes de DisjointClasses:.

### 2. Primeira Seção Após Class

Após a linha Class: NomeDaClasse, a primeira seção obrigatória deve ser EquivalentTo: ou SubClassOf:.

### 3. Ordem de Quantificadores
Dentro de uma mesma propriedade, only não pode aparecer antes de some.

```
Correto:
hasTopping some CheeseTopping
hasTopping only CheeseTopping

Incorreto:
hasTopping only CheeseTopping
hasTopping some CheeseTopping  # ❌ Erro
```

### 4. Coerção de Tipos com Operadores

Expressões como [>= 18], [< 100], etc. devem vir acompanhadas de tipos de dados explícitos, como xsd:int.

```
Correto:
hasAge some xsd:int [>= 18]

Incorreto:
hasAge some [>= 18]  # ❌ Erro
```

### 5. Operadores Inválidos

Os seguintes operadores não são válidos e geram erro:

   - <<, >>, ><, <>, ==>, ===


### 6. Sobrecarga de Propriedades

Uma propriedade não pode ser usada como Data Property e Object Property ao mesmo tempo.

```
Correto:
hasPrice some xsd:decimal
hasIngredient some Cheese

Incorreto:
hasValue some xsd:int
hasValue some Ingredient  # ❌ Erro de sobrecarga
```
---

## Classificação das Propiedades

Durante a análise, cada propriedade é classificada automaticamente:

```
==== Classificação das Propriedades ====

hasAge: Data Property
hasTopping: Object Property
isBaseOf: Object Property
```

   Propriedades sobrecarregadas (usadas como data e object) não aparecem nesta lista.

---

## Exemplos

### Entrada

```
Class: TestePizza
SubClassOf:
    hasTopping only (MozzarellaTopping or TomatoTopping),
    hasTopping some CheeseTopping

Class: InvalidPizza
SubClassOf:
    hasTopping some xsd:integer [<< 400]

Class: Pessoa
EquivalentTo:
    ssn min 1 xsd:string,
    ssn some Pessoa

Class: AmericanPizza
Individuals:
    X1, X2
EquivalentTo:
    Pizza
SubClassOf:
    NamedPizza

Class: Sobrecarregada
SubClassOf:
    hasTopping some MozzarellaTopping,  
    hasTopping some xsd:string            

```

## Análise Realizadas

Exemplo de saída:

```
==== CLASSIFICAÇÃO DAS PROPRIEDADES ====
ssn: Object Property

======= ERROS SEMÂNTICOS ========
Linha 3: O "only" não pode aparecer antes de "some" na classe "TestePizza".
Linha 3: Propriedade 'hasTopping' está sobrecarregada como data property e object property.
Linha 8: Operador inválido '<<'.
Linha 12: Tipo indefinido ou inválido da propriedade 'ssn'.
Linha 16: A seção 'Individuals' não pode aparecer antes de 'DisjointClasses:'.
Linha 16: A classe "AmericanPizza" não pode iniciar com "Individuals".
Linha 23: Ordem inválida de cabeçalhos na classe "Sobrecarregada".
Linha 25: Tipo indefinido ou inválido da propriedade 'hasTopping'.
```
---
