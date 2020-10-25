# NBLAST matrix proc

**usage:** `convert_matrix.py [-h] input_file row_db column_db cutoff`

Convert NBLAST matrix in feather format with external IDs into a sparse matrix with VFB IDs.

**positional arguments:**
 -  `input_file`  path to feather file to use as input
 -  `row_db`      identifier (short_form) of DB (AKA site node) for row identifiers (accessions).
 -  `column_db`   identifier (short_form) of DB (AKA site node) for column identifiers (accessions).
 -  `cutoff`      threshold above which NBLAST scores are retained in the matrix.

**optional arguments:**
  -h, --help  show this help message and exit
  
 (This doc may be out of date.  For latest check `convert_matrix.py -h`)
