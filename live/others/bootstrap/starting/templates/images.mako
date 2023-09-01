<%inherit file="base.mako" />

<%def name="imageurl()">http://192.168.0.100:9944/image</%def>

<%def name="images()">
    <div class="col">
        <div class="h1">Bootstrap classes</div>
        <div>
            <div class="bg-dark m-2" style="width: 128px; height: 128px; border: 5px solid purple;">
                <img src="${imageurl()}?width=512&height=256" alt="" class="img-fluid">
            </div>
            <div class="m-2">
                <img src="${imageurl()}" class="img-thumbnail" alt="">
            </div>
            <div class="bg-success d-flex container-fluid rounded">
                <div class="row p-1 gap-1">
                    <div class="col-12">
                        <img style="width: 256px;" src="${imageurl()}?flat=i" class="img-fluid"/>
                        <img style="width: 256px;" src="${imageurl()}?flat=k" class="float-end img-fluid"/>
                    </div>
                </div>
                <div class="row">
                    <img src="${imageurl()}?flat=9" class="float-end" alt="">
                </div>
            </div>
        </div>
    </div>
</%def>

<%block name="content">
    <div class="container my-3 user-select-none mb-5">
        <h1 class="text-underline">
            <center>Bootstrap Images</center>
        </h1>
        <div class="row row-gap-5 my-3">
            ${images()}
        </div>
    </div>
</%block>