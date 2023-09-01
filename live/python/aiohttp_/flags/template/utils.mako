<%def name="input_field(label, name, type)">
    <input type="${type}" id="${name}" name="${name}" class="p-2 w-100" placeholder="${label}">
</%def>

<%def name="checked_input(label, name, value=None)">
    <div class="w-100 p-2">
        <input ${'checked' if value else ''} value="on" type="checkbox" name="${name}" id="${name}">
        <label for="${name}">${label}</label>
    </div>
</%def>

<%def name="form_block(dest, method, submit, inputs, field=None, home = '/', home_lbl = 'Home')">
    <form action="${dest}" method="post">
        <div class="d-flex gap-2 flex-column justify-content-center align-items-center">
        % for _input in inputs:
            ${(field or input_field)(*_input)}
        % endfor
            <input type="submit" value="${submit}" class="btn btn-primary w-100">
            % if home:
                <a href="${home}" class="btn btn-primary w-100">${home_lbl}</a>
            % endif
        </div>
    </form>
</%def>