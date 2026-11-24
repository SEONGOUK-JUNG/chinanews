# -*- coding: utf-8 -*-
"""
chinanews.kr 원자재·뉴스 수집 + 발행 파이프라인 (무인 실행용 러너)

순서: fetch_spot -> parse_build -> patch_dupes (-> patch_dupes_gap) -> fetch_news
      -> stage_local -> git clone(pub) -> publish_prep -> check_new -> build_pages
      -> verify_clean -> commit/push
각 단계는 기존 검증된 스크립트(같은 폴더)를 그대로 호출한다.
로그: ..\logs\pipeline_YYYY-MM-DD.log
종료코드: 0 성공 / 1 실패 (수집 실패 시 라이브 데이터는 건드리지 않음)
"""
import datetime, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # Desktop\chinanews-kr
DATA = os.path.join(ROOT, "data")
PUB = os.path.join(HERE, "pub")
REPO = "https://github.com/SEONGOUK-JUNG/chinanews.git"
KST = datetime.timezone(datetime.timedelta(hours=9))
LOGDIR = os.path.join(ROOT, "logs")
os.makedirs(LOGDIR, exist_ok=True)
LOG = open(os.path.join(LOGDIR, "pipeline_%s.log" % datetime.datetime.now(KST).strftime("%Y-%m-%d")), "a", encoding="utf-8")

def log(msg):
    line = "[%s] %s" % (datetime.datetime.now(KST).strftime("%H:%M:%S"), msg)
    LOG.write(line + "\n"); LOG.flush()
    try: print(line)
    except Exception: pass

def run(cmd, cwd=None, check=True):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", GIT_TERMINAL_PROMPT="0")
    r = subprocess.run(cmd, cwd=cwd or HERE, capture_output=True, env=env)
    out = (r.stdout + r.stderr).decode("utf-8", "replace")
    out = re.sub(r"https://[^@\s]+@", "https://***@", out)
    if check and r.returncode != 0:
        log("FAILED (%s): %s\n%s" % (r.returncode, " ".join(cmd), out[-1500:]))
        raise SystemExit(1)
    return out

def py(script):
    out = run([sys.executable, os.path.join(HERE, script)])
    log("%s: %s" % (script, out.strip()[-700:]))
    return out

def main():
    log("=== pipeline start ===")
    # Independent of commodity collection: refresh macro/rates on every run.
    try:
        py("fetch_macro.py")
    except SystemExit:
        log("WARNING: macro/rates refresh failed; preserve previous values and dates")
    live = json.load(open(os.path.join(DATA, "commodities.json"), encoding="utf-8"))
    live_ref = live.get("ref_date")

    # 1) 수집 (DNS 일시 오류는 1회 재시도)
    try:
        py("fetch_spot.py")
    except SystemExit:
        log("fetch_spot retry")
        py("fetch_spot.py")
    py("parse_build.py")
    new = json.load(open(os.path.join(HERE, "commodities.new.json"), encoding="utf-8"))
    if len(new.get("all_items", [])) < 300 or len(new.get("featured", [])) != 16:
        log("ABORT: parsed data too small (items=%d featured=%d)" % (len(new.get("all_items", [])), len(new.get("featured", []))))
        raise SystemExit(1)
    log("ref_date live=%s new=%s" % (live_ref, new["ref_date"]))

    # 2) 동명 품목 교정 (정확 anchor 0건 + 날짜 전진이면 갭 보정)
    out = py("patch_dupes.py")
    m = re.search(r"reordered for continuity: (\d+)", out)
    reordered = int(m.group(1)) if m else 0
    if reordered == 0 and new["ref_date"] != live_ref:
        log("gap fallback: patch_dupes_gap.py")
        # 갭 보정은 라이브 기준값(head_commodities.json)이 필요 -> stage_local 전이라 로컬 파일이 곧 라이브
        shutil.copyfile(os.path.join(DATA, "commodities.json"), os.path.join(HERE, "head_commodities.json"))
        py("patch_dupes_gap.py")

    # 3) 뉴스 (실패해도 계속: stage_local 이 기존 파일을 유지)
    try:
        py("fetch_news.py")
    except SystemExit:
        log("fetch_news failed -> keep existing news files")

    # 3-1) 품목별 가격 단위 (막히면 지난번 표를 그대로 쓴다)
    try:
        py("fetch_units.py")
    except SystemExit:
        log("fetch_units failed -> keep existing units.json")

    # 4) 로컬 반영
    py("stage_local.py")

    # 4-1) 품목별 시계열에 그날 점을 쌓는다
    #   이 단계가 빠져 있어 commodity_charts 가 2026-07-30 에서 51일 멈췄다.
    #   실패해도 나머지는 계속한다 — 지난 계열이 남아 있는 편이 낫다.
    try:
        py("append_charts.py")
    except SystemExit:
        log("append_charts failed -> keep existing commodity_charts")

    # 5) 발행용 새 클론
    if os.path.exists(PUB):
        # Windows: .git 안의 읽기전용 파일 때문에 rmtree 가 실패하므로 권한을 풀고 지운다
        def _unlock(func, path, _exc):
            os.chmod(path, 0o777); func(path)
        shutil.rmtree(PUB, onerror=_unlock)
        if os.path.exists(PUB):
            log("ABORT: cannot remove old clone folder")
            raise SystemExit(1)
    run(["git", "clone", "-q", "--depth", "1", REPO, PUB])
    py("publish_prep.py")
    py("check_new.py")
    run([sys.executable, os.path.join(PUB, "tools", "build_pages.py"), "--root", PUB])
    log("build_pages done")
    py("verify_clean.py")

    # 6) 커밋·푸시
    run(["git", "config", "user.email", "koreagwangju@gmail.com"], cwd=PUB)
    run(["git", "config", "user.name", "BRIDGE GROUP"], cwd=PUB)
    run(["git", "add", "data/", "sitemap.xml", "feed.xml", "about.html", "commodity/", "ko/", "daily/", "commodities/", "supply/"], cwd=PUB)
    staged = run(["git", "diff", "--cached", "--name-only"], cwd=PUB).strip()
    if not staged:
        log("nothing to publish (no real changes)")
        log("=== pipeline done ===")
        return 0
    stamp = datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    run(["git", "-c", "core.safecrlf=false", "commit", "-q", "-m", "자동 데이터 갱신 · %s KST" % stamp], cwd=PUB)
    run(["git", "push", "-q", "origin", "HEAD:main"], cwd=PUB)
    remote = run(["git", "ls-remote", "origin", "-h", "refs/heads/main"], cwd=PUB).split()[0][:10]
    local = run(["git", "rev-parse", "--short=10", "HEAD"], cwd=PUB).strip()
    log("pushed %s (remote %s) · %d files" % (local, remote, len(staged.splitlines())))
    if remote != local:
        log("WARNING: remote head differs from local")
        return 1
    log("=== pipeline done ===")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit as e:
        raise
    except Exception as e:
        log("ERROR: %r" % (e,))
        sys.exit(1)
