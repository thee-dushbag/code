<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
        <%block name="title">WebSiteTitle</%block>
    </title>
    <link rel="stylesheet" href="${data.url('static', filename='index.css')}">
</head>

<body>
    <%block name="content">WebSite Content Goes HERE</%block>
</body>

</html>