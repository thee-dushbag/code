#pragma once
#include <cstddef>
#include <cstring>
#include <iostream>

using std::cout;

class string {
  char *payload;
  std::size_t length;

public:
  string(): payload(nullptr), length() { std::cout << "Default\n"; }
  string(string const &str): payload(new char[str.length]), length(str.length) {
    std::cout << "Copied\n";
    std::memcpy(payload, str.payload, length);
  }
  string(string &&str): payload(str.payload), length(str.length) {
    std::cout << "Moved\n";
    str.payload = nullptr;
    str.length = 0;
  }
  string(const char *c_str)
    : payload(new char[std::strlen(c_str)]), length(std::strlen(c_str)) {
    std::cout << "Construct: const char[" << length << "]\n";
    std::memcpy(payload, c_str, length);
  }
  string(char filler, std::size_t length)
    : payload(new char[length]), length(length) {
    std::cout << "Construct: char * length\n";
    std::memset(payload, filler, length);
  }
  template <std::size_t length>
  string(char (&char_arr)[length]): payload(new char[length]), length(length) {
    std::cout << "Construct: char[length]\n";
    std::memcpy(payload, char_arr, length);
  }
  string &operator=(string &&str) {
    if(this == &str)
      return *this;
    payload = str.payload;
    length = str.length;
    str.payload = nullptr;
    str.length = 0;
    return *this;
  }
  string &operator=(string const &str) {
    payload = str.payload;
    length = str.length;
    return *this;
  }
  string &operator=(const char *str) {
    this->~string();
    length = std::strlen(str);
    payload = new char[length];
    std::memcpy(payload, str, length);
    return *this;
  }
  template <std::size_t len>
  string &operator=(char (&str)[len]) {
    this->~string();
    payload = new char[len];
    length = len;
    std::memcpy(payload, str, len);
    return *this;
  }
  std::size_t size() const { return length; }
  char *data() { return payload; }
  const char *data() const { return payload; }
  std::string_view view() const { return *this; }
  operator std::string_view() const { return {payload, length}; }

  ~string() {
    if(payload) {
      cout << "Freed: payload\n";
      delete[] payload;
    } else
      cout << "Freed\n";
    payload = nullptr;
    length = 0;
  }
  friend std::ostream &operator<<(std::ostream &out, string const &s) {
    return out.write(s.payload, s.length);
  }
};
