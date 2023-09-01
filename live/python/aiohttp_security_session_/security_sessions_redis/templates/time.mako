<%inherit file="base.mako"/>

<%block name="metacontent">
    <title>Session Timing.</title>
</%block>

<%block name="content">
    <div class="container">
        <div class="row d-flex justify-content-center p-2 gap-2">
            <div class="col-6">
                <table class="table table-dark table-bordered">
                    <thead>
                        <th>Key</th>
                        <th>Value</th>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Last Time</td>
                            <td>${lasttime}</td>
                        </tr>
                        <tr>
                            <td>New Time</td>
                            <td>${newtime}</td>
                        </tr>
                        <tr>
                            <td>Visit Status</td>
                            <td>${visitstatus}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</%block>