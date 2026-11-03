# Ficha: 1 Student anxiety dataset

- Bloque: Bloque 1
- Ruta original: `DataSet.zip/Bloque 1/1 Student anxiety dataset/anxiety.csv`
- Tamaño: 4.26 MB
- Filas × columnas: 13,464 × 55
- Filas duplicadas exactas: 0

## Columnas
| Columna | Tipo | Nulos | Únicos |
|---|---|---|---|
| S. No. | int64 | 0 | 13464 |
| Timestamp | float64 | 0 | 11734 |
| GAD1 | int64 | 0 | 4 |
| GAD2 | int64 | 0 | 4 |
| GAD3 | int64 | 0 | 4 |
| GAD4 | int64 | 0 | 4 |
| GAD5 | int64 | 0 | 4 |
| GAD6 | int64 | 0 | 4 |
| GAD7 | int64 | 0 | 4 |
| GADE | str | 649 | 4 |
| SWL1 | int64 | 0 | 7 |
| SWL2 | int64 | 0 | 7 |
| SWL3 | int64 | 0 | 7 |
| SWL4 | int64 | 0 | 7 |
| SWL5 | int64 | 0 | 7 |
| Game | str | 0 | 11 |
| Platform | str | 0 | 3 |
| Hours | float64 | 30 | 84 |
| earnings | str | 0 | 314 |
| whyplay | str | 0 | 407 |
| League | str | 1852 | 1454 |
| highestleague | float64 | 13464 | 0 |
| streams | float64 | 100 | 65 |
| SPIN1 | float64 | 124 | 5 |
| SPIN2 | float64 | 154 | 5 |
| SPIN3 | float64 | 140 | 5 |
| SPIN4 | float64 | 159 | 5 |
| SPIN5 | float64 | 166 | 5 |
| SPIN6 | float64 | 156 | 5 |
| SPIN7 | float64 | 138 | 5 |
| SPIN8 | float64 | 144 | 5 |
| SPIN9 | float64 | 158 | 5 |
| SPIN10 | float64 | 160 | 5 |
| SPIN11 | float64 | 187 | 5 |
| SPIN12 | float64 | 168 | 5 |
| SPIN13 | float64 | 187 | 5 |
| SPIN14 | float64 | 156 | 5 |
| SPIN15 | float64 | 147 | 5 |
| SPIN16 | float64 | 147 | 5 |
| SPIN17 | float64 | 175 | 5 |
| Narcissism | float64 | 23 | 5 |
| Gender | str | 0 | 3 |
| Age | int64 | 0 | 30 |
| Work | str | 38 | 4 |
| Degree | str | 1577 | 4 |
| Birthplace | str | 0 | 126 |
| Residence | str | 0 | 109 |
| Reference | str | 15 | 4 |
| Playstyle | str | 0 | 298 |
| accept | str | 414 | 1 |
| GAD_T | int64 | 0 | 22 |
| SWL_T | int64 | 0 | 31 |
| SPIN_T | float64 | 650 | 69 |
| Residence_ISO3 | str | 110 | 107 |
| Birthplace_ISO3 | str | 121 | 124 |

