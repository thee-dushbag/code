#ifndef __SNN_LINKED_LIST_H_
#define __SNN_LINKED_LIST_H_

#include <stdlib.h>
#include <iso646.h>

#define CONCAT(ONE, TWO) ONE##TWO
#define XCONCAT(ONE, TWO) CONCAT(ONE, TWO)

#define LinkedListStructMaker(LinkedListStructName, LinkedListNodeType) \
    typedef struct XCONCAT(LinkedListStructName, LinkedListNodeType)    \
    {                                                                   \
        LinkedListNodeType *head;                                       \
        size_t node_count;                                              \
    } LinkedListStructName;

#define LinkedListNodeStructMaker(NodeStructName, NodeType)     \
    typedef struct XCONCAT(NodeStructName, NodeType)            \
    {                                                           \
        struct XCONCAT(NodeStructName, NodeType) * next, *prev; \
        NodeType data;                                          \
    } NodeStructName;

#define LinkedListInit(FuncName, LinkedListStructName) \
    void FuncName(LinkedListStructName *lptr)          \
    {                                                  \
        lptr->head = NULL;                             \
        lptr->node_count = 0;                          \
    }

#define LinkedListPushBack(FuncName, LinkedListStructName, NodeStructName) \
    void FuncName(LinkedListStructName *lptr, NodeStructName *node)        \
    {                                                                      \
        if (lptr->head)                                                    \
        {                                                                  \
            NodeStructName *tmp = lptr->head;                              \
            while (tmp->next)                                              \
                tmp = tmp->next;                                           \
            tmp->next = node;                                              \
            node->prev = tmp;                                              \
            node->next = NULL;                                             \
            tmp = tmp;                                                     \
        }                                                                  \
        else                                                               \
        {                                                                  \
            lptr->head = node;                                             \
            node->next = NULL;                                             \
            node->prev = NULL;                                             \
        }                                                                  \
        lptr->node_count++;                                                \
    }

#define LinkedListPushFront(FuncName, LinkedListStructName, NodeStructName) \
    void FuncName(LinkedListStructName *lptr, NodeStructName *node)         \
    {                                                                       \
        NodeStructName *tmp = lptr->head;                                   \
        if (lptr->head)                                                     \
            lptr->head->prev = node;                                        \
        lptr->head = node;                                                  \
        node->next = tmp;                                                   \
        node->prev = NULL;                                                  \
        lptr->node_count++;                                                 \
    }

#define LinkedListPopBack(FuncName, LinkedListStructName, NodeStructName) \
    NodeStructName *FuncName(LinkedListStructName *lptr)                  \
    {                                                                     \
        if (not lptr->head)                                               \
            return NULL;                                                  \
        NodeStructName *tmp = lptr->head;                                 \
        if (not lptr->head->next)                                         \
        {                                                                 \
            lptr->head = NULL;                                            \
            return tmp;                                                   \
        }                                                                 \
        while (tmp->next)                                                 \
            tmp = tmp->next;                                              \
        tmp->prev->next = NULL;                                           \
        tmp->next = NULL;                                                 \
        tmp->prev = NULL;                                                 \
        lptr->node_count--;                                               \
        return tmp;                                                       \
    }
    
#define LinkedListPopFront(FuncName, LinkedListStructName, NodeStructName) \
    NodeStructName *FuncName(LinkedListStructName *lptr)                   \
    {                                                                      \
        if (not lptr->head)                                                \
            return NULL;                                                   \
        NodeStructName *tmp = lptr->head;                                  \
        if (not lptr->head->next)                                          \
        {                                                                  \
            lptr->head = NULL;                                             \
            return tmp;                                                    \
        }                                                                  \
        lptr->head = lptr->head->next;                                     \
        lptr->head->prev = NULL;                                           \
        tmp->next = NULL;                                                  \
        tmp->prev = NULL;                                                  \
        lptr->node_count--;                                                \
        return tmp;                                                        \
    }

#define LinkedListMakeNode(FuncName, LinkedListStructName, NodeStructName, NodeType) \
    NodeStructName *FuncName(NodeType data)                                          \
    {                                                                                \
        NodeStructName *node = (NodeStructName *)malloc(sizeof(NodeStructName));     \
        node->data = data;                                                           \
        node->next = NULL;                                                           \
        node->prev = NULL;                                                           \
        return node;                                                                 \
    }

