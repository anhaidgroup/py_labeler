Labeling Tool
-------------

The command `label_table` is used to label the samples.
An example use is shown below:

    >>> import py_labeler as pl
    >>> G = pl.label_table(S, label_column_name='gold_labels')

The new labeler will take an input table `S` with pairs of tuples and create
a copy table `G` with additional label, comment, and tags columns. The command
will open a GUI that allows the user to label each pair of tuples with with
either 'Yes', 'No', or 'Not-Sure'.

Please refer to the API reference of :py:meth:`~py_labeler.label_table`
for more details
