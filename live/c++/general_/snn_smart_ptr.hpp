#ifndef __SNN_SMART_PTR_HPP_
#define __SNN_SMART_PTR_HPP_
#include <ostream>
#include <exception>

namespace snn {
    class myexcept: public std::exception {
        const char *data;
    public:
        myexcept(const char *data):data{data} {}
        const char *what() const noexcept {
            return data;
        }
    };

    template<typename T>
    class smart_ptr {
        T *__ptr;
    public:
        T *operator->() { return &this->data(); }
        smart_ptr(): __ptr{nullptr} {}
        smart_ptr(T val): __ptr{new T{val}} {}
        smart_ptr(smart_ptr const &smptr): __ptr{nullptr} {
            if(smptr.__ptr)
                __ptr = new T{*smptr.__ptr};
        }
        smart_ptr(smart_ptr &&smptr): __ptr{smptr.__ptr} {
            smptr.__ptr = nullptr;
        }
        void operator=(smart_ptr &&smptr) {
            this->forget();
            __ptr = smptr.__ptr;
            smptr.__ptr = nullptr;
        }
        void operator=(smart_ptr const &smptr) {
            if(smptr.__ptr) {
                if(__ptr) *__ptr = *(smptr.__ptr);
                else __ptr = new T{*(smptr.__ptr)};
            } else this->forget();
        }
        void forget() { if(__ptr) { delete __ptr; __ptr = nullptr; } }
        ~smart_ptr() { this->forget(); }
        operator bool() const noexcept { return __ptr; }
        T &data() { if(__ptr) return *__ptr; throw myexcept("Dereferencing nullptr."); }
        T const &data() const { if(__ptr) return *__ptr; throw myexcept("Dereferencing nullptr."); }
        T &operator*() { this->data(); }
        T const &operator*() const { this->data(); }
        friend std::ostream &operator<<(std::ostream &out, smart_ptr const &smptr) {
            out << "<smptr(";
            if(smptr.__ptr) out << *(smptr.__ptr);
            else out << "NULL";
            out << ")>";
            return out;
        }
    };
}

#endif //__SNN_SMART_PTR_HPP_