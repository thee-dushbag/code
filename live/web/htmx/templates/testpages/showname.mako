<div class="p-2 border position-relative rounded" id="greeting-${ID}">
  <p class="m-0">Hello <strong><em>${name}</em></strong>, how was your day?</p>
  <ion-icon
    class="position-absolute top-50 translate-middle end-0"
    name="close-outline"
    hx-swap="delete"
    hx-get="/test/deletename"
    hx-trigger="click"
    hx-target="#greeting-${ID}"
    ## hx-confirm="Are you sure?"
  >
  </ion-icon>
</div>