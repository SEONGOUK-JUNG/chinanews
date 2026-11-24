#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║  차이나뉴스 터미널 · 자동 업데이트 스크립트                                  ║
║                                                                          ║
║  실행 흐름:                                                               ║
║    1) fx_collector.py 실행 → data/fx_latest.json 갱신                    ║
║    2) stocks_collector.py 실행 → data/stocks_latest.json 갱신            ║
║    3) JSON 파일을 publish 폴더 (Git 리포)로 복사                          ║
║    4) Git add · commit · push 자동                                       ║
║                                                                          ║
║  스케줄: Windows 작업 스케줄러가 update.bat 호출 → 본 스크립트 실행         ║
║                                                                          ║
║  ⚠️ 사전 조건:                                                             ║
║    • Git for Windows 설치됨                                              ║
║    • chinanews-publish 폴더에 GitHub 리포 clone됨                        ║
║    • 첫 push 시 GitHub PAT를 Windows Credential Manager에 저장 완료      ║
║                                                                          ║
║  작성: 2026-05-29 · v1.0                                                 ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import logging
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ───── 경로 설정 ─────
KST = timezone(timedelta(hours=9))
BASE_DIR = Path(__file__).resolve().parent
PUBLISH_DIR = BASE_DIR.parent / "chinanews-publish"  # 대표님 바탕화면의 git 리포 폴더
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

today_str = datetime.now(KST).strftime("%Y-%m-%d")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"auto_{today_str}.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("AUTO")


def run_python(script_name: str) -> bool:
    """Python 스크립트 실행."""
    script_path = BASE_DIR / script_name
    if not script_path.exists():
        log.error(f"[{script_name}] 파일 없음")
        return False
    try:
        log.info(f"[{script_name}] 실행 시작")
        # python.exe 명시적 사용 (Windows 작업 스케줄러에서 안정적)
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300,  # 5분 타임아웃
        )
        if result.returncode == 0:
            log.info(f"[{script_name}] ✓ 종료 코드 0 (성공)")
            return True
        elif result.returncode == 3:
            log.warning(f"[{script_name}] △ 종료 코드 3 (부분 성공)")
            return True
        else:
            log.error(f"[{script_name}] ✗ 종료 코드 {result.returncode}")
            if result.stderr:
                log.error(f"  stderr: {result.stderr[-500:]}")
            return False
    except subprocess.TimeoutExpired:
        log.error(f"[{script_name}] 타임아웃 (5분 초과)")
        return False
    except Exception as e:
        log.error(f"[{script_name}] 예외: {e}")
        return False


def copy_data_to_publish() -> bool:
    """
    data/*.json + data/charts/*.json 을 publish/data/ 로 복사.
    """
    if not PUBLISH_DIR.exists():
        log.error(f"publish 폴더 없음: {PUBLISH_DIR}")
        log.error("  → chinanews-publish 폴더에 GitHub 리포를 clone 해주세요")
        return False

    publish_data = PUBLISH_DIR / "data"
    publish_data.mkdir(parents=True, exist_ok=True)

    copied = 0

    # 1) data 루트의 JSON 파일들 (fx, stocks 등)
    for src in DATA_DIR.glob("*.json"):
        if src.name.startswith("_"):
            continue  # _history.csv 같은 내부 파일 제외
        dst = publish_data / src.name
        try:
            shutil.copy2(src, dst)
            log.info(f"  copy: {src.name} ({src.stat().st_size:,} bytes)")
            copied += 1
        except Exception as e:
            log.error(f"  copy 실패 {src.name}: {e}")

    # 2) data/charts/ 폴더 통째 (캔들 차트 데이터)
    charts_src = DATA_DIR / "charts"
    if charts_src.exists():
        charts_dst = publish_data / "charts"
        charts_dst.mkdir(parents=True, exist_ok=True)
        chart_count = 0
        for src in charts_src.glob("*.json"):
            dst = charts_dst / src.name
            try:
                shutil.copy2(src, dst)
                chart_count += 1
            except Exception as e:
                log.error(f"  charts copy 실패 {src.name}: {e}")
        if chart_count > 0:
            log.info(f"  copy: data/charts/ ({chart_count}개 차트 파일)")
            copied += chart_count

    log.info(f"[copy] ✓ {copied}개 파일 publish 폴더로 복사")
    return copied > 0