## Estadísticos numéricos (primeras 40 columnas)
|               |   count |      mean |      std |   min |      25% |     50% |     75% |     max |
|:--------------|--------:|----------:|---------:|------:|---------:|--------:|--------:|--------:|
| S. No.        |   13464 |  7096.84  | 4114.48  |     1 |  3532.75 |  7087.5 | 10654.2 | 14250   |
| Timestamp     |   13464 | 42054.8   |    0.273 | 42052 | 42054.7  | 42054.8 | 42054.9 | 42058.4 |
| GAD1          |   13464 |     0.861 |    0.927 |     0 |     0    |     1   |     1   |     3   |
| GAD2          |   13464 |     0.673 |    0.916 |     0 |     0    |     0   |     1   |     3   |
| GAD3          |   13464 |     0.966 |    0.983 |     0 |     0    |     1   |     2   |     3   |
| GAD4          |   13464 |     0.724 |    0.922 |     0 |     0    |     0   |     1   |     3   |
| GAD5          |   13464 |     0.488 |    0.837 |     0 |     0    |     0   |     1   |     3   |
| GAD6          |   13464 |     0.911 |    0.931 |     0 |     0    |     1   |     1   |     3   |
| GAD7          |   13464 |     0.589 |    0.894 |     0 |     0    |     0   |     1   |     3   |
| SWL1          |   13464 |     3.72  |    1.736 |     1 |     2    |     4   |     5   |     7   |
| SWL2          |   13464 |     4.602 |    1.696 |     1 |     3    |     5   |     6   |     7   |
| SWL3          |   13464 |     4.345 |    1.809 |     1 |     3    |     5   |     6   |     7   |
| SWL4          |   13464 |     3.762 |    1.818 |     1 |     2    |     4   |     5   |     7   |
| SWL5          |   13464 |     3.359 |    1.916 |     1 |     2    |     3   |     5   |     7   |
| Hours         |   13434 |    22.247 |   70.285 |     0 |    12    |    20   |    28   |  8000   |
| highestleague |       0 |   nan     |  nan     |   nan |   nan    |   nan   |   nan   |   nan   |
| streams       |   13364 |    11.234 |   78.549 |     0 |     4    |     8   |    15   |  9001   |
| SPIN1         |   13340 |     0.857 |    0.907 |     0 |     0    |     1   |     1   |     4   |
| SPIN2         |   13310 |     1.211 |    1.144 |     0 |     0    |     1   |     2   |     4   |
| SPIN3         |   13324 |     1.095 |    1.165 |     0 |     0    |     1   |     2   |     4   |
| SPIN4         |   13305 |     1.683 |    1.23  |     0 |     1    |     2   |     3   |     4   |
| SPIN5         |   13298 |     1.249 |    1.222 |     0 |     0    |     1   |     2   |     4   |
| SPIN6         |   13308 |     1.348 |    1.279 |     0 |     0    |     1   |     2   |     4   |
| SPIN7         |   13326 |     1.051 |    1.221 |     0 |     0    |     1   |     2   |     4   |
| SPIN8         |   13320 |     1.405 |    1.373 |     0 |     0    |     1   |     2   |     4   |
| SPIN9         |   13306 |     1.567 |    1.384 |     0 |     0    |     1   |     3   |     4   |
| SPIN10        |   13304 |     0.918 |    1.126 |     0 |     0    |     1   |     1   |     4   |
| SPIN11        |   13277 |     1.827 |    1.488 |     0 |     0    |     2   |     3   |     4   |
| SPIN12        |   13296 |     0.892 |    1.158 |     0 |     0    |     0   |     1   |     4   |
| SPIN13        |   13277 |     0.539 |    0.944 |     0 |     0    |     0   |     1   |     4   |
| SPIN14        |   13308 |     1.252 |    1.207 |     0 |     0    |     1   |     2   |     4   |
| SPIN15        |   13317 |     1.411 |    1.35  |     0 |     0    |     1   |     2   |     4   |
| SPIN16        |   13317 |     0.621 |    0.962 |     0 |     0    |     0   |     1   |     4   |
| SPIN17        |   13289 |     0.936 |    1.18  |     0 |     0    |     0   |     2   |     4   |
| Narcissism    |   13441 |     2.028 |    1.062 |     1 |     1    |     2   |     3   |     5   |
| Age           |   13464 |    20.93  |    3.301 |    18 |    18    |    20   |    22   |    63   |
| GAD_T         |   13464 |     5.212 |    4.713 |     0 |     2    |     4   |     8   |    21   |
| SWL_T         |   13464 |    19.789 |    7.229 |     5 |    14    |    20   |    26   |    35   |
| SPIN_T        |   12814 |    19.849 |   13.467 |     0 |     9    |    17   |    28   |    68   |

