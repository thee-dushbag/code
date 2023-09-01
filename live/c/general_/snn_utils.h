#ifndef __SNN_UTILS_H
#define __SNN_UTILS_H

#include <stdbool.h>

// typedef struct __safe_string_token_iterator
// {
//     snn_string str;
//     snn_string cur_token;
//     char __dlm;
//     size_t __last_index;
//     size_t __done;
// } snn_string_iterator;

// void snn_iterator_del(snn_string_iterator *__iter) {
//     snn_string_del(&__iter->str);
//     snn_string_del(&__iter->cur_token);
//     __iter->__last_index = 0;
//     __iter->__dlm = '\0';
//     __iter->__done = false;
// }

// bool snn_iterator_next(snn_string_iterator *__iter) {
//     if(__iter->__done) return true;
//     for(size_t i = __iter->__last_index; i < __iter->str.size; i++)
//         if((__iter->str.str[i] == __iter->__dlm) || (i == __iter->str.size - 1)) {
//             if(i == __iter->str.size - 1) __iter->__done = true;
//             snn_string_substr(&__iter->str, &__iter->cur_token, __iter->__last_index, i);
//             __iter->__last_index = i + 1;
//             break;
//         }
//     return __iter->__done;
// }

// void snn_iterator_init(snn_string_iterator *__iter, snn_string *__tkbuf, char dlm) {
//     snn_string_assign_init(&__iter->str, "");
//     snn_string_init(&__iter->cur_token, 0);
//     snn_string_substr(__tkbuf, &__iter->str, 0, __tkbuf->size);
//     __iter->__dlm = dlm;
//     __iter->__done = false;
//     __iter->__last_index = 0;
// }

void snn_reduce(void *__arr, size_t s, size_t __len, void *__res, void (*__func)(void *, void *, void *))
{
    if (__len == 1)
        return;
    __func(__arr, __arr + s, __res);
    for (size_t i = 2; i < __len; i++)
        __func(__arr + (s * i), __res, __res);
}

#endif //__SNN_UTILS_H