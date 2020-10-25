from vfb_connect.cross_server_tools import VfbConnect
import feather
import argparse
import numpy


parser = argparse.ArgumentParser(
    description="Convert NBLAST matrix in feather format with external IDs into a sparse matrix with VFB IDs.")
# parser.add_argument('--test', help='Run in test mode.',
#                    action="store_true")  # Not doing anything with this yet.
parser.add_argument("input_file", help="path to feather file to use as input")
parser.add_argument("row_db", help="identifier (short_form) of DB (AKA site node) for row identifiers (accessions).")
parser.add_argument("column_db",
                    help="identifier (short_form) of DB (AKA site node) for column identifiers (accessions).")
parser.add_argument("cutoff", type=float, help="threshold above which NBLAST scores are retained in the matrix.")
args = parser.parse_args()

# Load Dataframe from feather file
input_matrix = feather.read_dataframe(args.input_file)

# index by contents of 'index' column:
input_matrix.set_index('index', inplace=True)  # Is this consistent between datasets?

# Get external ID to VFB ID lookups
vc = VfbConnect()
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
                if not (i in row_lookup.keys())]
input_matrix.drop(rows_to_drop, inplace=True)
input_matrix.index = input_matrix.index.map(lambda x: row_lookup[x][0]['vfb_id'])


# Turn everything in matrix with a value less than cutoff to NaN
def threshold(x):
    if x < args.cutoff:
        return numpy.NaN
    else:
        return x


reduced_matrix = input_matrix.applymap(threshold)
#sparse_matrix = reduced_matrix.astype(pd.SparseDtype("float", numpy.NaN))

# Reset index back to column & save

reduced_matrix.reindex()
feather.write_dataframe(reduced_matrix, 'reduced_matrix.feather')










