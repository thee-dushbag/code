<%inherit file="page.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="user_details(user)">
    <div class="p-2">
        <h1>User Details</h1>
        <table class="table text-light table-bordered">
            <thead>
                <th>Attribute</th>
                <th>Value</th>
            </thead>
            <tbody>
                <tr>
                    <td>Name</td>
                    <td>${user.name}</td>
                </tr>
                <tr>
                    <td>Email</td>
                    <td>${user.email}</td>
                </tr>
                <tr>
                    <td>Permission</td>
                    <td>${user.permission}</td>
                </tr>
            </tbody>
        </table>
    </div>
</%def>

<%def name="user_permissions(perms)">
    <div class="p-2">
        <h1>Available Permissions</h1>
        <table class="table text-light table-bordered">
            <thead>
                <th>Permission</th>
                <th>Value</th>
            </thead>
            <tbody>
            % for perm, value in perms.items():
                <tr>
                    <td>
                        <a href="/perm/${perm.lower()}" class="p-0 btn btn-link">${perm.title()}</a>
                        <a href="/test/${perm.lower()}" class="p-0 btn btn-link">test</a>
                    </td>
                    <td class="text-${'success' if value else 'danger'}">${str(value).lower()}</td>
                </tr>
            % endfor
            </tbody>
        </table>
    </div>
</%def>


<%def name="perm_form(perms)">
    <div class="border rounded p-2 gap-2">
        <h1 class="text-center"><u>Change Permissions</u></h1>
        <hr class="w-100">
    ${utils.form_block(
        dest='/update_perm',
        method='post',
        submit='Update',
        field=utils.checked_input,
        inputs=[
            (name.title(), name.lower(), value)
            for name, value in perms.items()
        ],
        home='/logout',
        home_lbl="Logout"
    )}
    </div>
</%def>

<%block name="page_content">
    <div class="d-flex flex-column gap-2">
        <h1 class="text-center">Welcome <span class="text-danger">${user.name.title()}</span></h1>
        ${user_details(user)}
        ${user_permissions(perms)}
        ${perm_form(perms)}
    </div>
</%block>