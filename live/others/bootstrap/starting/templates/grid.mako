<%inherit file="base.mako"/>

<%block name="title">
    Grid Page
</%block>

<%def name="get_color()">
<%

%>
${choice(colors)}
</%def>

<%block name="content">
    <div class="container my-5">
        <h2>Basic Grid</h2>
        <div class="row">
        % for i in range(1, 4):
            <div class="col">
                <div class="rounded d-flex g-0 justify-content-center p-3 bg-primary text-light">
                    Col ${i}
                </div>
            </div>
        % endfor
        </div>
    </div>
    <div class="container my-5">
        <h2>Column Widths</h2>
        <div class="row">
            <div class="col-6">
                <div class="rounded d-flex g-0 justify-content-center p-3 bg-primary text-light">
                    Col 1
                </div>
            </div>
            <div class="col-3">
                <div class="rounded d-flex g-0 justify-content-center p-3 bg-primary text-light">
                    Col 2
                </div>
            </div>
            <div class="col-3">
                <div class="rounded d-flex g-0 justify-content-center p-3 bg-primary text-light">
                    Col 3
                </div>
            </div>
        </div>
    </div>
        <div class="container my-5">
        <h2>Responsive Column Widths</h2>
        <div class="row justify-content-lg-center justify-content-md-center">
            <div class="col-xs-12 col-sm-4 col-lg-3 col-md-4 gx-1 gy-1">
                <div class="rounded d-flex justify-content-center p-3 bg-primary text-light">
                    Col 1
                </div>
            </div>
            <div class="col-xs-12 col-sm-4 col-lg-3 col-md-4 gx-1 gy-1">
                <div class="rounded d-flex justify-content-center p-3 bg-primary text-light">
                    Col 2
                </div>
            </div>
            <div class="col-xs-12 col-sm-4 col-lg-3 col-md-4 gx-1 gy-1">
                <div class="rounded d-flex justify-content-center p-3 bg-primary text-light">
                    Col 3
                </div>
            </div>
            <div class="col-xs-12 col-sm-6 col-lg-9 col-md-12 gx-1 gy-1 col-sm-12">
                <div class="rounded d-flex justify-content-center p-3 bg-primary text-light">
                    Col 3
                </div>
            </div>
        </div>
    </div>
</%block>