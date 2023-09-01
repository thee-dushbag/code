<%inherit file="base.mako"/>

<%block name="metacontent">
    <title>Movie App</title>
</%block>

<%def name="movie_box_template()">
    <div class="movie-box" index="$index">
        <video src="#" muted autoplay
            data-movie="/source/movie/$movie"
            data-preview="/source/preview/$preview"
            data-thumbnail="/source/thumbnail/$thumbnail"
            poster="/source/thumbnail/$thumbnail">
        </video>
    </div>
</%def>


<%def name="movie_block(movies=None)">
    <div id="movie-block">
        <div id="space"></div>
        <div class="container-fluid">
            <div id="movie-container" class="row d-flex justify-content-center row-gap-2">
            </div>
        </div>
    </div>
</%def>

<%def name="player_block()">
    <div id="player-block" class="bg-dark">
        <div class="container-fluid">
            <div class="row d-flex justify-content-center align-items-center">
                <video id="player" muted src="#" autoplay controls></video>
                ${paginate_block()}
            </div>
        </div>
    </div>
</%def>

<%def name="paginate_block()">
    <div id="paginate" class="py-2 d-flex justify-content-center align-items-center">
        <div id="page-buttons" class="d-flex justify-content-center column-gap-2">
            <div id="page-prev" class="btn btn-primary flex-shrink">&lt;&lt;</div>
            <div class="btn-group flex-fill" id="page-row"></div>
            <div id="page-next" class="btn btn-primary flex-shrink">&gt;&gt;</div>
        </div>
    </div>
</%def>

<%def name="movie_app()">
    <div id="app">
        ${player_block()}
        ${movie_block(movies)}
    </div>
    <div class="py-2 w-100"></div>
</%def>

<%def name="templates()">
    <template id="movie-box-template">
        <div class="col-xl-3 col-lg-4 g-2 col-md-6 col-sm-8 col-xs-12">
            ${movie_box_template()}
        </div>
    </template>
    <template id="page-number-template">
        <div class="page-number btn">$number</div>
    </template>
</%def>

<%block name="content">
    ${movie_app()}
    ${templates()}
</%block>