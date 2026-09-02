export interface Passport {
  agent_id: string;
  name: string;
  owner: string;
  provider?: string;
  model?: string;
  status: string;
  fingerprint: string;
}

export interface AuditRecord {
  record_id: string;
  agent_id: string;
  action: string;
  verdict: string;
  reason?: string;
}

export class Client {
  private baseUrl: string;

  constructor(baseUrl = "http://127.0.0.1:8420") {
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  private async req<T>(method: string, path: string, body?: unknown): Promise<T> {
    const resp = await fetch(this.baseUrl + path, {
      method,
      headers: { "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    if (!resp.ok) {
      throw new Error(`${method} ${path} -> HTTP ${resp.status}`);
    }
    return (await resp.json()) as T;
  }

  health() {
    return this.req<{ status: string }>("GET", "/healthz");
  }

  doctor() {
    return this.req<Record<string, unknown>>("GET", "/doctor");
  }

  listPassports() {
    return this.req<Passport[]>("GET", "/passports");
  }

  issue(name: string, owner: string, capabilities?: unknown[]) {
    return this.req<Passport>("POST", "/passports", { name, owner, capabilities });
  }

  audit(agentId: string, action: string, context?: unknown) {
    return this.req<AuditRecord>("POST", "/audit", { agent_id: agentId, action, context });
  }

  verifyChain() {
    return this.req<{ intact: boolean; broken_index: number }>("GET", "/audit/verify");
  }

  topology() {
    return this.req<{ topology: string }>("GET", "/channels/topology");
  }
}
