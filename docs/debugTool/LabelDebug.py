from PyQt5.Qt import *
# from OpenGL import GL  # Do not auto clean imports !! from OpenGL import GL is needed for linux

# todo 2/23/17  issue seems to be with linux
# todo 2/23/17  check error with blank screen. ref: https://riverbankcomputing.com/pipermail/pyqt/2014-January/033681.html

firstp =  '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Options</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script type="text/javascript" src=":/qtwebchannel/qwebchannel.js"></script>

    <script type="text/javascript">
        function submit_options() {
            var comments_col = document.getElementById("comments_col").value;
            var tags_col = document.getElementById("tags_col").value;
            var valid = true;
            if (comments_col === null || comments_col === "") {
                alert("Enter name for Comments column");
                valid = false;
            }
            if (tags_col === null || tags_col === "") {
                alert("Enter name for Tags column");
                valid = false;
            }
            if (valid) {
                new QWebChannel(qt.webChannelTransport, function (channel) {
                    channel.objects.bridge.respond("hello");
                });
            }

        }
    </script>
</head>
<body>
<div class="container-fluid">
    <div class="row">
        <div class="col-md-12">
            <h3 class="page-header"> Press the Submit bottom. If the menu page doesn't pop up, there's some problem within the html of py_labeler. </h3>

            <form>
                <div class="form-group">
                    <label for="comments_col">Comments Column Name</label>
                    <input type="text" class="form-control" id="comments_col" placeholder="comments" value="comments" required>
                </div>
                <div class="form-group">
                    <label for="tags_col">Tags Column Name</label>
                    <input type="text" class="form-control" id="tags_col" placeholder="tags" value="tags" required>
                </div>
                <button type="submit" class="btn btn-default" onclick="submit_options()">Submit</button>
            </form>
        </div>
    </div>
