<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="http://${STATICS_HOST}:9944/static/bootstrap/css/bootstrap.min.css">
    <script src="http://${STATICS_HOST}:9944/static/bootstrap/js/bootstrap.bundle.min.js" ></script>
</head>
<body>
<%
from mpack.number_reader import NumberReader, locales
from itertools import cycle
reader = NumberReader(locales['english'])
numbers = tuple(reader.read(i) for i in range(1, pages + 1))
colour_pairs = (
    ('dark', 'light'),
    ('light', 'dark'),
    ## ('warning', 'danger'),
    ## ('primary', 'dark')
)
%>
    <div class="container-fluid">
        <div class="row">
            % for num, (c1, c2) in zip(numbers, cycle(colour_pairs)):
                <a class="p-0 m-0 g-0" name="${num.lower()}">
                    <div class="col-12 bg-${c1} vh-100 vw-100 gap-3 d-flex flex-column justify-content-center">
                        <h1 class="text-center text-${c2}"><u><em>Page ${num.title()}</em></u></h1>
                        <div class="w-100 m-0 g-0">
                            <div class="d-flex justify-content-center flex-wrap gap-2">
                                % for other in numbers:
                                    % if other != num:
                                        <a class="btn btn-link text-${c2}" href="#${other.lower()}">${other.title()}</a>
                                    % endif
                                % endfor
                            </div>
                        </div>
                    </div>
                </a>
            % endfor
        </div>
    </div>
</body>
</html>