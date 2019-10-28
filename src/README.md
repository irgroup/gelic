# GND Synonyms

## Convert the GND encoding into proper utf-8

DNB presentation on how and why decomposed character encoding is used by DNB:
https://wiki.dnb.de/download/attachments/125420735/5-1-Codierung_UTF8_Heuvelmann.pdf?version=1&modificationDate=1501514354000&api=v2

To convert decomposed encoding into composed encoding you can use uconv (provided by ICU - International Components for Unicode). On Mac uconv is available through Homebrew:

```bash
$> brew install icu4c
$> /usr/local/Cellar/icu4c/64.2/bin/uconv  -f utf-8 -t utf-8 -x NFC synonyms.txt > synonyms_utf8.txt
``` 
