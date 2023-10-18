
<%inherit file="base.mako" />
<%namespace name="template" file="tmps.mako" />

<%def name="paginate_block()">
  <div id="paginate" class="paginate py-1 px-0">
    <div id="page-buttons" class="d-flex text-light justify-content-center column-gap-2">
      <div id="page-prev" class="page-btn btn btn-primary flex-shrink">&laquo;</div>
      <div class="btn-group flex-fill" id="page-row"></div>
      <div id="page-next" class="page-btn btn btn-primary flex-shrink">&raquo;</div>
    </div>
  </div>
</%def>

<%def name="player_block()">
  <div class="player-block bg-dark d-flex flex-column align-items-center">
    <div class="player-container d-flex justify-content-center">
      <video src="#" autoplay controls muted class="player" id="main-player"></video>
    </div>
    ${paginate_block()}
  </div>
</%def>

<%def name="content_block()">
  <div class="content-block container">
    <div id="movie-row" class="row d-flex justify-content-center">
    </div>
  </div>
</%def>

<%def name="movie_app()">
  ${player_block()}
  ${content_block()}
</%def>

<%def name="templates()">
  ${template.movie_box()}
  ${template.page_number()}
</%def>

<%block name="content">
  ${movie_app()}
  ${templates()}
</%block>

<%block name="metacontent">
  <script defer src="${template.module.STATICS_URL}/jquery/jquery.min.js"></script>
  <script defer src="/static/js/script.min.js"></script>
  ## <script defer src="/static/js/script.js"></script>
</%block>