</div>
</body>
</html>
'''

secondp = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Py Labeller</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
<style type="text/css">

    body {

    }

    .modal table {
        table-layout: fixed;
    }

    td {
        word-wrap: break-word;
    }

    .menu-section {
        text-align: center;
        background: #F0F8FF;
        border-right: 3px solid #F0FFFF;
        /*box-shadow: inset 0 0 10px black, 0 0 10px black;*/
    }

    .tuple-pair-buttons-div {
        text-align: center;
        margin-bottom: 10px;
    }

    .tuple-pair-buttons-div button {
        margin-bottom: 10px;
    }

    .table {
        margin-bottom: 2px;
        /*over-riding bootstrap's margin-bottom*/
    }

    .Yes {
        background-color: rgba(76, 175, 80, 0.3);
    }

    .Not-Sure {
        background-color: #fcf8e3;
    }

    .Not-Labeled {
        background-color: rgba(158, 158, 158, 0.3);
    }

    .Not-Matched {
        background-color: #f2dede;
    }

    .pagination {
        margin: 3px;
        float: right;
    }

    .btn-danger {
        background-color: rgba(200, 83, 79, 0.85);
    }

    .tuple-pair-div {
        margin-top: 5%;
    }

    .show-tuple-pair td {
        word-wrap: break-word;
    }

    .layout-buttons button {
        width: auto;
        text-overflow: clip;
        margin-left: auto;
        margin-right: auto;
    }

    #menu-row {
        display: table;
        width: 100%;
        height: 100%;
        margin-left: auto;
        margin-right: auto;
    }

    #next-page-btn {
        float: right;
    }

    #filter-pane {
        display: table-cell;
        float: none;
    }

    #filter-pane button {
        width: auto;
        float: left;
    }

    #select-display-pane {
        display: table-cell;
        float: none;
    }

    #attribute-display-pane {
        display: table-cell;
        float: none;
    }

    #misc-options-pane {
        display: table-cell;
        float: none;
    }

    #checkbox-div {
        height: 78%;
        overflow: hidden;
        padding-bottom: 40px;
        overflow-y: auto;
        text-align: left;
    }

    #attribute-display-button #clear-attribute-display-button {
        float: right;
        margin-top: 5%;
        width: 50%;
    }

    #options-change-button {
        float: right;
        margin-top: 1%;
        width: 100%;
    }

    #content-row {
        margin-bottom: 50px;
    }

    #pagination-div {
        background-color: rgba(23, 27, 23, 0.5);
        color: #f7f7f7;
        padding-top: 0px;
        border: 1px solid;
    }

    #save-button {
        float: left;
        width: 100%;
    }

</style>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script type="text/javascript" src=":/qtwebchannel/qwebchannel.js"></script>

<script type="text/javascript">

    var save_file_name = "default_save_file";
    var default_file_name = " default_save_file"
    var current_page = 0;
    var valid_file_name = /^[\w\-\/\\. ]+$/;

    function change_page(page_number) {
        current_page = page_number;
        new QWebChannel(qt.webChannelTransport, function (channel) {

            channel.objects.tuple_pair_display_controller.change_page(page_number);
        });

    }

    function change_token_count() {
        var token_count = document.getElementById("token_number_input").value;
        if ($.isNumeric(token_count) && Math.floor(parseInt(token_count, 10)) > 0) {
            token_count = Math.floor(parseInt(token_count, 10));
            new QWebChannel(qt.webChannelTransport, function (channel) {
                channel.objects.tuple_pair_display_controller.change_token_count(token_count);
            });
        }
        else {
            alert("Alphabet count value has to be a positive integer (more than 0)");
        }
    }

    function filter_tuples(label) {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            channel.objects.filter_controller.get_filtered_tuple_pairs(label);
        });
    }

    function change_label(tuple_pair_id, current_label, new_label) {
        if (String(current_label) !== String(new_label)) {
            new QWebChannel(qt.webChannelTransport, function (channel) {
                document.getElementById(tuple_pair_id).className = "table table-bordered " + new_label;
                channel.objects.label_controller.change_label(tuple_pair_id, new_label);
            });
        }
    }

    function edit_comments(tuple_pair_id, comments) {
        var element = document.getElementById("comments_" + tuple_pair_id);
        if (comments == null || !comments.trim()) {
            comments = element.innerHTML;
        }
        var comments = prompt("Edit comments", comments);
        if (comments == null) comments = "";
        var table_row = document.getElementById("comments_row_" + tuple_pair_id);
        table_row.style = "";
        element.innerHTML = comments;
        new QWebChannel(qt.webChannelTransport, function (channel) {
            channel.objects.label_controller.edit_comments(tuple_pair_id, comments);
        });
    }

    function edit_tags(tuple_pair_id, tags) {
        var element = document.getElementById("tags_" + tuple_pair_id);
        if (tags == null || !tags.trim()) {
            tags = element.innerHTML;
        }
        var tags = prompt("Enter comma separated tags", tags);
        if (tags == null) tags = "";
        var table_row = document.getElementById("tags_row_" + tuple_pair_id);
        table_row.style = "";
        element.innerHTML = tags;
        new QWebChannel(qt.webChannelTransport, function (channel) {
            channel.objects.label_controller.edit_tags(tuple_pair_id, tags);
        });
    }

    function change_layout(new_layout) {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            channel.objects.tuple_pair_display_controller.change_layout(new_layout);
        });
    }

    function filter_attributes(all) {
        if (all != null && all) {
            new QWebChannel(qt.webChannelTransport, function (channel) {
                var checkboxesChecked = "_show_all";
                channel.objects.filter_controller.filter_attribute(checkboxesChecked);
            });
        }
        else {
            new QWebChannel(qt.webChannelTransport, function (channel) {
                var checkedBoxes = document.querySelectorAll('input[name=attribute_filter]:checked');
                var checkboxesChecked = "";
                for (i = 0; i < checkedBoxes.length; i++) {
                    checkboxesChecked = checkboxesChecked.concat(checkedBoxes[i].id);
                    checkboxesChecked = checkboxesChecked.concat(",");
                }
                channel.objects.filter_controller.filter_attribute(checkboxesChecked);
            });
        }
    }

    function save_data() {
        save_file_name = prompt("Please enter your name", default_file_name);
        if (save_file_name != null) {
            if (!save_file_name.trim() || !valid_file_name.test(save_file_name.trim())) {
                alert("Save file name can't be empty. valid file names must have only alphabets, numbers, _ , - and spaces")
            }
            else {
                new QWebChannel(qt.webChannelTransport, function (channel) {
                    channel.objects.tuple_pair_display_controller.save_data(save_file_name);
                });
            }
        }

    }

    window.onload = function () {

        var pad = $("#menu-row").height();
        $('body').css({
            "padding-top": pad
        })
        ;
    }
    window.onresize = function () {

        var pad = $("#menu-row").height();
        $('body').css({
            "padding-top": pad
        })
        ;
    }
</script>
</head>
<body>
<nav class="navbar-fixed-top container-fluid" id="nav_menu">
    <div class="row" id="menu-row">

        <div class="col-sm-3 btn-group-vertical menu-section" id="filter-pane">
            <h7 class="menu-section-header">Filter tuple pairs by label</h7>
            <div class="layout-buttons">
                <button type="button" class="btn btn-default" onclick=filter_tuples('Yes')>Show "Yes" <span
                        class="badge">0</span>
                </button>
                <button type="button" class="btn btn-default" onclick=filter_tuples('Not-Matched')>Show "No" <span
                        class="badge">0</span>
                </button>
                <button type="button" class="btn btn-default" onclick=filter_tuples('Not-Sure')>Show "Not Sure" <span
                        class="badge"> 0</span>
                </button>
                <button type="button" class="btn btn-default" onclick=filter_tuples('Not-Labeled')>Show "Not Labelled" <span
                        class="badge">14</span></button>
                <button type="button" class="btn btn-default" onclick=filter_tuples('All')>Show All <span
                        class="badge">14</span>
                </button>
            </div>
        </div>


        <div class="col-sm-3 btn-group-vertical menu-section" id="select-display-pane">
            <h7 class="menu-section-header">Select display mode for tuple pairs</h7>
            <div class="layout-buttons">
                <button data-toggle="tooltip" title="Displays attributes horizontally and stacks tuple pairs" type="button"
                        class= "btn btn-default active"
                onclick=change_layout("horizontal")>Horizontal
                </button>
                <button data-toggle="tooltip" title="Displays attributes one below each other and stacks tuple pairs" type="button"
                        class= 'btn btn-default'
                onclick=change_layout("vertical")>Vertical</button>
                <button data-toggle="tooltip" title="Displays attributes horizontally and shows one tuple pair at a time" type="button"
                        class= 'btn btn-default'
                onclick=change_layout("single")>One at a time</button>
            </div>
        </div>

        <div class="col-sm-3 menu-section" id="attribute-display-pane">
            <h7 class="menu-section-header">Select which attributes to show</h7>
            <div id="checkbox-div">

                    <div class="checkbox">
                        <label>
                            <input name="attribute_filter" id=ID type="checkbox"> ID
                        </label>
                    </div>

                    <div class="checkbox">
                        <label>
                            <input name="attribute_filter" id=name type="checkbox"> name
                        </label>
                    </div>

                    <div class="checkbox">
                        <label>
                            <input name="attribute_filter" id=zipcode type="checkbox"> zipcode
                        </label>
                    </div>

                    <div class="checkbox">
                        <label>
                            <input name="attribute_filter" id=birth_year type="checkbox"> birth_year
                        </label>
                    </div>

                <button data-toggle="tooltip" title="Display tuple pairs with all attributes" type="button" class="btn btn-default"
                        id="clear-attribute-display-button" onclick=filter_attributes(true)>Clear filter
                </button>
                <button data-toggle="tooltip" title="Display tuple pairs with selected attributes" type="button" class="btn btn-default"
                        id="attribute-display-button" onclick=filter_attributes()>Change displayed attributes


                </button>
            </div>
        </div>


        <div class="col-sm-3 menu-section" id="misc-options-pane">
            <h7 class="menu-section-header">Other options</h7>
            <br>

            <label>Maximum number of letters to show per attribute</label>
            <input type="number" name="attribute-token-count" value=5 id="token_number_input">
            <button data-toggle="tooltip" title="Change the number of letters per attribute displayed" type="button" class="btn btn-md btn-default"
                    id="options-change-button" onclick=change_token_count()>Change number of letters
            </button>
            <br><br>

            <button data-toggle="tooltip" title="Save current labelling status to a csv file" type="button" class="btn btn-md btn-default"
                    id="save-button" onclick=save_data('default_save_file')>
                Save to file
            </button>

        </div>
    </div>
</nav>
<div class="container-fluid">
    <!-- todo: make this div a separate template ? -->
    <!-- make this div a separate template -->
    <div class="row" id="content-row">
        <div class="col-sm-12" id="tuple-pair-pane">




                <div class="tuple-pair-div">
                    <table class="Not-Labeled table table-bordered" id=0>
                        <tr>

                                <td>
                                    <strong>ID</strong>
                                </td>

                                <td>
                                    <strong>name</strong>
                                </td>

                                <td>
                                    <strong>zipcode</strong>
                                </td>

                                <td>
                                    <strong>birth_year</strong>
                                </td>

                        </tr>
                        <tr>

                                <td>
                                    a1
                                </td>

                                <td>
                                    Kevin...
                                </td>

                                <td>
                                    94107
                                </td>

                                <td>
                                    1989
                                </td>

                        </tr>
                        <tr>

                                <td>
                                    b1
                                </td>

                                <td>
                                    Mark ...
                                </td>

                                <td>
                                    94107
                                </td>

                                <td>
                                    1987
                                </td>

                        </tr>
                        <tr id="comments_row_0"
                            style= 'display:none;'
                        >
                        <td><strong>Comments</strong></td>
                        <td colspan="3">
                            <em id="comments_0"></em>
                        </td>
                        </tr>
                        <tr id="tags_row_0"
                            style= 'display:none;'
                        >
                        <td><strong>Tags</strong></td>
                        <td colspan="3">
                            <em id="tags_0"></em>
                        </td>
                        </tr>
                    </table>


                    <div class=" tuple-pair-buttons-div">
                        <button class="btn btn-md btn-success"
                                onclick="change_label(0, 'Not-Labeled', 'Yes')">
                            yes
                        </button>
                        <button class="btn btn-md btn-danger"
                                onclick="change_label(0, 'Not-Labeled', 'Not-Matched')">no
                        </button>
                        <button class="btn btn-sm btn-warning"
                                onclick="change_label(0, 'Not-Labeled', 'Not-Sure')">not sure
                        </button>
                        <button class="btn btn-sm btn-default"
                                onclick="edit_comments(0, '')">edit comments
                        </button>
                        <button class="btn btn-sm btn-default"
                                onclick="edit_tags(0, '')">edit tags
                        </button>
                        <!-- todo: check bootstrap modals -->
                        <button class="btn btn-sm btn-default" data-toggle="modal"
                                data-target=#0modal>show entire tuple pair
                        </button>

                        <div class="modal fade" role="dialog" id=0modal>
                            <div class="modal-dialog">

                                <!-- Modal content-->
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                                        <h4 class="modal-title">Tuple pair id 0</h4>
                                    </div>
                                    <div class="modal-body">

                                        <div>
                                            <table class="Not-Labeled table table-bordered show-tuple-pair">
                                                <tr>
                                                    <td><strong>Attribute</strong></td>
                                                    <td><strong>Table 1</strong></td>
                                                    <td><strong>Table 2</strong></td>
                                                </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>ID</strong>
                                                        </td>
                                                        <td>
                                                            a1
                                                        </td>
                                                        <td>
                                                            b1
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>name</strong>
                                                        </td>
                                                        <td>
                                                            Kevin Smith
                                                        </td>
                                                        <td>
                                                            Mark Levene
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>zipcode</strong>
                                                        </td>
                                                        <td>
                                                            94107
                                                        </td>
                                                        <td>
                                                            94107
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>birth_year</strong>
                                                        </td>
                                                        <td>
                                                            1989
                                                        </td>
                                                        <td>
                                                            1987
                                                        </td>
                                                    </tr>

                                            </table>
                                        </div>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                                    </div>
                                </div>

                            </div>
                        </div>

                    </div>
                </div>



                <div class="tuple-pair-div">
                    <table class="Not-Labeled table table-bordered" id=1>
                        <tr>

                                <td>
                                    <strong>ID</strong>
                                </td>

                                <td>
                                    <strong>name</strong>
                                </td>

                                <td>
                                    <strong>zipcode</strong>
                                </td>

                                <td>
                                    <strong>birth_year</strong>
                                </td>

                        </tr>
                        <tr>

                                <td>
                                    a1
                                </td>

                                <td>
                                    Kevin...
                                </td>

                                <td>
                                    94107
                                </td>

                                <td>
                                    1989
                                </td>

                        </tr>
                        <tr>

                                <td>
                                    b2
                                </td>

                                <td>
                                    Bill ...
                                </td>

                                <td>
                                    94107
                                </td>

                                <td>
                                    1986
                                </td>

                        </tr>
                        <tr id="comments_row_1"
                            style= 'display:none;'
                        >
                        <td><strong>Comments</strong></td>
                        <td colspan="3">
                            <em id="comments_1"></em>
                        </td>
                        </tr>
                        <tr id="tags_row_1"
                            style= 'display:none;'
                        >
                        <td><strong>Tags</strong></td>
                        <td colspan="3">
                            <em id="tags_1"></em>
                        </td>
                        </tr>
                    </table>


                    <div class=" tuple-pair-buttons-div">
                        <button class="btn btn-md btn-success"
                                onclick="change_label(1, 'Not-Labeled', 'Yes')">
                            yes
                        </button>
                        <button class="btn btn-md btn-danger"
                                onclick="change_label(1, 'Not-Labeled', 'Not-Matched')">no
                        </button>
                        <button class="btn btn-sm btn-warning"
                                onclick="change_label(1, 'Not-Labeled', 'Not-Sure')">not sure
                        </button>
                        <button class="btn btn-sm btn-default"
                                onclick="edit_comments(1, '')">edit comments
                        </button>
                        <button class="btn btn-sm btn-default"
                                onclick="edit_tags(1, '')">edit tags
                        </button>
                        <!-- todo: check bootstrap modals -->
                        <button class="btn btn-sm btn-default" data-toggle="modal"
                                data-target=#1modal>show entire tuple pair
                        </button>

                        <div class="modal fade" role="dialog" id=1modal>
                            <div class="modal-dialog">

                                <!-- Modal content-->
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                                        <h4 class="modal-title">Tuple pair id 1</h4>
                                    </div>
                                    <div class="modal-body">

                                        <div>
                                            <table class="Not-Labeled table table-bordered show-tuple-pair">
                                                <tr>
                                                    <td><strong>Attribute</strong></td>
                                                    <td><strong>Table 1</strong></td>
                                                    <td><strong>Table 2</strong></td>
                                                </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>ID</strong>
                                                        </td>
                                                        <td>
                                                            a1
                                                        </td>
                                                        <td>
                                                            b2
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>name</strong>
                                                        </td>
                                                        <td>
                                                            Kevin Smith
                                                        </td>
                                                        <td>
                                                            Bill Bridge
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>zipcode</strong>
                                                        </td>
                                                        <td>
                                                            94107
                                                        </td>
                                                        <td>
                                                            94107
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>birth_year</strong>
                                                        </td>
                                                        <td>
                                                            1989
                                                        </td>
                                                        <td>
                                                            1986
                                                        </td>
                                                    </tr>

                                            </table>
                                        </div>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                                    </div>
                                </div>

                            </div>
                        </div>

                    </div>
                </div>



                <div class="tuple-pair-div">
                    <table class="Not-Labeled table table-bordered" id=2>
                        <tr>

                                <td>
                                    <strong>ID</strong>
                                </td>

                                <td>
                                    <strong>name</strong>
                                </td>

                                <td>
                                    <strong>zipcode</strong>
                                </td>

                                <td>
                                    <strong>birth_year</strong>
                                </td>

                        </tr>
                        <tr>

                                <td>
                                    a1
                                </td>

                                <td>
                                    Kevin...
                                </td>

                                <td>
                                    94107
                                </td>

                                <td>
                                    1989
                                </td>

                        </tr>
                        <tr>

                                <td>
                                    b6
                                </td>

                                <td>
                                    Micha...
                                </td>

                                <td>
                                    94107
                                </td>

                                <td>
                                    1987
                                </td>

                        </tr>
                        <tr id="comments_row_2"
                            style= 'display:none;'
                        >
                        <td><strong>Comments</strong></td>
                        <td colspan="3">
                            <em id="comments_2"></em>
                        </td>
                        </tr>
                        <tr id="tags_row_2"
                            style= 'display:none;'
                        >
                        <td><strong>Tags</strong></td>
                        <td colspan="3">
                            <em id="tags_2"></em>
                        </td>
                        </tr>
                    </table>


                    <div class=" tuple-pair-buttons-div">
                        <button class="btn btn-md btn-success"
                                onclick="change_label(2, 'Not-Labeled', 'Yes')">
                            yes
                        </button>
                        <button class="btn btn-md btn-danger"
                                onclick="change_label(2, 'Not-Labeled', 'Not-Matched')">no
                        </button>
                        <button class="btn btn-sm btn-warning"
                                onclick="change_label(2, 'Not-Labeled', 'Not-Sure')">not sure
                        </button>
                        <button class="btn btn-sm btn-default"
                                onclick="edit_comments(2, '')">edit comments
                        </button>
                        <button class="btn btn-sm btn-default"
                                onclick="edit_tags(2, '')">edit tags
                        </button>
                        <!-- todo: check bootstrap modals -->
                        <button class="btn btn-sm btn-default" data-toggle="modal"
                                data-target=#2modal>show entire tuple pair
                        </button>

                        <div class="modal fade" role="dialog" id=2modal>
                            <div class="modal-dialog">

                                <!-- Modal content-->
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                                        <h4 class="modal-title">Tuple pair id 2</h4>
                                    </div>
                                    <div class="modal-body">

                                        <div>
                                            <table class="Not-Labeled table table-bordered show-tuple-pair">
                                                <tr>
                                                    <td><strong>Attribute</strong></td>
                                                    <td><strong>Table 1</strong></td>
                                                    <td><strong>Table 2</strong></td>
                                                </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>ID</strong>
                                                        </td>
                                                        <td>
                                                            a1
                                                        </td>
                                                        <td>
                                                            b6
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>name</strong>
                                                        </td>
                                                        <td>
                                                            Kevin Smith
                                                        </td>
                                                        <td>
                                                            Michael Brodie
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>zipcode</strong>
                                                        </td>
                                                        <td>
                                                            94107
                                                        </td>
                                                        <td>
                                                            94107
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>birth_year</strong>
                                                        </td>
                                                        <td>
                                                            1989
                                                        </td>
                                                        <td>
                                                            1987
                                                        </td>
                                                    </tr>

                                            </table>
                                        </div>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                                    </div>
                                </div>

                            </div>
                        </div>

                    </div>
                </div>



                <div class="tuple-pair-div">
                    <table class="Not-Labeled table table-bordered" id=6>
                        <tr>

                                <td>
                                    <strong>ID</strong>
                                </td>

                                <td>
                                    <strong>name</strong>
                                </td>

                                <td>
                                    <strong>zipcode</strong>
                                </td>

                                <td>
                                    <strong>birth_year</strong>
                                </td>

                        </tr>
                        <tr>

                                <td>
                                    a2
                                </td>

                                <td>
                                    Micha...
                                </td>

                                <td>
                                    94122
                                </td>

                                <td>
                                    1988
                                </td>

                        </tr>
                        <tr>

                                <td>
                                    b3
                                </td>

                                <td>
                                    Mike ...
                                </td>

                                <td>
                                    94122
                                </td>

                                <td>
                                    1988
                                </td>

                        </tr>
                        <tr id="comments_row_6"
                            style= 'display:none;'
                        >
                        <td><strong>Comments</strong></td>
                        <td colspan="3">
                            <em id="comments_6"></em>
                        </td>
                        </tr>
                        <tr id="tags_row_6"
                            style= 'display:none;'
                        >
                        <td><strong>Tags</strong></td>
                        <td colspan="3">
                            <em id="tags_6"></em>
                        </td>
                        </tr>
                    </table>


                    <div class=" tuple-pair-buttons-div">
                        <button class="btn btn-md btn-success"
                                onclick="change_label(6, 'Not-Labeled', 'Yes')">
                            yes
                        </button>
                        <button class="btn btn-md btn-danger"
                                onclick="change_label(6, 'Not-Labeled', 'Not-Matched')">no
                        </button>
                        <button class="btn btn-sm btn-warning"
                                onclick="change_label(6, 'Not-Labeled', 'Not-Sure')">not sure
                        </button>
                        <button class="btn btn-sm btn-default"
                                onclick="edit_comments(6, '')">edit comments
                        </button>
                        <button class="btn btn-sm btn-default"
                                onclick="edit_tags(6, '')">edit tags
                        </button>
                        <!-- todo: check bootstrap modals -->
                        <button class="btn btn-sm btn-default" data-toggle="modal"
                                data-target=#6modal>show entire tuple pair
                        </button>

                        <div class="modal fade" role="dialog" id=6modal>
                            <div class="modal-dialog">

                                <!-- Modal content-->
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                                        <h4 class="modal-title">Tuple pair id 6</h4>
                                    </div>
                                    <div class="modal-body">

                                        <div>
                                            <table class="Not-Labeled table table-bordered show-tuple-pair">
                                                <tr>
                                                    <td><strong>Attribute</strong></td>
                                                    <td><strong>Table 1</strong></td>
                                                    <td><strong>Table 2</strong></td>
                                                </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>ID</strong>
                                                        </td>
                                                        <td>
                                                            a2
                                                        </td>
                                                        <td>
                                                            b3
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>name</strong>
                                                        </td>
                                                        <td>
                                                            Michael Franklin
                                                        </td>
                                                        <td>
                                                            Mike Franklin
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>zipcode</strong>
                                                        </td>
                                                        <td>
                                                            94122
                                                        </td>
                                                        <td>
                                                            94122
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>birth_year</strong>
                                                        </td>
                                                        <td>
                                                            1988
                                                        </td>
                                                        <td>
                                                            1988
                                                        </td>
                                                    </tr>

                                            </table>
                                        </div>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                                    </div>
                                </div>

                            </div>
                        </div>

                    </div>
                </div>



                <div class="tuple-pair-div">
                    <table class="Not-Labeled table table-bordered" id=7>
                        <tr>

                                <td>
                                    <strong>ID</strong>
                                </td>

                                <td>
                                    <strong>name</strong>
                                </td>

                                <td>
                                    <strong>zipcode</strong>
                                </td>

                                <td>
                                    <strong>birth_year</strong>
                                </td>

                        </tr>
                        <tr>

                                <td>
                                    a2
                                </td>

                                <td>
                                    Micha...
                                </td>

                                <td>
                                    94122
                                </td>

                                <td>
                                    1988
                                </td>

                        </tr>
                        <tr>

                                <td>
                                    b4
                                </td>

                                <td>
                                    Josep...
                                </td>

                                <td>
                                    94122
                                </td>

                                <td>
                                    1982
                                </td>

                        </tr>
                        <tr id="comments_row_7"
                            style= 'display:none;'
                        >
                        <td><strong>Comments</strong></td>
                        <td colspan="3">
                            <em id="comments_7"></em>
                        </td>
                        </tr>
                        <tr id="tags_row_7"
                            style= 'display:none;'
                        >
                        <td><strong>Tags</strong></td>
                        <td colspan="3">
                            <em id="tags_7"></em>
                        </td>
                        </tr>
                    </table>


                    <div class=" tuple-pair-buttons-div">
                        <button class="btn btn-md btn-success"
                                onclick="change_label(7, 'Not-Labeled', 'Yes')">
                            yes
                        </button>
                        <button class="btn btn-md btn-danger"
                                onclick="change_label(7, 'Not-Labeled', 'Not-Matched')">no
                        </button>
                        <button class="btn btn-sm btn-warning"
                                onclick="change_label(7, 'Not-Labeled', 'Not-Sure')">not sure
                        </button>
                        <button class="btn btn-sm btn-default"
                                onclick="edit_comments(7, '')">edit comments
                        </button>
                        <button class="btn btn-sm btn-default"
                                onclick="edit_tags(7, '')">edit tags
                        </button>
                        <!-- todo: check bootstrap modals -->
                        <button class="btn btn-sm btn-default" data-toggle="modal"
                                data-target=#7modal>show entire tuple pair
                        </button>

                        <div class="modal fade" role="dialog" id=7modal>
                            <div class="modal-dialog">

                                <!-- Modal content-->
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                                        <h4 class="modal-title">Tuple pair id 7</h4>
                                    </div>
                                    <div class="modal-body">

                                        <div>
                                            <table class="Not-Labeled table table-bordered show-tuple-pair">
                                                <tr>
                                                    <td><strong>Attribute</strong></td>
                                                    <td><strong>Table 1</strong></td>
                                                    <td><strong>Table 2</strong></td>
                                                </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>ID</strong>
                                                        </td>
                                                        <td>
                                                            a2
                                                        </td>
                                                        <td>
                                                            b4
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>name</strong>
                                                        </td>
                                                        <td>
                                                            Michael Franklin
                                                        </td>
                                                        <td>
                                                            Joseph Kuan
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>zipcode</strong>
                                                        </td>
                                                        <td>
                                                            94122
                                                        </td>
                                                        <td>
                                                            94122
                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td>
                                                            <strong>birth_year</strong>
                                                        </td>
                                                        <td>
                                                            1988
                                                        </td>
                                                        <td>
                                                            1982
                                                        </td>
                                                    </tr>

                                            </table>
                                        </div>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                                    </div>
                                </div>

                            </div>
                        </div>

                    </div>
                </div>




        </div>
        <button class="btn btn-default" id="next-page-btn" onclick="change_page(1)">Next page</button>
    </div>
    <div class="navbar-fixed-bottom" id="pagination-div">




    <ul class="pagination pagination-sm">



                <li class="active"><a href="#" onclick="change_page(0)">1</a></li>



                <li><a href="#" onclick="change_page(1)">2</a></li>



                <li><a href="#" onclick="change_page(2)">3</a></li>



    </ul>

    <div id="pagination_info_text">
        <p>showing 1 page out of 3</p>
    </div>

</div>
</div>
</body>
</html>'''

