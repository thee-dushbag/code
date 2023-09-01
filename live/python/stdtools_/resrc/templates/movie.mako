<%inherit file="base.mako"/>

<%block name="title">
Movie PAGE
</%block>

<%def name="movie()">
    <div id="screen">
        <div id="movie_screen">
            <video controls autoplay id="video_screen"></video>
        </div>
        <div id="movie_name"></div>
    </div>
</%def>


<%def name="movie_link(movie_name, mid)">
<%
from pathlib import Path
from os.path import splitext
CHANGES = ('_', ' '), ('.', ' '), ('-', ' ')
def clean(movie_name: str):
    filename = Path(movie_name).name
    name, ext = splitext(filename)
    for tochange, tochangewith in CHANGES:
        name = name.replace(tochange, tochangewith)
    new_name = []
    for char in name:
        if char.isalpha() or char == ' ':
            new_name.append(char)
    name = ''.join(new_name)
    return name.title()
%>
    <div class="movie_link" movie_name="${movie_name}" not_playing="" movie_id="${mid}" onclick="seeMovie(${mid})">
        ${clean(movie_name)}
    </div>
</%def>

<%def name="movie_list(movies)">
    <div id="movie_list">
        % for mid, movie in enumerate(movies):
            ${movie_link(movie, mid + 1)}
        % endfor
    </div>
</%def>

<%block name="content">
    <div id="movie_page">
        ${movie()}
        ${movie_list(movies)}
        <link rel="stylesheet" href="/static/movie.css">
        <script src="/static/movie.js"></script>
    </div>
</%block>