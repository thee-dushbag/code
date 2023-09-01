<%inherit file="base.mako"/>

<%block name="metacontent">
    <title>User Page</title>
</%block>

<%block name="content">
    <div class="container">
        <div class="row gap-3 p-3">
            <div class="col-xl-6 col-lg-7 col-md-9 col-sm-12">
                <table class="table table-dark table-bordered">
                    <thead>
                        <th>Property</th>
                        <th>Value</th>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Username</td>
                            <td>${user.username}</td>
                        </tr>
                        <tr>
                            <td>Password</td>
                            <td>${user.password}</td>
                        </tr>
                    </tbody>
                </table>
                Your permissions:
                <ol class="list-group list-unstyled p-2 gap-2">
                    % for perm in user.permissions:
                        <li>${perm}</li>
                    % endfor
                </ol>
                Locations Available:
                <div class="btn-group">
                    <a href="/perm/read" class="btn-link btn border border-primary">Read</a>
                    <a href="/perm/write" class="btn-link btn border border-primary">Write</a>
                    <a href="/perm/execute" class="btn-link btn border border-primary">Execute</a>
                    <a href="/logout" class="btn-link btn border border-primary">Logout</a>
                </div>
            </div>
        </div>
    </div>
</%block>