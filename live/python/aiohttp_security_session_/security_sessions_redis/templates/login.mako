<%inherit file="base.mako"/>

<%block name="metacontent">
    <title>Login Page</title>
</%block>

<%block name="content">
    <form action="/login" method="post">
        <label for="username">UserName</label>
        <input type="text" name="username" id="username" required>
        <label for="password">Password</label>
        <input type="password" name="password" id="password" required>
        <input type="submit" value="Login" class="btn btn-primary">
    </form>
</%block>