def run_git(args: list, allow_fail: bool = False) -> tuple[bool, str]:
    """Git 명령 실행. (성공여부, 출력) 반환."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=str(PUBLISH_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        out = (result.stdout + result.stderr).strip()
        if result.returncode == 0:
            return True, out
        else:
            if not allow_fail:
                log.error(f"[git {args[0]}] 실패: {out[-300:]}")
            return False, out
    except Exception as e:
        log.error(f"[git {args[0]}] 예외: {e}")
        return False, str(e)


def git_commit_and_push() -> bool:
    """Git add · commit · push."""
    now = datetime.now(KST)
    timestamp = now.strftime("%Y-%m-%d %H:%M KST")
    commit_msg = f"자동 데이터 갱신 · {timestamp}"

    # 1) 변경된 파일 있는지 확인
    ok, status = run_git(["status", "--porcelain", "data/"])
    if not ok:
        return False
    if not status.strip():
        log.info("[git] 변경된 파일 없음 — push 생략")
        return True

    log.info(f"[git] 변경 파일:\n  {status}")

    # 2) add
    ok, _ = run_git(["add", "data/"])
    if not ok:
        return False

    # 3) commit
    ok, out = run_git(["commit", "-m", commit_msg], allow_fail=True)
    if not ok:
        if "nothing to commit" in out:
            log.info("[git] 변경 사항 없음")
            return True
        log.error(f"[git commit] 실패: {out[-300:]}")
        return False
    log.info(f"[git commit] ✓ {commit_msg}")

    # 4) push
    ok, out = run_git(["push", "origin", "main"])
    if not ok:
        log.error(f"[git push] 실패: {out[-300:]}")
        log.error("  → GitHub PAT 인증 캐시 확인 필요")
        return False
    log.info(f"[git push] ✓ origin/main")
    return True


def main():
    now = datetime.now(KST)
    # Keep the alternate scheduled updater on the same validated macro source.
    run_python("pipeline/fetch_macro.py")
    log.info("═" * 74)
    log.info(f" 자동 업데이트 시작 · {now.isoformat()}")
    log.info("═" * 74)

    # 1) 환율
    log.info("─" * 60)
    log.info("【1/6 · 환율 수집】")
    fx_ok = run_python("fx_collector.py")

    # 2) 주식·지수
    log.info("─" * 60)
    log.info("【2/6 · 주식·지수 수집】")
    stk_ok = run_python("stocks_collector.py")

    # 3) 차트 (OHLC 캔들)
    log.info("─" * 60)
    log.info("【3/7 · 차트 캔들 수집】")
    chart_ok = run_python("chart_collector.py")

    # 4) 시장 펄스 집계 (stocks + charts 기반)
    log.info("─" * 60)
    log.info("【4/7 · 시장 펄스 집계】")
    pulse_ok = run_python("pulse_collector.py")

    # 5) DART 공시
    log.info("─" * 60)
    log.info("【5/7 · DART 공시 수집】")
    dart_ok = run_python("dart_collector.py")

    if not (fx_ok or stk_ok or chart_ok or pulse_ok or dart_ok):
        log.error("모든 수집 실패 — Git 푸시 건너뜀")
        sys.exit(1)

    # 6) publish 폴더로 복사
    log.info("─" * 60)
    log.info("【6/7 · publish 폴더로 복사】")
    copy_ok = copy_data_to_publish()
    if not copy_ok:
        log.error("복사 실패 — Git 푸시 건너뜀")
        sys.exit(2)

    # 7) Git push
    log.info("─" * 60)
    log.info("【7/7 · Git add · commit · push】")
    push_ok = git_commit_and_push()

    log.info("═" * 74)
    if push_ok:
        log.info(f" ✅ 자동 업데이트 완료 · 1~2분 후 chinanews.kr 갱신됨")
    else:
        log.warning(f" ⚠️ 일부 실패 — 로그 확인 필요")
    log.info("═" * 74)

    sys.exit(0 if push_ok else 3)


if __name__ == "__main__":
    main()
