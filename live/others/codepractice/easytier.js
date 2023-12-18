/**
 * @param {number[]} nums1
 * @param {number} m
 * @param {number[]} nums2
 * @param {number} n
 * @return {void} Do not return anything, modify nums1 in-place instead.
 */
function merge(nums1, m, nums2, n) {
  nums1.splice(m);
  nums2.splice(n);
  while (m > 0 && n > 0)
    if (nums1[0] <= nums2[0]) {
      nums1.push(nums1.shift());
      m--;
    } else {
      nums1.push(nums2.shift());
      n--;
    }
  nums1.push(...nums1.slice(0, m));
  nums1.splice(0, m);
  nums1.push(...nums2);
}
