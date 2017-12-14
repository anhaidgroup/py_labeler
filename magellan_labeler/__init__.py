# # labeling
from magellan_labeler.labeler.labeler import label_table

# # generic helper functions
from magellan_labeler.utils.generic_helper import get_install_path, load_dataset, \
    add_output_attributes

# # pandas helper functions
from magellan_labeler.utils.pandas_helper import filter_rows, project_cols, \
    mutate_col, rename_col, preserve_metadata, drop_cols

# GUI related
_viewapp = None