## Muestra (10 primeras filas, máx. 25 columnas)
|   S. No. |   Timestamp |   GAD1 |   GAD2 |   GAD3 |   GAD4 |   GAD5 |   GAD6 |   GAD7 | GADE                 |   SWL1 |   SWL2 |   SWL3 |   SWL4 |   SWL5 | Game              | Platform                |   Hours | earnings       | whyplay    | League   |   highestleague |   streams |   SPIN1 |   SPIN2 |
|---------:|------------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|:---------------------|-------:|-------:|-------:|-------:|-------:|:------------------|:------------------------|--------:|:---------------|:-----------|:---------|----------------:|----------:|--------:|--------:|
|        1 |     42052   |      0 |      0 |      0 |      0 |      1 |      0 |      0 | Not difficult at all |      3 |      5 |      5 |      5 |      5 | Skyrim            | Console (PS, Xbox, ...) |      15 | I play for fun | having fun | nan      |             nan |         0 |       1 |       0 |
|        2 |     42052   |      1 |      2 |      2 |      2 |      0 |      1 |      0 | Somewhat difficult   |      3 |      5 |      2 |      5 |      1 | Other             | PC                      |       8 | I play for fun | having fun | nan      |             nan |         2 |       2 |       1 |
|        3 |     42052   |      0 |      2 |      2 |      0 |      0 |      3 |      1 | Not difficult at all |      2 |      6 |      5 |      2 |      2 | Other             | PC                      |       0 | I play for fun | having fun | nan      |             nan |         0 |       1 |       0 |
|        4 |     42052.1 |      0 |      0 |      0 |      0 |      0 |      0 |      0 | Not difficult at all |      2 |      5 |      5 |      3 |      2 | Other             | PC                      |      20 | I play for fun | improving  | nan      |             nan |         5 |       2 |       0 |
|        5 |     42052.1 |      2 |      1 |      2 |      2 |      2 |      3 |      2 | Very difficult       |      2 |      2 |      4 |      5 |      1 | Other             | Console (PS, Xbox, ...) |      20 | I play for fun | having fun | nan      |             nan |         1 |       2 |       0 |
|        6 |     42052.1 |      0 |      0 |      0 |      0 |      0 |      1 |      0 | Not difficult at all |      3 |      5 |      3 |      3 |      3 | Other             | Console (PS, Xbox, ...) |       4 | I play for fun | relaxing   | -        |             nan |         0 |       1 |       1 |
|        7 |     42052.1 |      0 |      0 |      0 |      0 |      0 |      0 |      0 | Not difficult at all |      3 |      4 |      4 |      3 |      2 | Other             | PC                      |      30 | I play for fun | relaxing   | nan      |             nan |         8 |       1 |       2 |
|        8 |     42052.2 |      0 |      0 |      0 |      0 |      0 |      0 |      0 | nan                  |      3 |      6 |      4 |      3 |      7 | Other             | Console (PS, Xbox, ...) |      25 | I play for fun | having fun | nan      |             nan |         0 |       0 |       0 |
|        9 |     42052.2 |      2 |      3 |      2 |      2 |      0 |      1 |      2 | Very difficult       |      2 |      3 |      3 |      3 |      1 | Other             | Console (PS, Xbox, ...) |       2 | I play for fun | winning    | nan      |             nan |         0 |       1 |       1 |
|       10 |     42052.2 |      2 |      1 |      2 |      2 |      2 |      1 |      0 | Somewhat difficult   |      3 |      3 |      3 |      2 |      2 | World of Warcraft | PC                      |      25 | I play for fun | improving  | -        |             nan |         0 |       1 |       1 |

---
<!-- relacionado -->
**Relacionado:** [Índice de datasets](../00_INDICE.md)
