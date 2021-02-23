from vfb_connect.cross_server_tools import VfbConnect
import feather
import argparse
import numpy
import pandas as pd


parser = argparse.ArgumentParser(
    description="Convert NBLAST matrix in feather format with external IDs into a sparse matrix with VFB IDs.")
# parser.add_argument('--test', help='Run in test mode.',
#                    action="store_true")  # Not doing anything with this yet.
parser.add_argument("input_file", help="path to feather file to use as input")
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("--row_db", required=True,
                    help="identifier (short_form) of DB (AKA site node) for row identifiers (accessions).")
requiredNamed.add_argument("--column_db", required=True,
                    help="identifier (short_form) of DB (AKA site node) for column identifiers (accessions).")
requiredNamed.add_argument("--cutoff", required=True, type=float,
                    help="Threshold above which NBLAST scores are retained in the matrix.")
parser.add_argument("--output_format", "-f", default='feather', help="Output format. Must be feather, tsv or robot")
requiredNamed.add_argument("--output_file", "-o", required=True, help="Output filepath")
args = parser.parse_args()

if not (args.output_format in ['feather', 'robot', 'tsv']):
    raise Exception(ValueError)

def gen_robot_template(df: pd.DataFrame):
    seed = {
        "ID": "ID",
        "TYPE": "TYPE",
        "OBJ": "AI n2o:has_similar_morphology_to",  # AI = Annotation IRI
        "SIMILARITY": ">AT n2o:NBLAST_score^^xsd:float"
    }
    out = [seed]
    vfb_base = 'http://virtualflybrain.org/reports/'
    for i, r in df.iterrows():
        red = r.dropna()
        for column, cell in red.items():
            d = {}
            d['ID'] = vfb_base + i
            d["TYPE"] = "owl:NamedIndividual"
            d['OBJ'] = vfb_base + column
            d['SIMILARITY'] = cell
            out.append(d)
    return pd.DataFrame.from_records(out)


# Load Dataframe from feather file
input_matrix = feather.read_dataframe(args.input_file)

# index by contents of 'index' column:
input_matrix.set_index('index', inplace=True)  # Is this consistent between datasets?

# Get external ID to VFB ID lookups
vc = VfbConnect(neo_endpoint='http://kb.virtualflybrain.org')
row_lookup = vc.neo_query_wrapper.xref_2_vfb_id(db=args.row_db)
column_lookup = vc.neo_query_wrapper.xref_2_vfb_id(db=args.column_db)

# Drop columns representing neurons not in KB; change the rest to VFB_ID
to_drop = []
new_columns = []
for c in input_matrix.columns:
    if c in column_lookup.keys():
        new_columns.append(column_lookup[c][0]['vfb_id'])
    else:
        to_drop.append(c)

input_matrix.drop(columns=to_drop, inplace=True)
input_matrix.columns = new_columns

# Drop rows representing neurons not in KB; change the rest to VFB_ID

rows_to_drop = [i for i in input_matrix.index
                if not (str(i) in row_lookup.keys())]
input_matrix.drop(rows_to_drop, inplace=True)
input_matrix.index = input_matrix.index.map(lambda x: row_lookup[str(x)][0]['vfb_id'])


# Turn everything in matrix with a value less than cutoff to NaN
def threshold(x):
    if x < args.cutoff:
        return numpy.NaN
    else:
        return x


reduced_matrix = input_matrix.applymap(threshold)
#sparse_matrix = reduced_matrix.astype(pd.SparseDtype("float", numpy.NaN))


if args.output_format == 'robot':
    gen_robot_template(reduced_matrix).to_csv(args.output_file, sep='\t', index=False)
elif args.output_format == 'tsv':
    reduced_matrix.to_csv(args.output_file, sep='\t', index=False)
elif args.output_format == 'feather':
    # Need to reset index back to column before saving
    reduced_matrix.reset_index(level=0, inplace=True)
    feather.write_dataframe(args.output_file)










