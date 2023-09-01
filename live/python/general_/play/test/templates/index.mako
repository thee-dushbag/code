<%inherit file="base.mako"/>

<%block name="head_block">
    <title>HomePage</title>
</%block>

<%block name="body_block">
        <div class="row my-3 d-flex flex-column gap-3 align-items-center">
            <h1 class="col-12 display-3"><center><i>Line Site</i></center></h1>
            <div class="col-lg-8 col-md-10 col-xl-7 col-sm-12 col-xs-12 mb-5">
                <div class="project w-100 border container-fluid user-select-none">
                    <div class="row gap-2 p-2">
                        <div class="text-dark d-flex justify-content-center align-items-center display-5 p-2">
                            Add Liner
                        </div>
                        <div class="container-fluid border">
                            <div id="line-form" class="row gap-2 p-2">
                                <textarea class="col-12 display-sm p-2 border-none" name="content-input" id="" cols="30" rows="3"></textarea>
                                <button class="col-12 btn btn-outline-success" name="content-add">Add Line</button>
                            </div>
                        </div>
                        <div id="content" class="col-12 container-fluid">
                            <div class="gap-1" id="contents"></div>
                        </div>
                        <div class="col-12 border p-2">
                            <div class="btn btn-outline-success w-100" id="send-data">Send To Server</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</%block>
