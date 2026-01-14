"""
Python 條件判斷測驗 - Streamlit 網頁版
部署到 Streamlit Cloud 後，學生可以線上填寫並即時看成績
"""
import streamlit as st
import io
import re
from contextlib import redirect_stdout

st.set_page_config(
  page_title="Python 條件判斷測驗",
  page_icon="🐍",
  layout="wide"
)

def get_test_cases():
  """回傳所有題目的測試案例"""
  return {
    "q1": {
      "name": "基礎單向判斷",
      "description": "判斷變數 `number` 是否為正數 (大於 0)。如果是，請印出 \"這是正數\"。",
      "inputs": [{"number": 5}, {"number": -1}],
      "expected": ["這是正數", ""],
      "is_variable_check": False,
      "var_name": None
    },
    "q2": {
      "name": "雙向判斷 (if-else)",
      "description": "判斷變數 `age` 是否大於等於 18。如果是，印出 \"已成年\"；否則印出 \"未成年\"。",
      "inputs": [{"age": 18}, {"age": 17}],
      "expected": ["已成年", "未成年"],
      "is_variable_check": False,
      "var_name": None
    },
    "q3": {
      "name": "多重判斷 (if-elif-else)",
      "description": """根據變數 `temperature` (氣溫) 印出建議：
- 30 度以上 (含)：印出 \"天氣炎熱\"
- 20 度 (含) 到 30 度之間：印出 \"天氣舒適\"
- 20 度以下：印出 \"天氣寒冷\"""",
      "inputs": [{"temperature": 35}, {"temperature": 25}, {"temperature": 15}],
      "expected": ["天氣炎熱", "天氣舒適", "天氣寒冷"],
      "is_variable_check": False,
      "var_name": None
    },
    "q4": {
      "name": "巢狀判斷實作",
      "description": """實作一個簡單的登入驗證邏輯：
1. 先檢查 `username` 是否等於 \"admin\"
2. 如果帳號正確，再檢查 `password` 是否等於 \"12345\"
3. 若帳號密碼皆正確，印出 \"登入成功\"；若密碼錯誤，印出 \"密碼錯誤\"；若帳號錯誤，印出 \"查無此帳號\"""",
      "inputs": [
        {"username": "admin", "password": "12345"},
        {"username": "admin", "password": "wrong"},
        {"username": "user", "password": "12345"}
      ],
      "expected": ["登入成功", "密碼錯誤", "查無此帳號"],
      "is_variable_check": False,
      "var_name": None
    },
    "q5": {
      "name": "條件運算式 (三元運算子)",
      "description": "使用「一行程式碼」(條件運算式)，根據變數 `x` 的值決定 `y` 的值：如果 `x` 是偶數，`y` 為 \"Even\"；否則 `y` 為 \"Odd\"。",
      "inputs": [{"x": 2}, {"x": 3}],
      "expected": ["Even", "Odd"],
      "is_variable_check": True,
      "var_name": "y"
    },
    "q6": {
      "name": "邏輯運算子整合 (閏年)",
      "description": "判斷年份 `year` 是否為閏年。\n(提示：能被 4 整除且不能被 100 整除，或者能被 400 整除的年份為閏年)",
      "inputs": [{"year": 2000}, {"year": 1900}, {"year": 2024}, {"year": 2023}],
      "expected": ["閏年", ["平年", "不是閏年"], "閏年", ["平年", "不是閏年"]],
      "is_variable_check": False,
      "var_name": None
    },
    "q7": {
      "name": "真值測試應用",
      "description": "給定一個變數 `user_input` (可能是字串)。請使用最簡潔的方式判斷使用者是否有輸入內容，如果有內容則印出該內容，否則印出 \"請輸入文字\"。",
      "inputs": [{"user_input": "Hi"}, {"user_input": ""}],
      "expected": ["Hi", "請輸入文字"],
      "is_variable_check": False,
      "var_name": None
    },
    "q8": {
      "name": "門票計價",
      "description": """某遊樂園票價規則如下：
- 6 歲以下 (含) 或 65 歲以上 (含) 免費
- 具備學生身份 (`is_student = True`) 且年齡在 25 歲以下 (含) 享有半價
- 其餘皆為全票

請撰寫程式碼判斷變數 `age` 與 `is_student` 對應的票價類別 (免費、半價、全票)。""",
      "inputs": [
        {"age": 5, "is_student": False},
        {"age": 70, "is_student": False},
        {"age": 20, "is_student": True},
        {"age": 30, "is_student": True},
        {"age": 25, "is_student": False}
      ],
      "expected": ["免費", "免費", "半價", "全票", "全票"],
      "is_variable_check": False,
      "var_name": None
    },
    "q9": {
      "name": "程式碼優化 (扁平化)",
      "description": """請將以下巢狀程式碼改寫為使用 `if-elif-else` 結構：
```python
if score >= 60:
  if score >= 90:
    print("優秀")
  else:
    print("及格")
else:
  print("不及格")
```""",
      "inputs": [{"score": 95}, {"score": 75}, {"score": 50}],
      "expected": ["優秀", "及格", "不及格"],
      "is_variable_check": False,
      "var_name": None
    },
    "q10": {
      "name": "綜合邏輯：三角形判斷",
      "description": """給定三角形的三邊長 `a`, `b`, `c`。請撰寫程式碼判斷：
1. 是否能組成三角形 (任意兩邊長之和大於第三邊)
2. 如果可以，請進一步判斷是 \"等邊三角形\"、\"等腰三角形\" 還是 \"普通三角形\"""",
      "inputs": [
        {"a": 3, "b": 3, "c": 3},
        {"a": 3, "b": 3, "c": 4},
        {"a": 3, "b": 4, "c": 5},
        {"a": 1, "b": 1, "c": 10}
      ],
      "expected": ["等邊三角形", "等腰三角形", "普通三角形", ["無法組成三角形", "不能組成三角形"]],
      "is_variable_check": False,
      "var_name": None
    }
  }

