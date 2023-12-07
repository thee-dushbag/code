#ifndef __CODEPRACTICE_HEADER_
#define __CODEPRACTICE_HEADER_

#include <sstream>
#include <string>
#include <iostream>
#include <vector>

template <typename T>
std::string _tostr_vec(std::vector<T> const &vec) {
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

template<class T, class U>
std::ostream &operator<<(std::ostream &out, std::pair<T, U> const &pair) {
  return out << '{' << "first: " << pair.first << ", second: " << pair.second << '}';
}

template <typename T, typename U, template<typename...> typename M>
std::string _tostr_map(M<T, U> const &map) {
  std::stringstream str;
  std::size_t size{ map.size() }, counter{ 1 };
  str << '{';
  for (auto const &pair : map) {
    str << pair.first << ": " << pair.second;
    if (counter < size)
      str << ", ";
    counter++;
  }
  str << '}';
  return str.str();
}

template<class T>
std::ostream &operator<<(std::ostream &out, std::vector<T> const &vec) {
  return out << _tostr_vec(vec);
}

#ifdef _GLIBCXX_UNORDERED_MAP
template<class T, class U>
std::ostream &operator<<(std::ostream &out, std::unordered_map<T, U> const &map) {
  return out << _tostr_map<T, U, std::unordered_map>(map);
}
#endif

#ifdef _GLIBCXX_MAP
template<class T, class U>
std::ostream &operator<<(std::ostream &out, std::map<T, U> const &map) {
  return out << _tostr_map<T, U, std::map>(map);
}
#endif

#endif //__CODEPRACTICE_HEADER_