# nomad-calc

Calculate days spent per territory (like Schengen), warn about maximum stay overusage. The data is provided by YAML with nomads (persons), territories, stay limit per period, entry and exit dates.

See [Example YAML](example.yaml) for the data example.

Example output based on this YAML:
```
$ ./nomad_calc.py --yaml example.yaml --date 2023-04-05
On Date: 2023-04-05 (all dates are inclusive)
Eugene:
  Schengen from 2022-10-08: 20
  Türkiye from 2022-10-08: 11
Olha:
    2023-04-01: already stayed 91 days from maximum stay of 90 days
    2023-04-02: already stayed 92 days from maximum stay of 90 days
    2023-04-03: already stayed 93 days from maximum stay of 90 days
    2023-04-04: already stayed 94 days from maximum stay of 90 days
    2023-04-05: already stayed 95 days from maximum stay of 90 days
  Schengen from 2022-10-08: 95
  Türkiye from 2022-10-08: 0
```
