#include <iostream>
#include <sstream>
#include <string>

/*
You are given two non-empty linked lists
representing two non-negative integers.
The digits are stored in reverse order,
and each of their nodes contains a single
digit. Add the two numbers and return the
sum as a linked list.

You may assume the two numbers do not
contain any leading zero, except the
number 0 itself.

Definition for singly-linked list.
*/

struct ListNode {
  int val;
  ListNode *next;
  ListNode()
    : val(0), next(nullptr) { }
  ListNode(int x)
    : val(x), next(nullptr) { }
  ListNode(int x, ListNode *next)
    : val(x), next(next) { }
};


struct Solution {
  static ListNode *addTwoNumbers(ListNode *l1, ListNode *l2) {
    ListNode *result{ new ListNode() }, *_temp, *_p{ nullptr };
    _temp = result;
    do {
      addNodeValues(_temp, l1, l2);
      l1 = shiftNode(l1);
      l2 = shiftNode(l2);
      _p = _temp;
      _temp = shiftNode(_temp);
    } while (l1 != nullptr || l2 != nullptr);
    if (_temp->val == 0) {
      _p->next = nullptr;
      delete _temp;
    }
    return result;
  }
private:
  static ListNode *shiftNode(ListNode *list) {
    return (list == nullptr) ? list : list->next;
  }

  static void addNodeValues(ListNode *result, ListNode *l1, ListNode *l2) {
    int value{ 0 };
    if (l1 != nullptr && l2 != nullptr)
      value = l1->val + l2->val;
    else if (l1 != nullptr)
      value = l1->val;
    else if (l2 != nullptr)
      value = l2->val;
    value += result->val;
    int carry = (value - (value % 10)) / 10;
    int digit = (value > 9) ? value - carry * 10 : value;
    result->val = digit;
    result->next = new ListNode(carry);
  }
};

std::string print_list(ListNode *node) {
  std::stringstream str;
  str << '[';
  while (node != nullptr) {
    str << node->val;
    if (node->next != nullptr)
      str << ", ";
    node = node->next;
  }
  str << ']';
  return str.str();
}

std::ostream &operator<<(std::ostream &out, ListNode *node) {
  out << print_list(node);
  return out;
}

ListNode *getList(std::string const &number) {
  std::string digits{ "0123456789" };
  ListNode *result{ nullptr };
  for (char character : number) {
    if (digits.find(character) == std::string::npos)
      character = '0';
    result = new ListNode(character - '0', result);
  }
  return result;
}

void deleteList(ListNode *list) {
  ListNode *temp;
  while (list != nullptr) {
    temp = list;
    list = list->next;
    delete temp;
  }
}

auto main(int argc, char **argv) -> int {
  if (argc != 3) {
    std::cerr << "Usage:\n"
      << '\t' << argv[0] << " n_one n_two\n"
      << "where n_one and n_two are integers.\n"
      << "None integer values will be substituted for zeros.\n"
      << "Example: " << argv[0] << " 563 9767\n"
      << R"(
Output:
  Number1: [3, 6, 5]
  Number2: [7, 6, 7, 9]
  NumbSum: [0, 3, 3, 0, 1]
)";
    std::exit(1);
  }

  std::string sn1{ argv[1] }, sn2{ argv[2] };
  ListNode *number1 = getList(argv[1]);
  ListNode *number2 = getList(argv[2]);
  ListNode *numbsum = Solution::addTwoNumbers(number1, number2);

  std::cout << "Number1: " << number1 << '\n'
    << "Number2: " << number2 << '\n'
    << "NumbSum: " << numbsum << '\n';

  deleteList(number1);
  deleteList(number2);
  deleteList(numbsum);
}