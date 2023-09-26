## <% from os import getenv
## _PORT=getenv('STATICS_PORT') or 9944
## _HOST=getenv('STATICS_HOST') or 'localhost'
## STATICS_URL=f'http://{_HOST}:{_PORT}/static'
## %>
<%namespace name="tmp" file="tmps.mako"/>
<!DOCTYPE html5>
  <html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="shortcut icon" href="/public/favicon-64.png" type="image/png">
    <link rel="icon" href="/public/favicon-128.png" type="image/png">
    <link rel="stylesheet" href="${tmp.module.STATICS_URL}/bootstrap/css/bootstrap.min.css" />
    <link rel="stylesheet" href="/static/css/style.min.css" />
    ## <link rel="stylesheet" href="/static/css/style.css" />
    ## <script defer src="${STATICS_URL}/bootstrap/js/bootstrap.bundle.min.js"></script>    
    <%block name="metacontent">
      <title>Movie APP</title>
    </%block>
  </head>
  <body class="bg-dark text-light">
    <%block name="content">
      Body Content GOES HERE
    </%block>
  </body>
</html>