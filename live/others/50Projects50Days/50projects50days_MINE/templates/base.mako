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
        <script defer src="${STATICS_URL}/bootstrap/js/bootstrap.bundle.js"></script>
        <script defer src="${STATICS_URL}/jquery/jquery.min.js"></script>
        <link rel="stylesheet" href="/static/global.css"/>
        <script defer src="/static/global.js"></script>
        <%block name="metacontent">
            <title>Learning CSS</title>
        </%block>
    </head>
    <body class="p-0 m-0 g-0 gap-0 vh-100 vw-100">
        <div id="body" class="bg-dark text-light h-100">
            <%block name="content">
                Website Content GoesHERE
            </%block>
        </div>
    </body>
</html>