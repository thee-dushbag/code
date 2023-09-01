<%inherit file="base.mako"/>

<%block name="content">
    <div id="main" class="border rounded p-2">
        <form action="/recv_text" method="post" class="border p-3 rounded d-flex gap-2">
            <input type="text" name="msg" id="text_field" placeholder="Enter Some Text HERE"/>
            <input type="submit" id="send_btn" class="btn btn-primary btn-sm" value="Send Text"/>
        </form>
        <div class="messages p-3 border rounded">
            % for msg in msgs:
                <div class="message p-2 m-2 border rounded">${msg}</div>
            % endfor
        </div>
    </div>
</%block>
