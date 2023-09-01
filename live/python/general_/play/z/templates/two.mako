<%inherit file="base.mako"/>

<%block name="metacontent">
    <title>Two Page</title>
    <script defer src="/static/two.js"></script>
</%block>

<%block name="content">
    <div class="container">
        <div class="row gap-2 p-2 d-flex flex-column align-items-center p-2">
            <div class="col-xl-4 d-flex flex-column gap-2 p-2 border" id="flushes">
                <div class="bg-light text-wrap text-dark lead p-2">
                    Hello There
                </div>
            </div>
        </div>
    </div>
</%block>