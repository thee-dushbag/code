<%inherit file="base.mako"/>

<%block name="metacontent">
    <title>One Page</title>
    <link rel="stylesheet" href="/static/one.css">
</%block>

<%block name="content">
    <div class="vw-100 vh-100 bg-secondary d-flex flex-column justify-content-center align-items-center">
        <div class="w-50 h-75 rounded bg-dark p-3 my-box" name="box">
            <div class="bg-danger rounded-top" name="heading">
                <h1><center>Message App</center></h1>
            </div>
            <div class="bg-warning px-1 py-1 overflow-y-scroll overflow-y-hidden gap-1 d-flex flex-column" name="messages">
                <div class="card">
                    <div class="card-body">Hello Mark</div>
                    <div class="card-footer"><small><span class="text-muted float-end">@Simon</span></small></div>
                </div>
                <div class="card">
                    <div class="card-body">Hello Simon</div>
                    <div class="card-footer"><small><span class="text-muted float-end">@Mark</span></small></div>
                </div>
                <div class="card">
                    <div class="card-body">Hello Mark</div>
                    <div class="card-footer"><small><span class="text-muted float-end">@Simon</span></small></div>
                </div>
                <div class="card">
                    <div class="card-body">Hello Mark</div>
                    <div class="card-footer"><small><span class="text-muted float-end">@Simon</span></small></div>
                </div>
            </div>
            <div class="bg-success" name="inputarea">
                <textarea name="message_input" id="" class="w-100 h-50"></textarea>
                <div class="btn btn-primary w-100 h-50">Send</div>
            </div>
        </div>
    </div>
</%block>