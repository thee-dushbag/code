<%def name="movie_box()">
  <template id="template-movie-box">
    <div class="col-xl-4 col-lg-4 g-1 col-md-6 col-sm-10 col-xs-12">
      <div class="movie-box" index="$index">
        ## autoplay
        <video src="#" muted autoplay disablepictureinpicture
            data-movie="/source/movies/$movie"
            data-preview="/source/previews/$preview"
            data-thumbnail="/source/thumbnails/$thumbnail"
            data-movie-id="$id-movie"
            poster="/source/thumbnails/$thumbnail"
          >
        </video>
      </div>
    </div>
  </template>
</%def>

<%def name="page_number()">
  <template id="template-page-number">
      <div class="page-number btn">$number</div>
  </template>
</%def>

<%!
from os import getenv
_PORT=getenv('STATICS_PORT') or 9944
_HOST=getenv('STATICS_HOST') or 'localhost'
STATICS_URL=f'http://{_HOST}:{_PORT}/static'
%>