<%inherit file="base.mako" />

<%block name="metacontent">
  <title>Movie App</title>
</%block>

<%block name="content">
  <div class="vw-100 vh-100">
    <div class="d-flex gap-2 flex-column w-100 h-100 justify-content-center align-items-center">
      <p class="lead"><u>Welcome to the Movie App</u></p>
      <div class="d-flex gap-2">
        <p>Watch Movies:</p>
        <a href="/movies" class="btn btn-success">Movies</a>
      </div>
      <div class="d-flex gap-2">
        <p>Reload Content:</p>
        <a href="/api/refresh?load=n" class="btn btn-danger">Reload</a>
      </div>
      <div class="d-flex gap-2">
        <p>Sort By:</p>
        <div class="btn-group-vertical">
          % for order in orders:
            <a href="/api/refresh?sortby=${str(order)}"
              class="btn btn-${'warning' if order == movies.order else 'primary'}">
              ${str(order).title()}
            </a>
          % endfor
        </div>
      </div>
    </div>
  </div>
</%block>
