<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="http://192.168.0.100:9944/static/bootstrap/css/bootstrap.min.css">
    <script src="http://192.168.0.100:9944/static/bootstrap/js/bootstrap.bundle.min.js"></script>
    <script src="http://192.168.0.100:9944/static/jquery/jquery.min.js"></script>
    <link rel="stylesheet" href="/static/style.css">
    <script defer src="/static/script.js"></script>
    <%block name="head_block">
        <title>Document Title GOES HERE</title>
    </%block>
</head>

<body class="vh-100 vw-100 d-flex flex-column container">
<%block name="body_block">
    Document Content GOES HERE
</%block>
</body>

</html>