<%inherit file="base.mako"/>

<%block name="content">
    <div class="container h-100">
        <div class="row d-flex h-100 justify-content-center">
            <div class="col-xl-9 h-100 col-lg-10 pt-2 pb-3 col-md-12 col-sm-12">
                <%block name="page_content">
                    <div class="text-danger display"><b>Page Content</b></div>
                </%block>
            </div>
        </div>
    </div>
</%block>