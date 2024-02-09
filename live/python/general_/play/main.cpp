#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <thread>
#include <coroutine>
#include <future>
#include <list>
#include <mutex>
using namespace std::chrono_literals;
std::mutex gmut;
auto sleep_time = 2s;

template<typename ...T>
void print(const T&...ts) {
  struct Lock {
    Lock() { gmut.lock(); }
    ~Lock() { gmut.unlock(); }
  } _;
  (std::cout << ... << ts) << '\n';
}

std::vector<std::string> split(std::string str, char sep) {
  std::string substring;
  std::vector<std::string> container;    
  for (char c : str) {
    if (c == sep) {
      container.push_back(substring);
      substring = "";
    } else
      substring.push_back(c);
  }
  if (substring.length() > 0)
    container.push_back(substring);
  return container;
}

std::string join(std::vector<std::string> const &words, char sep) {
  std::string container;
  for (std::string const &word: words) {
    container += word;
    container.push_back(sep);
  }
  container.pop_back();
  return container;
}

std::string title(std::string const &str) {
  auto words = split(str, ' ');
  for (std::string& word: words)
    word[0] = std::toupper(word[0]);
  return join(words, ' ');
}

void say_hi(std::string const &name) {
  auto i = std::this_thread::get_id();
  print("[ ", i, " ]: ", "Hello ", name, ", how was your day?");
  std::this_thread::sleep_for(sleep_time);
}

void say_hi_to(int size, char **names) {
  std::list<std::future<void>> futs;
  for (int i = 0; i < size; i++)
    futs.push_back(std::async(std::launch::async, say_hi, title(names[i])));
}

auto main(int argc, char **argv) -> int {
  std::string sync{"sync"}, async{"async"};
  if (argc <= 2)
    print("Please Enter names on the CommandLine.");
  else if (std::string(argv[1]) == sync)
    for (int i = 2; i < argc; i++)
      say_hi(title(argv[i]));
  else if (std::string(argv[1]) == async)
    say_hi_to(argc - 2, argv + 2);
  else
    print("Unknown option '", argv[1], '\'');
}
