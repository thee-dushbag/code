<%inherit file="base.mako"/>

<%block name="metacontent">
    <title>Home Page</title>
</%block>

<%block name="content">
    <div class="container">
        <div class="row p-2">
            <div class="col-12 d-flex align-items-center flex-column row-gap-3">
                <h1><u>This is the HomePage</u></h1>
                <div class="btn-group">
                % for linkname, link in links.items():
                    <a class="btn btn-link border border-primary" href="${link}">${linkname}</a>
                % endfor
                </div>
            </div>
        </div>
    </div>
</%block>