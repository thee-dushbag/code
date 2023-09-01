<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%block name="title">
        WebPageTitle
    </%block></title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="stylesheet" href="http://192.168.0.100:9944/static/bootstrap/css/bootstrap.min.css">
    <script src="http://192.168.0.100:9944/static/bootstrap/js/bootstrap.bundle.min.js"></script>
    <script src="http://192.168.0.100:9944/static/jquery/jquery.min.js"></script>
</head>

<body class="bg-dark text-light user-select-none">
    <%block name="content">
        WebPage CONTENT GOES HERE
    </%block>
</body>

</html>