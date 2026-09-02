# -*- coding: utf-8 -*-
"""agentpassport 命令行入口。"""
import argparse
import json
import sys

from ..platform import App


def main(argv=None):
    ap = argparse.ArgumentParser(prog="agentpassport",
                                 description="智能体数字护照与循环审计治理平台")
    ap.add_argument("--config", help="配置文件路径")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("version", help="打印版本")
    sub.add_parser("doctor", help="健康自检")
    sub.add_parser("serve", help="启动 HTTP 控制面")
    sub.add_parser("chain-verify", help="校验审计哈希链")

    p_issue = sub.add_parser("issue", help="签发数字护照")
    p_issue.add_argument("--name", required=True)
    p_issue.add_argument("--owner", required=True)
    p_issue.add_argument("--provider", default="")
    p_issue.add_argument("--model", default="")

    p_verify = sub.add_parser("verify", help="校验护照")
    p_verify.add_argument("agent_id")

    p_audit = sub.add_parser("audit", help="审计一次动作")
    p_audit.add_argument("agent_id")
    p_audit.add_argument("action")

    p_revoke = sub.add_parser("revoke", help="吊销护照")
    p_revoke.add_argument("agent_id")

    p_scan = sub.add_parser("scan", help="扫描账本篡改记录")

    args = ap.parse_args(argv)

    if args.cmd == "version":
        from ..version import __version__
        print(__version__)
        return 0

    app = App(config_path=args.config)

    if args.cmd == "doctor":
        print(json.dumps(app.doctor(), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "issue":
        p = app.issue(args.name, args.owner, provider=args.provider, model=args.model)
        print(json.dumps(p.to_dict(), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "verify":
        p = app.passport_store.get(args.agent_id)
        if not p:
            print("护照不存在: " + args.agent_id, file=sys.stderr)
            return 1
        try:
            app.verifier.validate(p)
            print("有效: %s (%s)" % (p.agent_id, p.name))
            return 0
        except Exception as e:  # noqa: BLE001
            print("无效: %s" % e, file=sys.stderr)
            return 1

    if args.cmd == "audit":
        rec = app.audit_action(args.agent_id, args.action)
        print(json.dumps(rec.to_dict(), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "revoke":
        app.authority.revoke(args.agent_id, "cli-revoke")
        print("已吊销: " + args.agent_id)
        return 0

    if args.cmd == "chain-verify":
        ok, idx = app.audit_ledger.verify_chain()
        print("哈希链完整: %s (断裂点=%s)" % (ok, idx))
        return 0 if ok else 1

    if args.cmd == "scan":
        tampered = app.tamper.scan(app.audit_ledger.list(100000))
        print("篡改记录数: %d %s" % (len(tampered), tampered))
        return 0

    if args.cmd == "serve":
        host = app.config.get("server", {}).get("host", "127.0.0.1")
        port = int(app.config.get("server", {}).get("port", 8420))
        from ..api.server import serve
        serve(app, host, port)
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
