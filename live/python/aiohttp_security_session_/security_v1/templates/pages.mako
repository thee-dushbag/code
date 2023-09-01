<%namespace name="u" file="utils.mako"/>

<%def name="home(data: dict)">
    <form action="${data.url('say_hi')}" method="get">
        <label for="NAME">Name</label>
        <input type="text" name="name" id="NAME">
        <input type="submit" value="Greet">
    </form>
</%def>

<%def name="say_hi(data: dict)">
    <%
    from time import sleep
    n = 3
    print(f"{data.name} is waiting to be greeted after {n} seconds.")
    sleep(n)
    %>
    <div id="greeting">
        Hello ${data.name.title()}, how was your day?<br>
    </div>
    <a href="${data.url('index')}">Home</a>
</%def>

<%def name="get_page(page_name: str, data: dict)">
    <%
    pages = {
        'home': home,
        'say_hi': say_hi
    }
    %>
    ${pages[page_name](data)}
</%def>