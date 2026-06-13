# iso3166-3-flags

This folder contains flag icons for **former countries and territories** that have been withdrawn from the ISO 3166-1 standard and assigned an **ISO 3166-3** alpha-4 code. These are nations, territories, and political entities that no longer exist in their original form — dissolved, renamed, merged, or absorbed into successor states — but whose flags remain historically and geographically significant.

---

## What is ISO 3166-3?

[ISO 3166-3](https://www.iso.org/standard/63547.html) is the third part of the ISO 3166 standard, maintained by the ISO 3166 Maintenance Agency. It defines **four-letter alpha-4 codes** for countries and territories that were previously assigned an alpha-2 code in ISO 3166-1 but have since been deleted from that list.

The alpha-4 code is constructed from two parts:

- **First two letters** — the former ISO 3166-1 alpha-2 code of the deleted country
- **Last two letters** — a code indicating the reason for deletion:
  - The alpha-2 code of the successor country (e.g. `DYBJ` → Dahomey `DY` became Benin `BJ`)
  - `HH` — the entry was deleted with no direct single successor (dissolved, split, or merged into multiple states)

---

## Flags in this folder

There are currently **24** ISO 3166-3 flags in this folder. All flags are in **SVG** format and named using the ISO 3166-3 alpha-4 code (uppercase), e.g. `SUHH.svg`.

| Alpha-4 | Former Country / Territory | Successor(s) | Period |
|---|---|---|---|
| `AIDJ` | French Territory of the Afars and Issas | Djibouti (`DJ`) | 1967–1977 |
| `ANHH` | Netherlands Antilles | Curaçao (`CW`), Sint Maarten (`SX`), dissolved | 1954–2010 |
| `BQAQ` | British Antarctic Territory | British Antarctic Territory (subsumed into `AQ`) | 1962–1979 |
| `BUMM` | Burma | Myanmar (`MM`) | 1948–1989 |
| `BYAA` | Byelorussian SSR | Belarus (`BY`) | 1974–1992 |
| `CSHH` | Czechoslovakia | Czech Republic (`CZ`), Slovakia (`SK`) | 1918–1993 |
| `CSXX` | Serbia and Montenegro | Serbia (`RS`), Montenegro (`ME`) | 1992–2006 |
| `CTKI` | Canton and Enderbury Islands | Kiribati (`KI`) | 1939–1979 |
| `DDDE` | German Democratic Republic (East Germany) | Germany (`DE`) | 1949–1990 |
| `DYBJ` | Dahomey | Benin (`BJ`) | 1958–1975 |
| `FQHH` | French Southern and Antarctic Territories | French Southern Territories (`TF`) | 1955–1979 |
| `FXFR` | Metropolitan France | France (`FR`) | 1993–1997 |
| `HVBF` | Upper Volta | Burkina Faso (`BF`) | 1958–1984 |
| `NHVU` | New Hebrides | Vanuatu (`VU`) | 1906–1980 |
| `PCHH` | Pacific Islands Trust Territory | Micronesia (`FM`), Marshall Islands (`MH`), Northern Mariana Islands (`MP`), Palau (`PW`) | 1947–1986 |
| `PZPA` | Panama Canal Zone | Panama (`PA`) | 1903–1979 |
| `RHZW` | Rhodesia | Zimbabwe (`ZW`) | 1965–1980 |
| `SKIN` | Sikkim | India (`IN`) | 1890–1975 |
| `SUHH` | Soviet Union (USSR) | Russia (`RU`) and 14 successor republics | 1922–1991 |
| `TPTL` | Portuguese Timor / East Timor | Timor-Leste (`TL`) | 1702–2002 |
| `VDVN` | Democratic Republic of Vietnam (North Vietnam) | Vietnam (`VN`) | 1945–1976 |
| `YDYE` | South Yemen (People's Democratic Republic of Yemen) | Yemen (`YE`) | 1967–1990 |
| `YUCS` | Yugoslavia | Bosnia & Herzegovina (`BA`), Croatia (`HR`), North Macedonia (`MK`), Slovenia (`SI`), Serbia (`RS`), Montenegro (`ME`) | 1918–1992 |
| `ZRCD` | Zaire | Democratic Republic of the Congo (`CD`) | 1971–1997 |

---

## Relationship to other flag directories

| Directory | Standard | Scope |
|---|---|---|
| [`iso3166-1-flags/`](../iso3166-1-flags/) | ISO 3166-1 | Current sovereign countries and territories (250 entries) |
| [`iso3166-2-flags/`](../iso3166-2-flags/) | ISO 3166-2 | Current country subdivisions (regions, states, provinces) |
| `iso3166-3-flags/` | ISO 3166-3 | Former countries and territories, now withdrawn from ISO 3166-1 |

---

## Usage

Flags follow the same SVG format as the rest of this repository. Reference them by their alpha-4 code filename:

```html
<img src="iso3166-3-flags/SUHH.svg" alt="Flag of the Soviet Union" width="40" />
<img src="iso3166-3-flags/YUCS.svg" alt="Flag of Yugoslavia" width="40" />
<img src="iso3166-3-flags/DDDE.svg" alt="Flag of East Germany" width="40" />
```

---

## Notes

- Some of the flags in this folder are disputed, historical reconstructions, or have multiple variants. Where multiple designs existed during a country's lifetime, the most widely recognised or officially documented version has been used.
- The `FXFR` (Metropolitan France) entry is unusual — it represented the European territory of France separately from its overseas departments, and was deleted in 1997 when this distinction was removed from the standard.
- Coverage of ISO 3166-3 is ongoing. Not every deleted entry from the standard necessarily has an associated flag that is well-documented or freely licensed.

---

**Standard**: [ISO 3166-3:2013](https://www.iso.org/standard/63547.html)  
**Maintained by**: [ISO 3166 Maintenance Agency](https://www.iso.org/iso-3166-country-codes.html)
