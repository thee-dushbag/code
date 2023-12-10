#include <iostream>
#include <vector>
#include <span>
#include <algorithm>
#include "helpers.hpp"

struct ListNode {
  int val;
  ListNode *next;
  ListNode() : val(0), next(nullptr) { }
  ListNode(int x) : val(x), next(nullptr) { }
  ListNode(int x, ListNode *next) : val(x), next(next) { }
};

std::ostream &operator<<(std::ostream &out, ListNode *list) {
  out << '[';
  while (list) {
    out << list->val;
    // out << "{value:" << list->val << ", addr: " << std::addressof(list->val) << "}";
    list = list->next;
    if (list) out << ", ";
  }
  return out << ']';
}

struct Solution {
  static ListNode *mergeTwoLists(ListNode *list1, ListNode *list2) {
    ListNode sorted, *last{ &sorted }, **list;
    while (list1 and list2)
      *list = (last = (last->next = *(list = list1->val < list2->val ? &list1 : &list2)))->next;
    last->next = list1 ? list1 : list2;
    return sorted.next;
  }
};

ListNode *makelist(std::vector<int> const &ilist) {
  ListNode head, *last{ &head };
  for (int const &item : ilist)
    last = (last->next = new ListNode{ item });
  return head.next;
}

void deletelist(ListNode *list) {
  ListNode *first;
  while (list) {
    first = list;
    list = list->next;
    delete first;
  }
}

auto main(int argc, char **argv) -> int {
  if (argc < 2) {
    std::cerr << "Usage: " << argv[0] << " list1_size [list1...] [list2...]\n"
      << "Example: " << argv[0] << " 6 3 3 8 10 13 19 10 11 17 18 18 23 24 26"
      << R"(
Output:
  input1: [3, 3, 8, 10, 13, 19]
  input2: [10, 11, 17, 18, 18, 23, 24, 26]
  output: [3, 3, 8, 10, 10, 11, 13, 17, 18, 18, 19, 23, 24, 26]
)";
    std::exit(1);
  }

  const long index = std::min<long>(std::atol(argv[1]), argc - 2) + 2;
  std::vector<int> list1_vec, list2_vec;

  for (int i = 2; i < index; i++)
    list1_vec.push_back(std::atoi(argv[i]));

  for (int i = index; i < argc; i++)
    list2_vec.push_back(std::atoi(argv[i]));

  bool notsorted1{ not std::ranges::is_sorted(list1_vec) },
    notsorted2{ not std::ranges::is_sorted(list2_vec) };

  if (notsorted1 or notsorted2) {
    if (notsorted1) {
      std::cerr << "Sorting list1: " << list1_vec;
      std::ranges::sort(list1_vec);
      std::cerr << " to " << list1_vec << '\n';
    }
    if (notsorted2) {
      std::cerr << "Sorting list2: " << list2_vec;
      std::ranges::sort(list2_vec);
      std::cerr << " to " << list2_vec << '\n';
    }
    std::cerr << '\n';
  }

  ListNode *list1{ makelist(list1_vec) },
    *list2{ makelist(list2_vec) };

  std::cout << "input1: " << list1 << '\n'
    << "input2: " << list2 << '\n'
    << "output: " << (list1 = Solution::mergeTwoLists(list1, list2)) << '\n';

  deletelist(list1);
}
