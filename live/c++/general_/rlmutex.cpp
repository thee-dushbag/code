#include <iostream>
#include <vector>
#include <mutex>

using mutex_lock = std::recursive_mutex;

struct IntListThreadsafe {
  std::vector<int> _int_list;
  mutex_lock _lock;

  IntListThreadsafe() = delete;
  IntListThreadsafe(std::vector<int> const &vec)
  : _int_list { vec }, _lock { } { }
  IntListThreadsafe(std::vector<int> &&vec)
  : _int_list { std::move(vec) }, _lock { } { }

  std::vector<int> indices_of(int to_find) {
    std::lock_guard _{ _lock };
    std::vector<int> found_indices;
    int index { 0 };
    auto iter { _int_list.cbegin() };
    for (; iter != _int_list.cend(); ++iter, ++index)
      if (*iter == to_find) found_indices.push_back(index);
    return found_indices;
  }

  void find_and_replace(int to_replace, int replace_with) {
    std::lock_guard _ { _lock };
    for(int index: indices_of(to_replace))
        _int_list[index] = replace_with;
  }
};

template <typename T>
std::ostream &operator<<(std::ostream &out, std::vector<T> const &vec) {
  out << '[';
  auto iter = vec.cbegin();
  std::size_t index { 0 }, last_index { vec.size() - 1 };
  for (; iter != vec.cend(); ++iter, ++index)
    out << *iter << ((index < last_index)? ", ": "");
  return out << ']';
}

auto main(int argc, char **argv) -> int {
  IntListThreadsafe ilt {{ 1, 2, 1, 2, 1 }};
  std::cout << "Input list: " << ilt._int_list << '\n';
  ilt.find_and_replace(1, 2);
  std::cout << "Output list: " << ilt._int_list << '\n';
}