def test_code(code, test_case):
  """測試單一題目"""
  if not code or not code.strip():
    return False, "未作答"

  for inp, exp in zip(test_case["inputs"], test_case["expected"]):
    f = io.StringIO()
    loc = inp.copy()
    try:
      with redirect_stdout(f):
        exec(code, {}, loc)

      if test_case["is_variable_check"]:
        actual = loc.get(test_case["var_name"])
      else:
        actual = f.getvalue().strip()

      if isinstance(exp, list):
        if actual not in exp:
          return False, f"輸入 {inp} → 預期 {exp}，實際 \"{actual}\""
      else:
        if actual != exp:
          return False, f"輸入 {inp} → 預期 \"{exp}\"，實際 \"{actual}\""

    except Exception as e:
      return False, f"執行錯誤：{e}"

  return True, "通過"

def main():
  st.title("🐍 Python 條件判斷測驗")
  st.markdown("請在每題下方的程式碼區塊中填入你的答案，完成後點擊「批改」按鈕查看成績。")

  test_cases = get_test_cases()

  # 初始化 session state
  if "answers" not in st.session_state:
    st.session_state.answers = {f"q{i}": "" for i in range(1, 11)}

  # 顯示每一題
  for i in range(1, 11):
    q_key = f"q{i}"
    tc = test_cases[q_key]

    st.markdown("---")
    st.subheader(f"第 {i} 題：{tc['name']}")
    st.markdown(tc["description"])

    st.session_state.answers[q_key] = st.text_area(
      f"你的答案 (第 {i} 題)",
      value=st.session_state.answers[q_key],
      height=120,
      key=f"input_{q_key}",
      label_visibility="collapsed"
    )

  st.markdown("---")

  # 批改按鈕
  col1, col2, col3 = st.columns([1, 1, 1])
  with col2:
    submit = st.button("📝 批改", type="primary", use_container_width=True)

  if submit:
    st.markdown("---")
    st.header("📊 批改結果")

    score = 0
    results = []

    for i in range(1, 11):
      q_key = f"q{i}"
      tc = test_cases[q_key]
      code = st.session_state.answers[q_key]

      passed, msg = test_code(code, tc)
      if passed:
        score += 1
        results.append((i, tc["name"], "✅", "通過"))
      else:
        results.append((i, tc["name"], "❌", msg))

    # 顯示總分
    percentage = score / 10 * 100
    if percentage >= 80:
      st.success(f"🎉 總得分：{score}/10 ({percentage:.0f}%)")
    elif percentage >= 60:
      st.warning(f"📝 總得分：{score}/10 ({percentage:.0f}%)")
    else:
      st.error(f"💪 總得分：{score}/10 ({percentage:.0f}%)")

    # 顯示每題結果
    st.markdown("### 各題詳情")
    for num, name, status, msg in results:
      if status == "✅":
        st.markdown(f"{status} **第 {num} 題** ({name})：{msg}")
      else:
        st.markdown(f"{status} **第 {num} 題** ({name})：{msg}")

if __name__ == "__main__":
  main()
