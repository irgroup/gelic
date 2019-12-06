## Categories of gelic_collection

- „id“: contains the document-id
- „title_txt_de“/„title_s“: contains title data
- „editor_ss“: contains the editor‘s names
- „imprint_ss“: contains the publisher information
- „year_s“: contains the publishing year
- „isbn_ss“: contains the ISBN number
- „lang_ss“: contains the language of the document
- „size_s“: contains the size of the document
- „class_ddc_ss“/„class_ddc_txt_de“: contains ddc-classification
- „class_dnb_ss“ bzw. „class_dnb_txt_de“: contains the subject groups
- „subject_gnd_ss“/„subject_gnd_txt_de“: contains the intellectually awarded keywords
- „subject_vlb_ss“/„subject_vlb_txt_de“: contains publisher keywords
- „author_ss“: contains the authors names
- „notes_ss“: contains the edition note
- „series_ss“: contains the entity note
- „subject_auto_ss“/„subject_auto_txt_de“: contains the machine-assigned keywords
- „footnote_ss“/„footnote_txt_de“: contains footnote information
- „collection_s“: contains the name of the current collection
- „_version_“: contains solr-version number
- „score“: contains a score value wich is calculated by solr and means a match between words in a query and the found documents

The reason for additional categories like „subject_auto_txt_de“ or „footnote_txt_de“ is the expansion with some solr functions for a better natural language search of the german text.