#define LinkedListDel(FuncName, LinkedListStructName, NodeStructName, PopFuncName) \
    void FuncName(LinkedListStructName *lptr)                                      \
    {                                                                              \
        while (lptr->head)                                                         \
            free(PopFuncName(lptr));                                               \
    }

#define LinkedListView(FuncName, LinkedListStructName, NodeStructName, ViewLine) \
    void FuncName(LinkedListStructName *lptr)                                    \
    {                                                                            \
        NodeStructName *tmp = lptr->head;                                        \
        printf("printing linked list:\n");                                       \
        while (tmp)                                                              \
        {                                                                        \
            ViewLine;                                                            \
            tmp = tmp->next;                                                     \
        }                                                                        \
    }

#define GLOBAL_PREFIX snn_linked_list
#define LINKED_LIST_DEF GLOBAL_PREFIX
#define LINKED_LIST_DEL_DEF XCONCAT(GLOBAL_PREFIX, _del)
#define LINKED_LIST_POP_BACK_DEF XCONCAT(GLOBAL_PREFIX, _pop_back)
#define LINKED_LIST_POP_FRONT_DEF XCONCAT(GLOBAL_PREFIX, _pop_front)
#define LINKED_LIST_PUSH_FRONT_DEF XCONCAT(GLOBAL_PREFIX, _push_front)
#define LINKED_LIST_PUSH_BACK_DEF XCONCAT(GLOBAL_PREFIX, _push_back)
#define LINKED_LIST_MAKE_NODE_DEF XCONCAT(GLOBAL_PREFIX, _make_node)
#define LINKED_LIST_INIT XCONCAT(GLOBAL_PREFIX, _init)
#define LINKED_LIST_NODE_DEF XCONCAT(GLOBAL_PREFIX, _node)
#define LINKED_LIST_VIEW_DEF XCONCAT(GLOBAL_PREFIX, _view)
#define LINKED_LIST_VIEW_LINE(PHolder) printf("Data: " #PHolder " | prev: %14p | cur: %14p | next: %14p |\n", tmp->data, tmp->prev, tmp, tmp->next);

#define LinkedListMaker(Suffix, Type, ViewLine)                                                                                                                               \
    LinkedListNodeStructMaker(XCONCAT(LINKED_LIST_NODE_DEF, Suffix), Type)                                                                                                    \
        LinkedListStructMaker(XCONCAT(LINKED_LIST_DEF, Suffix), XCONCAT(LINKED_LIST_NODE_DEF, Suffix))                                                                        \
            LinkedListInit(XCONCAT(LINKED_LIST_INIT, Suffix), XCONCAT(LINKED_LIST_DEF, Suffix))                                                                               \
                LinkedListPopFront(XCONCAT(LINKED_LIST_POP_FRONT_DEF, Suffix), XCONCAT(LINKED_LIST_DEF, Suffix), XCONCAT(LINKED_LIST_NODE_DEF, Suffix))                       \
                    LinkedListPopBack(XCONCAT(LINKED_LIST_POP_BACK_DEF, Suffix), XCONCAT(LINKED_LIST_DEF, Suffix), XCONCAT(LINKED_LIST_NODE_DEF, Suffix))                     \
                        LinkedListPushFront(XCONCAT(LINKED_LIST_PUSH_FRONT_DEF, Suffix), XCONCAT(LINKED_LIST_DEF, Suffix), XCONCAT(LINKED_LIST_NODE_DEF, Suffix))             \
                            LinkedListPushBack(XCONCAT(LINKED_LIST_PUSH_BACK_DEF, Suffix), XCONCAT(LINKED_LIST_DEF, Suffix), XCONCAT(LINKED_LIST_NODE_DEF, Suffix))           \
                                LinkedListMakeNode(XCONCAT(LINKED_LIST_MAKE_NODE_DEF, Suffix), XCONCAT(LINKED_LIST_DEF, Suffix), XCONCAT(LINKED_LIST_NODE_DEF, Suffix), Type) \
                                    LinkedListView(XCONCAT(LINKED_LIST_VIEW_DEF, Suffix), XCONCAT(LINKED_LIST_DEF, Suffix), XCONCAT(LINKED_LIST_NODE_DEF, Suffix), ViewLine)  \
                                        LinkedListDel(XCONCAT(LINKED_LIST_DEL_DEF, Suffix), XCONCAT(LINKED_LIST_DEF, Suffix), XCONCAT(LINKED_LIST_NODE_DEF, Suffix), XCONCAT(LINKED_LIST_POP_BACK_DEF, Suffix))

#endif //__SNN_LINKED_LIST_H_