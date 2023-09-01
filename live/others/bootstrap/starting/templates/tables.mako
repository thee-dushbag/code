<%inherit file="base.mako"/>

<%def name="basic_table()">
    <div class="col-lg-6 col-md-8 col-sm-12 col-xs-12 col-xl-5">
        <h1 class="text-center lead"><em>Basic Table</em></h1>
        <table class="table text-light">
            <thead>
                <th>#</th>
                <th>Name</th>
                <th>Age</th>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>Simon Nganga</td>
                    <td>20</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>Lydia Wanjiru</td>
                    <td>37</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>Faith Njeri</td>
                    <td>10</td>
                </tr>
            </tbody>
        </table>
    </div>
</%def>

<%def name="bordered_table()">
    <div class="col-lg-6 col-md-8 col-sm-12 col-xs-12 col-xl-5">
        <h1 class="text-center lead"><em>Bordered Table</em></h1>
        <table class="table table-dark table-bordered">
            <thead>
                <th>#</th>
                <th>Name</th>
                <th>Age</th>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>Simon Nganga</td>
                    <td>20</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>Lydia Wanjiru</td>
                    <td>37</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>Faith Njeri</td>
                    <td>10</td>
                </tr>
            </tbody>
        </table>
    </div>
</%def>

<%def name="hover_table()">
    <div class="col-lg-6 col-md-8 col-sm-12 col-xs-12 col-xl-5">
        <h1 class="text-center lead"><em>Hover Table</em></h1>
        <table class="table table-hover table-dark table-bordered">
            <thead>
                <th>#</th>
                <th>Name</th>
                <th>Age</th>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>Simon Nganga</td>
                    <td>20</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>Lydia Wanjiru</td>
                    <td>37</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>Faith Njeri</td>
                    <td>10</td>
                </tr>
            </tbody>
        </table>
    </div>
</%def>

<%def name="stripped_table()">
    <div class="col-lg-6 col-md-8 col-sm-12 col-xs-12 col-xl-5">
        <h1 class="text-center lead"><em>Striped Table</em></h1>
        <table class="table table-striped table-hover table-dark table-bordered">
            <thead>
                <th>#</th>
                <th>Name</th>
                <th>Age</th>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>Simon Nganga</td>
                    <td>20</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>Lydia Wanjiru</td>
                    <td>37</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>Faith Njeri</td>
                    <td>10</td>
                </tr>
            </tbody>
        </table>
    </div>
</%def>

<%def name="table_two()">
    <div class="col-lg-auto col-xl-auto col-md-8 col-sm-12 col-xs-12">
        <h1 class="text-center lead"><em>Table Two</em></h1>
        <div class="container">
            <div class="row border p-2 d-flex gap-2 justify-content-center">
                % for color in ['danger', 'secondary', 'info', 'primary', 'light', 'dark']:
                    <div class="col-lg-auto col-xl-auto col-md-7 col-sm-12 p-1 col-xs-12">
                        <table class="table table-${color}">
                            <p class="table-caption text-end text-secondary lead">table-${color}</p>
                            <thead>
                                <th>#</th>
                                <th>Name</th>
                                <th>Age</th>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>1</td>
                                    <td>Simon Nganga</td>
                                    <td>20</td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Lydia Wanjiru</td>
                                    <td>37</td>
                                </tr>
                                <tr>
                                    <td>3</td>
                                    <td>Faith Njeri</td>
                                    <td>10</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                % endfor
            </div>
        </div>
    </div>
</%def>

<%block name="content">
    <div class="container">
        <h1 class="text-end my-4"><u>Bootstrap Tables</u></h1>
        <div class="row py-5 px-2 row-gap-5 column-gap-2 m-auto border border-danger border-2">
            ${basic_table()}
            ${bordered_table()}
            ${hover_table()}
            ${stripped_table()}
            ${table_two()}
        </div>
    </div>
</%block>