#!/usr/bin/env python3
"""Offline protocol fixture for tests and adapter development."""
from __future__ import annotations
import json
import sys

request = json.load(sys.stdin)
operation = request.get("operation")
payload = request.get("payload", {})
if operation == "process-source":
    result = {"items": [{"type": "fact", "title": "客户方案需要来源追溯", "summary": "客户方案中的重要结论需要保留来源路径。", "body": "生成客户方案时，重要结论应链接到未被改写的原始来源。", "confidence": "medium", "source_quality": "primary"}]}
elif operation == "prepare-task":
    result = {"task_summary": "根据可信知识准备客户方案。", "recommended_approach": ["先确认目标受众", "再按业务结果、实施条件和风险边界组织内容"], "missing_context": ["客户行业和截止时间"], "questions": ["方案面向哪一类管理者？"], "risk_notes": ["未核实内容不能作为确定结论"]}
elif operation == "finish-task":
    result = {"items": [{"type": "decision", "title": "客户方案优先展示实施路径", "summary": "本次方案优先展示落地路径而非模型参数。", "body": "面向企业管理层时，本次材料先说明实施条件、交付路径和风险边界。", "confidence": "medium", "source_quality": "primary"}]}
elif operation == "review-stale":
    candidates = payload.get("candidates", [])
    result = {"proposals": [{"target": item["path"], "suggestion": "重新核对来源并更新复核日期", "evidence": item.get("summary", ""), "uncertainty": "当前结论可能已超过复核日期"} for item in candidates]}
else:
    result = {}
json.dump(result, sys.stdout, ensure_ascii=False)
