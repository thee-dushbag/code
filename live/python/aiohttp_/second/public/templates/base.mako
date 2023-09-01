<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Message App</title>
    <link rel="stylesheet" href="http://192.168.0.100:9944/static/bootstrap/css/bootstrap.min.css">
    <script src="http://192.168.0.100:9944/static/bootstrap/js/bootstrap.bundle.min.js"></script>
    <script src="http://192.168.0.100:9944/static/jquery/jquery.min.js"></script>
    <link rel="stylesheet" href="/static/style.css">
    <script defer src="/static/script.js"></script>
</head>
<body>
    <div class="bg-dark text-light">
        <%block name="content">
            Website Content GOES HERE
        </%block>
    </div>
</body>
</html>