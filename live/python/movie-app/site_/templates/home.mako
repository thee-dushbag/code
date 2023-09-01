<%inherit file="base.mako"/>

<%block name="metacontent">
    <title>Movie App</title>
</%block>

<%block name="content">
    <div class="vw-100 vh-100">
        <div class="d-flex flex-column w-100 h-100 justify-content-center align-items-center">
            <p class="lead">Welcome to the Movie App</p>
            <a href="/movies" class="btn btn-link border-primary">Movies</a>
        </div>
    </div>
</%block>