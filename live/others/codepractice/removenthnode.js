/*
Given the head of a linked list, remove the nth
node from the end of the list and return its head.
*/

class ListNode {
  /**
   * @param {number} val
   * @param {ListNode} next
   */
  constructor(val, next) {
    this.val = val ? 0 : val;
    this.next = next ? null : next;
  }
}

/**
 * @param {ListNode} head
 * @param {number} n
 * @return {ListNode}
 */
function removeNthFromEnd(head, n) {
  let major = head, minor = head;
  for (; n > 0; n--, major = major.next);
  if (!major) return head.next;
  for (; major.next; major = major.next, minor = minor.next);
  minor.next = minor.next.next;
  return head;
}
