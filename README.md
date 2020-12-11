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

### Fazer análises e verificar correlações

Separamos a análise em três partes para facilitar a divisão de trabalho. Ficando uma parte para cada integrante:

- [Parte 1](analise_pt1.ipynb) - Djenifer
- [Parte 2](analise_pt2.ipynb) - Carlos
- [Parte 3](analise_pt3.ipynb) - Jaqueline (que devido a sua saída passou para o Carlos)

Alguns aspectos que nos chamaram a atenção foram:
- Basicamente 80% das pessoas que realizaram o ENEM não moram em capitais (pt2)
- Mais de 50% de quem faz a prova tem entre 16 e 18 anos (pt2)
- Aproximadamente 60% dos participantes é do sexo feminino (pt2)
- Mais de 50% dos participantes tem renda mensal familiar de até R$ 1497,00 (pt1)
- 80% das pais dos candidatos possuem no máximo o ensino médio completo (pt3)
- Quase todos os participantes tem um celular, mas 40% deles não tem um computador e 20% não tem acesso a internet (pt3)

As correlações estão no mesmo arquivo que as análises, onde verificamos as tendências as variáveis tem nas notas.

### Machine Learning

Pra ter certeza das correlações, um heatmap foi feito e a partir dele foi possível verificar que:
- As notas possuem alta correlação entre si
- As demais colunas tem baixa correlação, sendo a renda a maior delas com 0.4 de correlação

Para tentar fazer a predição, testamos 4 modelos de predição: DummyRegressor, LinearRegression, DecisionTreeRegressor e SVM.
O DummyRegressor teve um péssimo desempenho dado que sua implementação usa estratégias simples.
Já o LinearRegression e DecisionTreeRegressor tiveram resultados parecidos, no entanto o DecisionTreeRegressor aparenta ser mais lento. E por fim, tentamos o SVM, porém seu tempo de execução é altíssimo para o nosso dataset. Não conseguimos estimar o tempo de execução do SVM pois ele passou de 30 minutos e desistimos de terminar a execução desse modelo.


