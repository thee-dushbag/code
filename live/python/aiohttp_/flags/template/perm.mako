<%inherit file="page.mako"/>

<%block name="metacontent">
    <title>Checking Permission.</title>
</%block>

<%block name="page_content">
    <div class="h-100 w-100 d-flex justify-content-center align-items-center">
        <div class="p-2 w-100 border border-2 rounded border-${'success' if granted else 'danger'}">
            <h1 class="text-center">
                <span class="text-warning">${perm.lower()}</span> page.</h1>
            <p class="lead text-center text-${'success' if granted else 'danger'}"><b>
                % if granted:
                    Hooray 
                    <span class="text-warning">${user.name.title()}</span>!!! You have the
                    <span class="text-warning">${perm.lower()}</span> permission.
                % else:
                    Sorry <span class="text-warning">${user.name.title()}</span>, You lack the
                    <span class="text-warning">${perm.lower()}</span> permission.
                % endif
            </b></p>
            <a href="/user" class="btn w-100 btn-${'success' if granted else 'danger'}">Back</a>
        </div>
    </div>
</%block>