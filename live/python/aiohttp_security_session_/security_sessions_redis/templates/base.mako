<%
from os import getenv
HOST, PORT = getenv('STATICS_HOST'), getenv('STATICS_PORT')
STATICS_URL = f'http://{HOST}:{PORT}/static'
%>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="${STATICS_URL}/bootstrap/css/bootstrap.min.css">
        <script defer src="${STATICS_URL}/bootstrap/js/bootstrap.bundle.min.js"></script>
        <script defer src="${STATICS_URL}/jquery/jquery.min.js"></script>
        <%block name="metacontent">
            <title>WebSite Title</title>
        </%block>
    </head>
    <body>
        <div id="body" class="bg-dark text-light vh-100 vw-100">
        <%block name="content">
            WebSite Content GOES HERE
        </%block>
        </div>
    </body>
</html>