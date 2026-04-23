import types
import threading

# ---------- โจทย์ & เคสทดสอบ (Public) ----------
PROBLEMS = {
    "add": {
        "signature": ("add",),
        "tests": [
            (("func", (2,3), {}), 5),
            (("func", (-1,1), {}), 0),
            (("func", (10,20), {}), 30),
        ],
    },
    "is_even": {
        "signature": ("is_even",),
        "tests": [
            (("func", (0,), {}), True),
            (("func", (1,), {}), False),
            (("func", (-2,), {}), True),
        ],
    },
    "middle_char": {
        "signature": ("middle_char",),
        "tests": [
            (("func", ("",), {}), ""),
            (("func", ("a",), {}), "a"),
            (("func", ("xy",), {}), "xy"),
            (("func", ("cat",), {}), "a"),
        ],
    },
    "unique_sorted": {
        "signature": ("unique_sorted",),
        "tests": [
            (("func", ([],), {}), []),
            (("func", ([1],), {}), [1]),
            (("func", ([3,3,2,1],), {}), [1,2,3]),
        ],
    },
    "count_vowels": {
        "signature": ("count_vowels",),
        "tests": [
            (("func", ("AEiou",), {}), 5),
            (("func", ("xyz",), {}), 0),
            (("func", ("",), {}), 0),
        ],
    },
    "two_sum": {
        "signature": ("two_sum",),
        "tests": [
            (("func", ([2,7,11,15], 9), {}), (0,1)),
            # อนุญาตคำตอบใดก็ได้ที่ถูกต้อง จะตรวจแบบ 'เซต' ในภายหลัง
            (("func", ([1,2,3], 5), {}), {(0,2),(1,2)}),  # set of valid answers
            (("func", ([1,1,1], 10), {}), None),
        ],
    },
    "is_anagram": {
        "signature": ("is_anagram",),
        "tests": [
            (("func", ("Listen","Silent"), {}), True),
            (("func", ("Dormitory", "Dirty room"), {}), True),
            (("func", ("a","aa"), {}), False),
        ],
    },
    "collatz_steps": {
        "signature": ("collatz_steps",),
        "tests": [
            (("func", (1,), {}), 0),
            (("func", (2,), {}), 1),
            (("func", (3,), {}), 7),
            (("func", (6,), {}), 8),
        ],
    },
    "rle_encode": {
        "signature": ("rle_encode",),
        "tests": [
            (("func", ("",), {}), ""),
            (("func", ("a",), {}), "a1"),
            (("func", ("aaabbc",), {}), "a3b2c1"),
        ],
    },
    "spiral_order": {
        "signature": ("spiral_order",),
        "tests": [
            (("func", ([],), {}), []),
            (("func", ([[1]],), {}), [1]),
            (("func", ([[1,2],[3,4]],), {}), [1,2,4,3]),
            (("func", ([[1,2,3],[4,5,6],[7,8,9]],), {}), [1,2,3,6,9,8,7,4,5]),
        ],
    },
}

# ---------- ยูทิลตรวจ & รันด้วย timeout ----------
class TimeoutError(Exception):
    pass

