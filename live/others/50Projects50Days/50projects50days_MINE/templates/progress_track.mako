<%inherit file="base.mako"/>

<%block name="metacontent">
    <title>Progress Tracker</title>
    <script defer src="/static/progress_track.js"></script>
    <link rel="stylesheet" href="/static/progress_track.css">
</%block>

<%block name="content">
    <div class="mycontainer mb-4 border rounded py-3 px-5">
        <div class="myprogress-container">
            <div class="myprogress" id="myprogress"></div>
            <div class="mycircle current-circle myactive">1</div>
            <div class="mycircle">2</div>
            <div class="mycircle">3</div>
            <div class="mycircle">4</div>
            <div class="mycircle">5</div>
            <div class="mycircle">6</div>
            <div class="mycircle">7</div>
        </div>
        <button class="mybtn" id="prev" disabled>Prev</button>
        <button class="mybtn" id="next">Next</button>
    </div>
    <a href="${PROJECT.get_project('index').route_path}" class="btn btn-primary">Home</a>
</%block>