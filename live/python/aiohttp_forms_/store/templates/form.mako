<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form Testing Aiohttp</title>
    <link rel="stylesheet" href="http://192.168.0.100:9944/static/bootstrap/css/bootstrap.min.css">
    <script src="http://192.168.0.100:9944/static/bootstrap/js/bootstrap.bundle.js"></script>
    <script src="http://192.168.0.100:9944/static/jquery/jquery.min.js"></script>
</head>
<body class="bg-dark text-light">
    <div class="container-fluid">
        <div class="row d-flex justify-content-center gap-3">
            <div class="col-12">
                <h1 class="text-center"><em>${title}</em></h1>
            </div>
            <div class="col-lg-8 col-md-10 col-xl-7 col-sm-12 col-xs-12 border rounded">
                <form action="/form" method="post" enctype="multipart/form-data">
                    <div class="container-fluid">
                        <div class="row gap-4 py-3 px-1 d-flex justify-content-center">
                            <div class="col-12">
                                <h1 class="text-center"><u><em>Form Heading.</em></u></h1>
                            </div>
                            <div class="container-fluid col-12">
                                % for l, t in form_values:
                                    <div class="row d-flex align-items-center my-1">
                                        <div class="col-xl-3 col-lg-4 col-md-4 col-sm-12 col-xs-12"><div class="lead h-100">${l}</div></div>
                                        <div class="col-xl-9 col-lg-8 col-md-8 col-sm-12 col-xs-12"><input class="w-100 h-100 p-1" type="${t}" name="${l}"></div>
                                    </div>
                                % endfor
                            </div>
                            <div class="col-lg-6 col-xl-6 col-md-6 col-sm-12 col-xs-12">
                                <div class="d-flex flex-column justify-content-center w-100">
                                    <input class="btn btn-primary w-100" type="submit" value="Submit">
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</body>
</html>