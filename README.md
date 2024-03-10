# Implementační dokumentace k 1. úloze do IPP 2023/2024 

Jméno a příjmení: Václav Zapletal  
Login: xzaple40

---

## `parse.py` 
### Spuštění

Zobrazení nápovědy
- `python parse.py --help`

Načtení vstupu ze standartního vstupu a spuštění skriptu, například:
- `cat test.IPPcode24 | python3 parse.py`

### Knihovny
- `argparse`
- `re`

### Hlavní funkcionalita

Na začátku programu probíha kontrola hlavičky `.IPPcode24`, pomocí funkce `header_check()`, která odstraní komentáře, poté vytiskne XML hlavičku a případně ukončí program s chybovou hodnotou 21.
Nyní se načítají řádky ze standartního vstupu, přeskakují se komentáře a mezery na samostatných řádcích a odstraňují se komentáře za instrukcemi. Pomocí  
- `if (line.startswith('#')) or (not line.strip()) : continue`
- `line = re.sub(r'#.*', '', line)`  
  
Zbylé řádky jsou dále převedeny na samostatné řetězce pomocí `split()`. Na zpracovávání instrukcí je využita funkce `match`, případy jsou rozdělené na několik částí pro rozlišení počtu potřebných argumentů a jejich druhů. Podle těchto kritérií se volají různé funkce. 
- `args_num(acc_num,exp_num)` - kontrola počtu argumentů.
- `print_arg(arg, typeORint: str)` - Kontrola pomocí regexů, nahrazení speciální znaků a tisk XML
- `constantORvar(arg)` - Rozhodnotí zda se jedná o konstantu nebo proměnnou
- `var_check(arg)` `label_check(arg)` `constant_check(arg)` `type_check(arg)` Pro kontrolu spravných typů, hodnot ...
- `sys.exit(EXIT_CODE)` - Pro ukončení programu se správnou hodnotou

