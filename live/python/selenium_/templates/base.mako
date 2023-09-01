<html>
    <head>
        <title>WebPage Title</title>
        <link rel="stylesheet" href="http://localhost:9944/static/bootstrap/css/bootstrap.min.css">
        <script defer src="http://localhost:9944/static/bootstrap/js/bootstrap.bundle.min.js"></script>
        <link rel="stylesheet" href="/static/index.css">
    </head>

    <body class="d-flex flex-col align-items-center justify-content-center vh-100 vw-100">
        <%block name="content">
            WebPage Content Goes HERE
        </%block>
    </body>
</html>