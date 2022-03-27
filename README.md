# Roland_gamos_cs via HLTV

```python
>>> import rolland_gamos_cs as roga
>>> roga.players_played_together("coldzera", "rain")
"They not played together in 00nation"
"They not played together in complexity"
"They played together in faze (Aug 2020-Oct 2020) ['niko', 'rain', 'kjaerbye', 'coldzera', 'broky']"
"They played together in faze (May 2020-Jul 2020) ['niko', 'rain', 'coldzera', 'broky', 'bymas']"
"They played together in faze (Sep 2019-May 2020) ['olofmeister', 'niko', 'rain', 'coldzera', 'broky']"
"They not played together in mibr"
"They not played together in sk"
"They not played together in luminosity"
True
```

```python
>>> import rolland_gamos_cs as roga
>>> roga.players_played_together("coldzera", "device", display = False)
False
```

if too many request :

```python
>>> import rolland_gamos_cs as roga
>>> roga.players_played_together("pimp", "nitr0", False, time_sleep = 1.5)
# wait 1.5 second between each request
True
```
