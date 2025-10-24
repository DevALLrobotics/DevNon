# Problem: Sum of Unique Elements

## Description
Given a list of integers, return the sum of all unique elements (those that appear exactly once).

## Function Signature
```python
def sumOfUnique(nums: list[int]) -> int:
```

## Examples

| Input       | Output |
| ----------- | ------ |
| [1,2,3,2]   | 4      |
| [1,1,1,1]   | 0      |
| [1,2,3,4,5] | 15     |

## Constraints

- 0 ≤ len(nums) ≤ 10^5
- -10^4 ≤ nums[i] ≤ 10^4

---

### คำอธิบาย
- **Description**: โจทย์ให้หาผลรวมของตัวเลขที่ไม่ซ้ำ (ปรากฏเพียงครั้งเดียวในรายการ)
- **Function Signature**: ต้องเขียนฟังก์ชัน `sumOfUnique(nums: list[int]) -> int`
- **Examples**: ตารางตัวอย่างช่วยให้เห็นอินพุตและผลลัพธ์ที่คาดหวัง
- **Constraints**: กำหนดขอบเขตของขนาดรายการและค่าตัวเลขในรายการ
