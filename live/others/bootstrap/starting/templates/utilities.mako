<%inherit file="base.mako"/>

<%def name="borders()">
    <div class="col-sm-12 col-md-9 col-lg-auto col-xl-auto mx-auto">
        <h2 class="text-center">Bootstrap Borders</h2>
        % for color in ['danger', 'secondary', 'dark', 'light', 'success', 'primary', 'info', 'warning']:
            <div class="border border-${color} p-3 m-1">
                Hello this is ${color}
            </div>
        % endfor
    </div>
</%def>

<%def name="borders_widths()">
    <div class="col-sm-12 col-md-9 col-lg-auto col-xl-auto mx-auto">
        <h2 class="text-center">Bootstrap Border Width</h2>
        % for i in range(1, 6):
            <div class="border border-${i} border-success p-3 m-1">
                border-${i}
            </div>
        % endfor
    </div>
</%def>


<%def name="backgrounds_colors()">
    <div class="col-sm-12 col-md-9 col-lg-auto col-xl-auto mx-auto">
        <h2 class="text-center">Bootstrap Backgroud Colors</h2>
        % for color in ['danger', 'secondary', 'dark', 'light', 'success', 'primary', 'info', 'warning']:
            <div class="border bg-${color} p-3 m-1">
                bg-${color}
            </div>
        % endfor
    </div>
</%def>

<%def name="backgrounds_colors_opacities()">
    <div class="col-sm-12 col-md-9 col-lg-auto col-xl-auto mx-auto">
        <h2 class="text-center">Bootstrap Backgroud Color Opacity</h2>
        <div class="container">
            <div class="border p-2 gap-1 d-flex justify-content-center row">
            % for color in ['danger', 'secondary', 'dark', 'light', 'success', 'primary', 'info', 'warning']:
                <div class="col-lg-auto col-md-12 col-xl-auto col-sm-12 col-xs-12 p-1">
                    % for op in [10, 25, 50, 75, 100]:
                    <div class="bg-${color} bg-opacity-${op} p-3">
                        bg-opacity-${op} bg-${color}
                    </div>
                % endfor
                </div>
            % endfor
            </div>
        </div>
    </div>
</%def>

<%def name="text_colors_opacities()">
    <div class="col-sm-12 col-md-9 col-lg-auto col-xl-auto mx-auto">
        <h2 class="text-center">Bootstrap Text Color Opacity</h2>
        <div class="container">
            <div class="row p-2 gap-2 border d-flex justify-content-center">
                % for color in ['danger', 'secondary', 'dark', 'light', 'success', 'primary', 'info', 'warning']:
                    <div class="border p-1 col-lg-auto col-md-12 col-xl-auto col-sm-12 col-xs-12">
                        % for op in [25, 50, 75, 100]:
                        <div class="text-${color} text-md-center text-opacity-${op} p-3 m-1">
                            text-opacity-${op} text-${color}
                        </div>
                    % endfor
                    </div>
                % endfor
            </div>
        </div>
    </div>
</%def>

<%def name="backgrounds_colors()">
    <div class="col-sm-12 col-md-9 col-lg-auto col-xl-auto mx-auto">
        <h2 class="text-center">Bootstrap Text Colors</h2>
        % for color in ['danger', 'secondary', 'dark', 'light', 'success', 'primary', 'info', 'warning']:
            <div class="border text-${color} p-3 m-1">
                text-${color}
            </div>
        % endfor
    </div>
</%def>

<%def name="varying_border()">
    <script>
        $(function() {
            let cur = 0;
            let classes = ['border-danger', 'border-success'];
            let target = $('#target');
            target.addClass(classes[cur])
            function classToggler() {
                let curclass = classes[cur % 2];
                cur++;
                let rmclass = classes[cur % 2];
                return [curclass, rmclass]
            }
            target.click(function() {
                let cls = classToggler();
                target.removeClass(cls[0]);
                target.addClass(cls[1]);
            })
            target.slideDown(3000);
            $('html').scrollTop(0)
            $('html').scrollBottom(50)
        })
    </script>
    <div class="col-12">
        <h2 class="text-center">Bootstrap Varying Position</h2>
        <div class="container-fluid">
            <div class="row border border-danger bg-primary p-2 rounded bg-opacity-10 w-100">
                <div id="target" class="col-lg-3 m-0 col-sm-6 col-xs-8 text-start h1 p-5 bg-light border-start border-5 rounded-end-pill" style="color: purple;">Hello</div>
            </div>
        </div>
    </div>
</%def>

<%block name="content">
    <div class="container mt-4">
        <h1 class="text-end">Bootstrap Utilities.</h1>
        <div class="row p-2 rounded column-gap-1 row-gap-5 my-5" style="height: 20vh;">
            ${borders()}
            ${borders_widths()}
            ${backgrounds_colors()}
            ${backgrounds_colors_opacities()}
            ${text_colors_opacities()}
            ${varying_border()}
            <div class="col-12 p-3"></div>
        </div>
    </div>
</%block>