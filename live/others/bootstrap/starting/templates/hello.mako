<%inherit file="base.mako"/>
<%block name="title">Hello Page</%block>

<%block name="content">
    <div class="container vh-100 d-flex flex-column justify-content-center align-items-center gap-3">
        <h1><center>Hello ${name.title()}</center></h1>
        <form class="p-3 w-50 m-2 rounded-4 d-flex flex-column gap-2 border" action="${url('hello_form')}" method="post">
            <div class="d-flex">
            <label class="w-25" for="name">Name</label>
            <input class="w-75 rounded-2 px-2" type="text" name="name" id="name">
            </div>
            <input class="btn btn-primary rounded-pill" type="submit" value="Say Hello">
        </form>
    </div>
</%block>