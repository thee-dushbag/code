<%inherit file="base.mako"/>

<%block name="title">
    Button Page
</%block>

<%block name="content">
<%
colors = 'primary', 'secondary', 'success', 'warning', 'danger', 'info', 'light', 'dark'
sizes = 'xs', 'sm', 'md', 'lg', 'xl', 'xxl'
%>
    <div class="container">
        <div class="my-5">
            <h2>Basic Bootstrap Buttons</h2>
            <div class="d-flex justify-content-around">
                % for color in colors:
                    <button class="btn btn-${color}">Button ${color.title()}</button>
                % endfor
            </div>
        </div>
        <div class="my-5">
            <h2>Basic Bootstrap Outline Buttons</h2>
            <div class="d-flex justify-content-around">
                % for color in colors:
                    <button class="btn btn-outline-${color} ${'text-black' if color == 'light' else ''}">
                        Button ${color.title()}
                    </button>
                % endfor
            </div>
        </div>
        <div class="my-5">
            <h2>Basic Bootstrap Button Sizes</h2>
            <div class="d-flex justify-content-around">
                % for size in sizes:
                    <button class="btn btn-primary btn-${size}">Button ${size.upper()}</button>
                % endfor
            </div>
        </div>
        <div class="my-5">
            <h2>Basic Button Options</h2>
            <div class="d-flex justify-content-around">
                <button class="btn btn-primary" disabled>Button Disabled</button>
            </div>
        </div>
    </div>
</%block>