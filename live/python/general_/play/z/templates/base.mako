<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="http://localhost:9944/static/bootstrap/css/bootstrap.min.css">
    <script defer src="http://localhost:9944/static/bootstrap/js/bootstrap.bundle.js"></script>
    <script defer src="http://localhost:9944/static/jquery/jquery.min.js"></script>
    <link rel="stylesheet" href="/static/base.css">
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