<%inherit file="base.mako"/>

<%block name="title">
Line App
</%block>

<%block name="content">
    <h1>
        <center id="title">Hello World</center>
    </h1><br>
    <a href="/" class="btns">Home</a>
    <a href="/movie_page" class="btns">Movies</a>
    <button onclick="clicked()">Click Me</button>
    <div id="line_project">
        <div id="lines">
            ## <div class="line">This is a line</div>
        </div>
        <div id="line_form">
            <div id="input_line">
                <label for="line_input">Line Value</label>
                <input type="text" id="line_input">
            </div>
            <div id="btns">
                <button onclick="addLine()">AddLine</button>
                <button onclick="tellServerAllLines()">TellServer</button>
            </div>
        </div>
    </div>
    <script src="/static/index.js"></script>
    <link rel="stylesheet" href="/static/style.css">
</%block>