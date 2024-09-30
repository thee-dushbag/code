#include <stdio.h>
#include <app.h>

int main(int argc, char **argv) {
  struct app_t objs[3];
  app_init(objs + 0,
      "Simon Nganga Njoroge",
      "simongash@gmail.com",
      "Google Inc"
    );
  app_init(objs + 1,
      "Faith Njeri Wanjiru",
      "faithnjeri@yahoo.com",
      "Facebook"
    );
  app_init(objs + 2,
      "Lydia Wanjiru Njeri",
      "lydiawanjiru@outlook.mil",
      "Twitter"
    );
  app_print(objs + 0);
  app_print(objs + 1);
  app_print(objs + 2);
}

