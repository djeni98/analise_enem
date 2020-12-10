# Análise do ENEM
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)

Implementação da [proposta de projeto](proposta.md) do TechLabs.

## Objetivos

- Análise exploratória completa dos dados do ENEM divulgados publicamente para que possamos entender o perfil dos candidatos.
- Modelo de predição das notas de matemática e redação.

## Jornada

**OBS**: Para conseguir executar os _notebooks_ e os _scripts_ é preciso baixar o zip dos dados de 2019 e colocar os arquivos que estão nos diretórios `DADOS` e `DICIONÁRIO` do zip no diretório `dados` deste repositório.
Esses dados não estão atualmente no repositório dado que o arquivo `MICRODADOS_ENEM_2019.csv` tem 3G de tamanho.

### Obter e entender os dados do ENEM

Os dados foram obtidos a partir do link http://inep.gov.br/web/guest/microdados e optamos pelos dados de 2019.
Os arquivos relevantes `Dicionário_Microdados_Enem_2019.xlsx` e `MICRODADOS_ENEM_2019.csv` foram movidos para o diretório `dados` e os usamos a partir de lá.

Para conseguir trabalhar mais facilmente as colunas, criamos um [_notebook_](get_dicionario.ipynb) para obter as informações do arquivo .xlsx e convertê-las em dois arquivos:
- [dados/dicionario.json](dados/dicionario.json): contém a coluna e sua descrição
- [dados/categorias.json](dados/categorias.json): contém a colunas e suas categorias, se a coluna for categórica

### Limpar o dataset

Como o dataset tem mais de 5 milhões de linhas, não é possível abrir o arquivo num editor de texto nem no jupyter notebook.
Então fizemos alguns passos para conseguir diminuir o tamanho e uso de memória do dataset.
O _notebook_ de [limpeza do csv](limpar_csv.ipynb) mostra a nossa análise inicial do dataset e o que poderíamos fazer para diminuir o uso de memória.

Para gerar o arquivo otimizado, o [_script_](script_limpar_csv.ipynb) criado a partir do _notebook_ de limpeza roda as alterações no dataset em partes.
Assim, a cada X linhas, as alterações são aplicadas e ao final da execução essas partes alteradas são juntadas para obter o dataset inteiro otimizado.

Como arquivos de texto não podem manter a otimização de alguns tipos, optamos por usar o formato pickle do python.
Desta maneira, o objeto otimizado pode ser armazenado e lido posteriormente sem aumento no consumo da memória.
