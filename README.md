# nomad-calc

Calculate days spent per territory (like Schengen), warn about maximum stay overusage. The data is provided by YAML with nomads (persons), territories, stay limit per period, entry and exit dates.

See [Example YAML](example.yaml) for the data example.
```
territories:
  Schengen:
    Ukraine: # per nationality
      maximum_stay: 90
      per_period: 180
  Türkiye:
    Ukraine:
      maximum_stay: 90
      per_period: 180

nomads:
  Eugene:
    nationality: Ukraine
  Olha:
    nationality: Ukraine

stays:
- entry_date: 2023-01-01
  exit_date: 2023-01-20
  territory: Schengen
  nomads:
    - Eugene
    - Olha
- entry_date: 2023-01-20
  exit_date: 2023-01-30
  territory: Türkiye
  nomads:
    - Eugene
- entry_date: 2023-01-21
  exit_date: 2023-04-05
  territory: Schengen
  nomads:
    - Olha
```

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
