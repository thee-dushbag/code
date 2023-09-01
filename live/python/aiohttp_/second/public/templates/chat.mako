<%inherit file="base.mako"/>

<%def name="formblock()">
    <div class="col-12 h-100 d-flex flex-column justify-content-around">
        <input id="message_input" class="bg-transparent text-white border-bottom border w-100 p-3 rounded"/>
        <button id="send_message" class="btn btn-primary w-100">Send</button>
    </div>
</%def>

<%def name="message_block(msg)">
    <figure class="p-2 border-start border-success border-1 border-bottom rounded">
        <p class="lead text-start">${msg.message}</p>
        <blockquote class="text-end"><small><em>@${msg.sender.lower()}</em></small></blockquote>
    </figure>
</%def>

<%def name="display_messages(messages: list)">
    <div class="col-12 h-100">
        <div style="height: 5%;" class="text-end"><small><em>Messages</em></small></div>
        <div id="messages" style="height: 92%;" class="p-2 row-gap-2 overflow-y-scroll border-1 rounded">
            % for msg in messages:
                ${message_block(msg)}
            % endfor
        </div>
    </div>
</%def>

<%block name="content">
    <div class="container">
        <div class="row vh-100 d-flex justify-content-center align-items-center">
            <div class="col-lg-8 col-xl-7 col-md-9 col-sm-12 col-xs-12 items-center" style="height: 90%;">
                <div id="message_app" class="bg-dark body-success h-100">
                    <div class="container-fluid h-100">
                        <div class="row h-100">
                            <div style="height: 7%;" class="col-12">
                                <h1 class="text-center"><u>Chat App</u></h1>
                            </div>
                            <div style="height: 75%;" class="col-12">
                                ${display_messages(messages)}
                            </div>
                            <div style="height: 18%;" class="col-12">
                                ${formblock()}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</%block>