#ifndef _SNN_ALLOCATOR_OPERATOR_OVERLOADS_
#define _SNN_ALLOCATOR_OPERATOR_OVERLOADS_

#include <iostream>
#include <cstdlib>

void* operator new(size_t size) {
    void* addr = malloc(size);
    std::cout << "[Type]: Allocating: size=" << size << "bytes addr='" << addr << "'\n";
    return addr;
}
void operator delete(void* ptr) {
    std::cout << "[Type]: Deallocating: addr='" << ptr << "'\n";
    free(ptr);
}
void* operator new[](size_t size) {
    void* addr = malloc(size);
    std::cout << "[Array]: Allocating: size=" << size << "bytes addr='" << addr << "'\n";
    return addr;
}
void operator delete[](void* ptr) {
    std::cout << "[Array]: Deallocating: addr='" << ptr << "'\n";
    free(ptr);
}

#endif //_SNN_ALLOCATOR_OPERATOR_OVERLOADS_