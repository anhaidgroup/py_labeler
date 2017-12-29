New tool for labeling (experimental)
------------------------------------

WARNING: The new labeler is only available in python version 3.5 and above only.

A new command `label_table` has been added to label the samples. This new
labeler is currently in pre-alpha stage and is still incomplete. Use at your
own risk. An example use is shown below:

    >>> G = em.label_table(S, label_column_name='gold_labels')

The new labeler completes the same task as `label_table` in that it will take
an input table `S` with pairs of tuples and create a copy table `G` with
additional label, comment, and tags columns. The command will open a GUI that
allows the user to label each pair of tuples with with either 'Yes', 'No', or
'Not-Sure'.

Please refer to the API reference of :py:meth:`~py_labeler.label_table`
for more details
