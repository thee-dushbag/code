<%inherit file="base.mako"/>

<%block name="metacontent">
    <title>Message Page</title>
</%block>

<%block name="content">
    <div class="vh-100 vw-100 d-flex justify-content-center align-items-center">
        <div>${message}</div>
    </div>
</%block>