# NBLAST matrix proc

**usage:** `convert_matrix.py [-h] input_file row_db column_db cutoff`

Convert NBLAST matrix in feather format with external IDs into a sparse matrix with VFB IDs.

**positional arguments:**

  -  `input_file`  path to feather file to use as input

**optional arguments:**

  - -h, --help            show this help message and exit
  - --output_format OUTPUT_FORMAT, -f OUTPUT_FORMAT
                        Output format. Must be feather, tsv or robot

**required named arguments:**

  - --row_db ROW_DB       identifier (short_form) of DB (AKA site node) for row identifiers (accessions).
  - --column_db COLUMN_DB
                        identifier (short_form) of DB (AKA site node) for column identifiers (accessions).
  - --cutoff CUTOFF       Threshold above which NBLAST scores are retained in the matrix.
  - --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Output filepath


 (This doc may be out of date.  For latest check `convert_matrix.py -h`)
