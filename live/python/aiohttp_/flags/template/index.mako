<%inherit file="base.mako" />

<%block name="metacontent">
    <title>Home Page</title>
</%block>

<%block name="content">
    <div class="h-100 w-100 d-flex flex-column justify-content-center align-items-center">
        <div>
            <h1>Hello There? Welcome.</h1>
            <div class="d-flex gap-2 w-100 flex-column justify-content-center align-items-center">
                <a href="/login" class="btn d-inline-block w-100 btn-primary">Login</a>
                <a href="/signup" class="btn w-100 d-inline-block btn-primary">Signup</a>
            </div>
        </div>
    </div>
</%block>