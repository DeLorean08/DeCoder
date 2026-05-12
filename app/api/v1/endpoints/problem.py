from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from app.dependencies import get_current_user
from app.shemas.user import UserOut
from app.shemas.problem import ProblemBase
from pathlib import Path
from fastapi.templating import Jinja2Templates
from app.core.logging_config import logging
import subprocess
import json
import time



logger = logging.getLogger(__name__)

router = APIRouter(prefix="/problem", tags=["PROBLEM"])

template_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=template_dir)

@router.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request, user: UserOut = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="problems.html", context={"request": request, "user": user})

@router.get("/demo-twosum", response_class=HTMLResponse)
async def get_problem_two_sum(request: Request, user: UserOut = Depends(get_current_user)):
    problem = {
    "title": "Two Sum",
    "difficulty": "Easy",
    "description": "<h3>Умова</h3><p>Дано масив цілих чисел nums та ціле число target.\n Необхідно знайти індекси двох чисел у цьому масиві так, щоб їхня сума дорівнювала значенню target\n</p><pre><code class='language-python'>Input: nums = [2,7,11,15], target = 9</code></pre>",
    "starter_code": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        # Твій код тут"
}
    return templates.TemplateResponse(request=request, name="twosum.html", context={"request": request, "user": user, "problem": problem})

@router.post("/execute-twosum", response_class=HTMLResponse)
async def execute_problem_two_sum(problem: ProblemBase, request: Request, user: UserOut = Depends(get_current_user)):
    start_time = time.perf_counter()
    full_code = problem.submission + "\n" + """
import json
print(json.dumps(Solution().twoSum([1, 2, 3], 7)))
print(json.dumps(Solution().twoSum([-1, -2, -3, -4, -5], -8)))
print(json.dumps(Solution().twoSum([3, 3], 6)))
print(json.dumps(Solution().twoSum([3, 2, 4], 6)))
"""  
    try:

        result = subprocess.run(
            ["docker", "run", "--rm", "-i", "--net", "none", "--memory=128m", "--cpus=.5", "python:3.12-slim", "python", "-"],
            input=full_code,
            capture_output=True,
            text=True,
            timeout=20
        )

        if result.returncode != 0:
            output = f"<span style='color: red;'><b>Помилка виконання:</b><br><pre>{result.stderr or result.stdout}</pre></span>"
        else:
            outputs = result.stdout.strip().split('\n')
            
            def get_result(index):
                try:
                    return json.loads(outputs[index]) if len(outputs) > index and outputs[index] else None
                except Exception:
                    return outputs[index] if len(outputs) > index else None

            test_json = {
                "[1, 2, 3], target=7": {"passed": get_result(0) == [], "result": get_result(0), "expected": []},
                "[-1, -2, -3, -4, -5], target=-8": {"passed": get_result(1) == [2, 4], "result": get_result(1), "expected": [2, 4]},
                "[3, 3], target=6": {"passed": get_result(2) == [0, 1], "result": get_result(2), "expected": [0, 1]},
                "[3, 2, 4], target=6": {"passed": get_result(3) == [1, 2], "result": get_result(3), "expected": [1, 2]}
            }

            output_lines = []
            all_passed = True
            for k, v in test_json.items():
                if not v["passed"]:
                    output_lines.append(f"<div style='color: red;'>&#10060; <b>Ви не пройшли тест:</b> {k}. Очікувалось: {v['expected']}, Ваш результат: {v['result']}</div>")
                    all_passed = False
                    break
                else:
                    output_lines.append(f"<div style='color: green;'>&#9989; Тест пройдено: {k}</div>")
            
            if all_passed:
                output_lines.append("<br><h4 style='color: green;'>Всі тести успішно пройдено!</h4>")
            
            output = "".join(output_lines)
            
    except subprocess.TimeoutExpired:
        output = "<span style='color: red;'><b>Помилка:</b> Перевищено ліміт часу (Time Limit Exceeded)</span>"
    except Exception as e:
        output = f"<span style='color: red;'><b>Системна помилка:</b> {str(e)}</span>"
    process_time = time.perf_counter() - start_time
    print(f"Время обробки задачи: {process_time}") 
    return HTMLResponse(content=output)
