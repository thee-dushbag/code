<%
from os import getenv
_HOST, _PORT = getenv("STATICS_HOST"), getenv("STATICS_PORT")
_URL = f'http://{_HOST}:{_PORT}'
STATICS_URL = f'{_URL}/static'
%>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="${STATICS_URL}/bootstrap/css/bootstrap.min.css">
        <link rel="stylesheet" href="${STATICS_URL}/fontawesome/css/all.min.css">
        <script defer src="${STATICS_URL}/bootstrap/js/bootstrap.bundle.min.js"></script>
        <script defer src="${STATICS_URL}/fontawesome/js/all.min.js"></script>
        <script defer src="${STATICS_URL}/jquery/jquery.min.js"></script>
        <%block name="metacontent">
            <title>WebPage Title Goes HERE</title>
        </%block>
    </head>
    <body class="bg-dark text-light vh-100">
        <%block name="content">
            <div class="h-100 w-100 d-flex flex-column justify-content-center align-items-center">
                <h1 class="text-danger display-2">
                    <b>WebPage Content Goes HERE</b>
                </h1>
            </div>
        </%block>
    </body>
</html>