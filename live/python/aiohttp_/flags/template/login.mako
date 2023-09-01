<%inherit file="page.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%block name="metacontent">
    <title>Login Page</title>
</%block>

<%def name="login_form()">
    ${utils.form_block(
        '/loginp',
        method='post',
        submit='Login',
        inputs=[
            ('Name', 'username', 'text'),
            ('Password', 'password', 'password')
    ])}
</%def>


<%block name="page_content">
    <div class="border rounded p-2 gap-2">
        <h1 class="text-center"><u>Login Form</u></h1>
        <hr class="w-100">
        ${login_form()}
    </div>
</%block>