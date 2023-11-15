#ifndef __CODEPRACTICE_HEADER_
#define __CODEPRACTICE_HEADER_

#include <sstream>
#include <string>
#include <iostream>
#include <vector>

template <typename T>
std::string _tostr_vec(std::vector<T> const& vec) {
  std::stringstream str;
  std::size_t size{ vec.size() };
  str << '[';
  for (uint i = 0; i < size; i++) {
    str << vec[i];
    if (i + 1 < size)
      str << ", ";
  }
  str << ']';
  return str.str();
};

template<class T>
std::ostream& operator<<(std::ostream& out, std::vector<T> const& vec)
{ return out << _tostr_vec(vec); }


#endif //__CODEPRACTICE_HEADER_