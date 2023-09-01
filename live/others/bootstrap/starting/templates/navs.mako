<%inherit file="base.mako"/>

<%def name="basic_nav()">
    <div class="col-12">
        <h1 class="lead"><em>Basic Nav/Navbar</em></h1>
    </div>
</%def>

<%block name="content">
    <div class="container">
        <h1 class="text-end mt-5 mb-3"><u>Bootstrap Navbars and Navs</u></h1>
        <hr class="mb-2">
        <div class="row border">
            ${basic_nav()}
        </div>
    </div>
</%block>