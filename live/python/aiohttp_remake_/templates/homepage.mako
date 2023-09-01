<%inherit file="base.mako"/>

<%block name="content">
    <h1>Hello I'm Jack, I'm ${logged}logged in.</h1><br>
    <a href="${url('login')}">Log me in</a><br>
    <a href="${url('logout')}">Log me out</a><br>
    <h2>Check My permissions.</h2><br>
    <h3>When am Logged in and out.</h3><br>
    <a href="${url('listen')}">Can I listen.</a><br>
    <a href="${url('speak')}">Can I speak.</a><br>
</%block>