<%inherit file="page.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%block name="metacontent">
    <title>Signup Page</title>
</%block>

<%def name="signup_form()">
    ${utils.form_block(
        dest='/signupp',
        method='post',
        submit='Signup',
        inputs=[
            ('Name', 'username', 'text'),
            ('Email', 'useremail', 'email'),
            ('Password', 'password', 'password')
    ])}
</%def>

<%block name="page_content">
    <div class="border rounded p-2 gap-2">
        <h1 class="text-center"><u>SignUp Form</u></h1>
        <hr class="w-100">
        ${signup_form()}
    </div>
</%block>