def run_with_timeout(func, args=(), kwargs=None, timeout=1.5):
    if kwargs is None:
        kwargs = {}
    result = {"value": None, "error": None}
    def target():
        try:
            result["value"] = func(*args, **kwargs)
        except Exception as e:
            result["error"] = e
    t = threading.Thread(target=target, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():
        raise TimeoutError("Time limit exceeded")
    if result["error"] is not None:
        raise result["error"]
    return result["value"]

# ---------- ฟังก์ชันตรวจหนึ่งข้อ ----------
def grade_one(problem_key: str, student_ns: dict):
    spec = PROBLEMS[problem_key]
    func_name = spec["signature"][0]
    if func_name not in student_ns or not isinstance(student_ns[func_name], types.FunctionType):
        return {"passed": False, "detail": f"ไม่พบฟังก์ชัน {func_name}()"}
    f = student_ns[func_name]
    results = []
    for (kind, call, kw), expected in spec["tests"]:
        try:
            if kind != "func":
                return {"passed": False, "detail": f"รูปแบบเคสไม่รองรับ: {kind}"}
            got = run_with_timeout(f, call, kw, timeout=1.5)

            # กรณีคำตอบหลายแบบที่ถูกต้องได้ (เช่น two_sum)
            if isinstance(expected, set):
                ok = False
                if isinstance(got, tuple) and len(got) == 2:
                    pair = tuple(sorted(got))
                    # ตรวจว่าเป็นหนึ่งในชุดที่รับได้โดยไม่สนลำดับ
                    if pair in {tuple(sorted(x)) for x in expected}:
                        ok = True
                results.append(("OK" if ok else "FAIL", call, expected, got))
            else:
                results.append(("OK" if got == expected else "FAIL", call, expected, got))
        except Exception as e:
            results.append(("ERROR", call, expected, repr(e)))

    passed = all(r[0] == "OK" for r in results)
    return {"passed": passed, "cases": results}

# ---------- ฟังก์ชันหลักสำหรับตรวจทั้งไฟล์นักเรียน ----------
def grade_all(student_code: str):
    report = {}
    for key in PROBLEMS.keys():
        ns = {}
        try:
            exec(student_code, ns)
        except Exception as e:
            report[key] = {"passed": False, "detail": f"โค้ดคอมไพล์ไม่ผ่าน: {e}"}
            continue
        report[key] = grade_one(key, ns)
    return report

# ------------------ ตัวอย่างการใช้งาน ------------------
if __name__ == "__main__":
    # วางโค้ดนักเรียนตรงนี้เป็นสตริง (ตัวอย่างถูกครึ่งๆ เพื่อให้เห็น FAIL/OK)
    student_solution = r'''
def add(a,b): return a+b
def is_even(n): return n%2==0
def middle_char(s):
    n=len(s)
    if n==0: return ""
    m=n//2
    return s[m] if n%2==1 else s[m-1:m+1]
def unique_sorted(nums): return sorted(set(nums))
def count_vowels(s):
    return sum(ch.lower() in "aeiou" for ch in s)
def two_sum(nums, target):
    m={}
    for i,x in enumerate(nums):
        if target-x in m: return (m[target-x], i)
        m[x]=i
    return None
def is_anagram(a,b):
    import re
    A=re.sub(r"\s+","",a).lower()
    B=re.sub(r"\s+","",b).lower()
    from collections import Counter
    return Counter(A)==Counter(B)
def collatz_steps(n):
    steps=0
    while n>1:
        if n%2==0: n//=2
        else: n=3*n+1
        steps+=1
    return steps
def rle_encode(s):
    if not s: return ""
    out=[];cnt=1
    for i in range(1,len(s)):
        if s[i]==s[i-1]: cnt+=1
        else:
            out.append(f"{s[i-1]}{cnt}")
            cnt=1
    out.append(f"{s[-1]}{cnt}")
    return "".join(out)
def spiral_order(mat):
    res=[]
    if not mat: return res
    top,left=0,0
    bottom,len_col=len(mat)-1,len(mat[0])-1
    while top<=bottom and left<=len_col:
        for c in range(left, len_col+1): res.append(mat[top][c])
        top+=1
        for r in range(top, bottom+1): res.append(mat[r][len_col])
        len_col-=1
        if top<=bottom:
            for c in range(len_col, left-1, -1): res.append(mat[bottom][c])
            bottom-=1
        if left<=len_col:
            for r in range(bottom, top-1, -1): res.append(mat[r][left])
            left+=1
    return res
'''
    summary = grade_all(student_solution)
    for k,v in summary.items():
        print(f"=== {k} ===")
        if "cases" in v:
            for status, call, exp, got in v["cases"]:
                print(status, f"{k}{call} -> expected {exp}, got {got}")
        else:
            print(v)
