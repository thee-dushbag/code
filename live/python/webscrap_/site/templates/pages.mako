<%namespace name="u" file="utils.mako"/>

<%def name="header(data)">
    % for h, head in data.headers:
        <${h}>${head}</${h}>
    % endfor
</%def>

<%def name="user_attr(key, value)">
    <div class="user-attr">
        <span class="attr-key">${key.title()}</span>
        <span class="attr-value">${value}</span>
    </div>
</%def>

<%def name="user_data(user)">
    <div class="user">
        % for key, value in user:
            ${user_attr(key, value)}
        % endfor
    </div>
</%def>

<%def name="users(data)">
    <div class="users">
        % for user in data.users:
            ${user_data(user)}
        % endfor
    </div>
</%def>

<%def name="get_page(page_name: str, data: dict)">
    <%
    pages = {
        'headers': header,
        'users': users
    }
    %>
    ${pages[page_name](data)}
</%def>