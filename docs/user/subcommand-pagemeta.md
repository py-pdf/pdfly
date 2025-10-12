# pagemeta

Give details about a PDF's single page.

## Usage

```
$ pdfly pagemeta --help
 Usage: pdfly pagemeta [OPTIONS] PDF PAGE_INDEX

 Give details about a single page.


╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    pdf             FILE     [default: None] [required]                     │
│ *    page_index      INTEGER  [default: None] [required]                     │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --output  -o      [json|text]  output format [default: text]                 │
│ --help                         Show this message and exit.                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Examples

Get the metadata of the 101st page of `document.pdf` in text format.
```
pdfly pagemeta document.pdf 100
    /home/user/.../document.pdf, page index 100       

    ┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃   Attribute ┃ Value                                               ┃
    ┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │    mediabox │ (0.0, 0.0, 504.0, 661.5): with=504.0 x height=661.5 │
    │     cropbox │ (0.0, 0.0, 504.0, 661.5): with=504.0 x height=661.5 │
    │      artbox │ (0.0, 0.0, 504.0, 661.5): with=504.0 x height=661.5 │
    │    bleedbox │ (0.0, 0.0, 504.0, 661.5): with=504.0 x height=661.5 │
    │ annotations │ 8                                                   │
    └─────────────┴─────────────────────────────────────────────────────┘
    All annotations:                                                                
    1. /Link at [232.05524, 385.79007, 343.6091, 396.29007]
    2. /Link at [157.63988, 209.99002, 243.69913, 220.49002]
    3. /Link at [72, 178.19678, 249.65918, 188.69678]
    4. /Link at [196.12769, 152.40353, 361.02328, 162.90353]
    5. /Link at [360.97717, 139.80353, 432, 150.30353]
    6. /Link at [72, 127.20352, 213.9915, 137.70352]
    7. /Link at [179.64218, 448.3905, 220.08231, 458.8905]
    8. /Link at [282.84, 347.99005, 340.83148, 358.49005]
```

Get the same metadata in `json` format.

```
pdfly pagemeta document.pdf 100 -o json

    {"mediabox":[0.0,0.0,504.0,661.5],"cropbox":[0.0,0.0,504.0,661.5],"artbox":[0.0,0.0,504.0,661.5],"bleedbox":[0.0,0.0,504.0,661.5],"annotations":19}
```