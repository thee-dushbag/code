struct Database
{
    const char *name;
};


void db_connect(struct Database *db, const char *username, const char *passwd)
{
    size_t len = strlen(passwd);
    char stars[len + 1];
    stars[len] = '\0';
    for (int i = 0; i < len; i++)
        stars[i] = '*';
    printf("Connecting to database: %s with auth: (name='%s', passwd='%s')\n", db->name, username, stars);
}

void env(void)
{
    struct Database mydb;
    mydb.name = "sqlite:///home/simon/Desktop/students.db";
    const char *username = getenv("USERNAME");
    const char *passwd = getenv("PASSWORD");
    if (username && passwd)
        db_connect(&mydb, username, passwd);
    else
    {
        printf("Connection Error: auth: (name='%s', passwd='%s')\n", username, passwd);
        exit(2);
    }
    printf("Databases successfully connected.\n");
}

struct vector
{
    int x, y, z;
};

void set_vec_value(struct vector *vec, int x, int y, int z)
{
    vec->x = x;
    vec->y = y;
    vec->z = z;
}

void snn_vector_view(struct vector *vec)
{
    printf("<vector(x=%d, y=%d, z=%d)>\n", vec->x, vec->y, vec->z);
}

#include <linked_list.h>

typedef struct vector __vector;
LinkedListMaker(_vec, __vector, snn_vector_view(&(tmp->data)));
LinkedListMaker(_i, int, LINKED_LIST_VIEW_LINE(%d));
typedef int *iptr;
LinkedListMaker(_ip, iptr, printf("Value: %d\n", *(tmp->data)));

int counter = 1000;
iptr allocate()
{
    int *mem = (int *)malloc(sizeof(int));
    *mem = counter;
    printf("Allocated memory for: counter: %d at addr: %p\n", counter, mem);
    counter++;
    return mem;
}

void deallocate(iptr data)
{
    printf("Deallocating memory: %p with value: %d\n", data, *data);
    free(data);
}

void test2(void)
{
    snn_linked_list_ip list;
    snn_linked_list_init_ip(&list);
    for (int i = 0; i < 10; i++)
        snn_linked_list_push_back_ip(&list, snn_linked_list_make_node_ip(allocate()));
    snn_linked_list_view_ip(&list);
    snn_linked_list_node_ip *node = list.head;
    while (node)
    {
        deallocate(node->data);
        node = node->next;
    }
    snn_linked_list_del_ip(&list);
}

void test()
{
    snn_linked_list_i list;
    snn_linked_list_vec vlist;
    struct vector tvec;
    snn_linked_list_init_i(&list);
    snn_linked_list_init_vec(&vlist);
    int data[][3] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27};
    for (int i = 0; i < 9; i++)
    {
        set_vec_value(&tvec, data[i][0], data[i][1], data[i][2]);
        snn_linked_list_push_back_i(&list, snn_linked_list_make_node_i(data[i][0]));
        snn_linked_list_push_back_vec(&vlist, snn_linked_list_make_node_vec(tvec));
    }
    snn_linked_list_view_i(&list);
    snn_linked_list_del_i(&list);
    snn_linked_list_view_vec(&vlist);
    snn_linked_list_del_vec(&vlist);
}