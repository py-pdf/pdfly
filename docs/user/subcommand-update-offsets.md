# update-offsets

Updates offsets and lengths in a simple PDF file.                              

## Usage

```
$ pdfly update-offsets --help                                                                                                                                                                                                                                                        
 Usage: pdfly update-offsets [OPTIONS] FILE_IN FILE_OUT                         
                                                                                
 Updates offsets and lengths in a simple PDF file.                              
                                                                                
 The PDF specification requires that the xref section at the end                
 of a PDF file has the correct offsets of the PDF's objects.                    
 It further requires that the dictionary of a stream object                     
 contains a /Length-entry giving the length of the encoded stream.              
                                                                                
 When editing a PDF file using a text-editor (e.g. vim) it is                   
 elaborate to compute or adjust these offsets and lengths.                      
                                                                                
 This command tries to compute /Length-entries of the stream dictionaries       
 and the offsets in the xref-section automatically.                             
                                                                                
 It expects that the PDF file has ASCII encoding only. It may                   
 use ISO-8859-1 or UTF-8 in its comments.                                       
 The current implementation incorrectly replaces CR (0x0d) by LF (0x0a) in      
 binary data.                                                                   
 It expects that there is one xref-section only.                                
 It expects that the /Length-entries have default values containing             
 enough digits, e.g. /Length 000 when the stream consists of 576 bytes.         
                                                                                
 Example:                                                                       
    update-offsets --verbose --encoding ISO-8859-1 issue-297.pdf                
 issue-297.out.pdf                                                              
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    file_in       FILE  [default: None] [required]                          │
│ *    file_out      PATH  [default: None] [required]                          │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --encoding                    TEXT  Encoding used to read and write the      │
│                                     files, e.g. UTF-8.                       │
│                                     [default: ISO-8859-1]                    │
│ --verbose     --no-verbose          Show progress while processing.          │
│                                     [default: no-verbose]                    │
│ --help                              Show this message and exit.              │
╰──────────────────────────────────────────────────────────────────────────────╯

```

## Examples

Update the offsets of `document.pdf` with UTF-8 encoding and write the output to `document.out.pdf`.
```
pdfly update-offsets document.pdf --verbose --encoding UTF-8 document.out.pdf
```