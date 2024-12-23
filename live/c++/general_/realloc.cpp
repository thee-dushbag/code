#include <cstring>
#define LOG_SNN_DATA
#include <snn_data.hpp>
#include <iostream>
#include <vector>

using data_t = snn::utils::data<int>;

/* C++                            C
 * new                            malloc
 * new[]                          calloc
 * delete                         free
 * delete[]                       free
 * std::vector::{reserve,resize}  realloc
 *
 * The main difference is that C++ is aware of object
 * constructors and destructors which C lacks, this means
 * C's allocs dont initialize the objects on allocation.
 * std::vector calls the destructor on popped items and 
 * constructor on pushed items, this goes very nicely with
 * realloc-kind of functionality.
 */

#ifndef NODEF
# define USE_REALLOC
# define PRINT true
#endif

template<typename T>
struct vector {
  vector(): payload(nullptr), cnt(0), cap(0) {}
  vector(unsigned reserve):
    payload(static_cast<T*>(std::malloc(sizeof(T) * reserve))),
    cnt(0), cap(reserve) {}
  void push_back(T const &t) {
    grow();
    new (payload + cnt++) T(t);
  }
  template<typename ...args_t>
  void emplace_back(args_t &&...args) {
    grow();
    new (payload + cnt++) T(std::forward<args_t>(args)...);
  }
  T &at(unsigned pos) const {
    if(pos < cnt) return payload[pos];
    throw "Invalid Pos";
  }
  void pop_at(unsigned pos) {
    if (pos < cnt) {
      payload[pos].~T();
      std::memcpy(payload + pos, payload + pos + 1, cnt - pos - 1);
      cnt--;
    } else throw "Invalid Pos";
  }
  void pop_at(unsigned start, unsigned end) {
    if (start < end and end <= cnt) {
      unsigned const count = end - start;
      for (unsigned idx = start; idx < end; idx++)
        payload[idx].~T();
      std::memcpy(payload + start, payload + start + count, cnt - start - count);
      cnt -= count;
    } else throw "Invalid Range";
  }
  void pop_back() {
    if(cnt) payload[--cnt].~T();
    throw "Empty";
  }
  ~vector() {
    for(unsigned idx = 0; idx < cnt; idx++)
      payload[idx].~T();
    if(payload) std::free(payload);
    payload = nullptr;
    cnt = cap = 0;
  }
  unsigned capacity() const { return cap; }
  unsigned size() const { return cnt; }
private:
  void grow() {
    if (cnt != cap) return;
    cap = cap ? cap * 2 : 5;
#ifdef USE_REALLOC
    T* npayload = static_cast<T*>(std::realloc(payload, sizeof(T) * cap));
    if (npayload != payload) {
#else
    T* npayload = static_cast<T*>(std::malloc(sizeof(T) * cap));
#endif
      for (unsigned idx = 0; idx < cnt; idx++) {
        new (npayload + idx) T(std::move(payload[idx]));
        payload[idx].~T();
      }
      if(payload) std::free(payload);
      payload = npayload;
#ifdef USE_REALLOC
    } else if (PRINT) std::cout << "ReallocSaved\n";
#endif
  }
  T *payload;
  unsigned cnt, cap;
};

int main() {
  vector<data_t> values(1);
  for(int idx = 0, value = 1; idx < 100; idx++, value *= 2) {
    values.emplace_back(value);
  }
  values.pop_at(10, 20);
  std::cout << values.size() << ' ' << values.capacity() << '\n';
}

