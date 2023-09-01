<%inherit file="base.mako"/>

<%def name="basic_alerts()">
<%
def colors():
    return ['danger', 'secondary', 'dark', 'light', 'success', 'primary', 'info', 'warning']
%>
    <div class="col-lg-auto col-xl-auto col-sm-12 col-md-6 col-xs-12">
        <h1 class="lead"><em>Basic Coloured Alerts</em></h1>
        <div class="container">
            <div class="row p-2 gap-2 border d-flex justify-content-center">
                % for color in colors():
                    <div role="alert" class="col-lg-auto col-xl-auto m-0 col-md-6 col-sm-12 col-xs-12 alert alert-${color}">
                        This is ${color} alert.
                    </div>
                % endfor
            </div>
        </div>
    </div>
</%def>

<%def name="dismissible_alerts()">
<%
def colors():
    return ['danger', 'secondary', 'dark', 'light', 'success', 'primary', 'info', 'warning']
%>
    <div class="col-lg-auto col-xl-auto col-sm-12 col-md-6 col-xs-12">
        <h1 class="lead"><em>Dismissible Coloured Alerts</em></h1>
        <div class="container">
            <div class="row p-2 gap-2 border d-flex justify-content-center">
                % for color in colors():
                    <div role="alert" class="fade show alert-dismissible col-lg-auto col-xl-auto m-0 col-md-6 col-sm-12 col-xs-12 alert alert-${color}">
                        This is ${color} alert.
                        <button type="button" class="btn-class" data-bs-dismissible="alert" aria-label="close">x</button>
                    </div>
                % endfor
            </div>
        </div>
    </div>
</%def>


<%block name="content">
    <div class="container">
        <h1 class="mt-5 mb-3 text-end"><u>Bootstrap Alerts</u></h1>
        <hr>
        <div class="row p-2 gap-2">
            ${basic_alerts()}
            ${dismissible_alerts()}
        </div>
    </div>
</%block>