times = 0

qwebchannel_js = QFile(':/qtwebchannel/qwebchannel.js')
if not qwebchannel_js.open(QIODevice.ReadOnly):
    raise SystemExit(
        'Failed to load qwebchannel.js with error: %s' %
        qwebchannel_js.errorString())
qwebchannel_js = bytes(qwebchannel_js.readAll()).decode('utf-8')


def client_script():
    script = QWebEngineScript()
    script.setSourceCode(qwebchannel_js + '''
    var button = document.getElementById('hello');
    button.onclick = function(){
     new QWebChannel(qt.webChannelTransport, function(channel) {
        channel.objects.bridge.respond('button clicked!!');
    });}
    ''')
    script.setName('xxx')
    script.setWorldId(QWebEngineScript.MainWorld)
    script.setInjectionPoint(QWebEngineScript.DocumentReady)
    script.setRunsOnSubFrames(True)
    return script


class WebPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            print('%s:%s: %s' % (source_id, linenumber, msg))
        except OSError:
            pass

    @pyqtSlot(str)
    def respond(self, text1):
        # print('From JS:', text1)
        global times
        if times == 0:
            p.setHtml('<h2>PyQt5 and its package works well. If you can\'t see this page in py_labeler, check the related function calls. The order matters!</h2><button id="hello">press here</button>')
            times = times + 1
        elif times == 1:
            p.setHtml(firstp)
            times = times + 1
        elif times == 2:
            p.setHtml(secondp)

print('''This is a single debug tool for py_labeler. The first test is a very simple WebPage.
If no GUI pops up, please check you installation of PyQt5.
Also check your system and python version.''')
app = QApplication([])
p = WebPage()
v = QWebEngineView()
v.setPage(p)
p.profile().scripts().insert(client_script())
c = QWebChannel(p)
p.setWebChannel(c)
c.registerObject('bridge', p)
p.setHtml('<h2>Next, press the botton.\n If there is no response, there is some problem with WebChannel or SetHtml in PyQt5.</h2><button id="hello">press here first</button>')
p.setBackgroundColor(Qt.transparent)
v.show()

app.exec_()
