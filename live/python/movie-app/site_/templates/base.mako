<%
from os import getenv
_HOST = getenv('STATICS_HOST')
_PORT = getenv('STATICS_PORT')
STATICS_URL = f'http://{_HOST}:{_PORT}/static'
%>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="/static/favicon.128.ico" type="image/x-icon">
    <link rel="stylesheet" href="${STATICS_URL}/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/style.css">
    <script defer src="${STATICS_URL}/bootstrap/js/bootstrap.bundle.js"></script>
    <script defer src="${STATICS_URL}/jquery/jquery.min.js"></script>
    <script defer src="/static/script.js"></script>
    <%block name="metacontent">
      <title>WebPage Title</title>
    </%block>
  </head>
  <body class="bg-dark text-light">
    <%block name="content">
      WebPage Content Goes Here
    </%block>
  </body>
</html>
