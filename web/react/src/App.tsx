import { useEffect, useState } from "react";

interface Passport { agent_id: string; name: string; owner: string; status: string; fingerprint: string; }
interface Doctor { passports: number; audit_records: number; chain_intact: boolean; }

export default function App() {
  const [doctor, setDoctor] = useState<Doctor | null>(null);
  const [passports, setPassports] = useState<Passport[]>([]);

  useEffect(() => {
    fetch("/doctor").then(r => r.json()).then(setDoctor);
    fetch("/passports").then(r => r.json()).then(setPassports);
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ fontSize: 20, color: "#7c9cff" }}>agentpassport 控制台</h1>
      {doctor && (
        <div style={{ display: "flex", gap: 16, marginBottom: 20 }}>
          <Stat k="护照数" v={doctor.passports} />
          <Stat k="审计记录" v={doctor.audit_records} />
          <Stat k="哈希链完整" v={doctor.chain_intact ? "✓" : "✗"}
                color={doctor.chain_intact ? "#4ade80" : "#f87171"} />
        </div>
      )}
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>{["Agent ID", "名称", "所属", "状态", "指纹"].map(h =>
            <th key={h} style={thStyle}>{h}</th>)}
          </tr>
        </thead>
        <tbody>
          {passports.map(p => (
            <tr key={p.agent_id}>
              <td style={tdStyle}>{p.agent_id}</td>
              <td style={tdStyle}>{p.name}</td>
              <td style={tdStyle}>{p.owner}</td>
              <td style={{ ...tdStyle, color: p.status === "active" ? "#4ade80" : "#f87171" }}>{p.status}</td>
              <td style={tdStyle}>{p.fingerprint.slice(0, 12)}…</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const thStyle: React.CSSProperties = { textAlign: "left", padding: "10px 12px",
  borderBottom: "1px solid #1e2433", color: "#8b94ad", fontSize: 13, fontWeight: 500 };
const tdStyle: React.CSSProperties = { padding: "10px 12px", borderBottom: "1px solid #1e2433", fontSize: 13 };

function Stat({ k, v, color = "#e6e8ef" }: { k: string; v: string | number; color?: string }) {
  return (
    <div style={{ background: "#12182a", border: "1px solid #1e2433", borderRadius: 8, padding: 16 }}>
      <div style={{ color: "#8b94ad", fontSize: 12 }}>{k}</div>
      <div style={{ fontSize: 26, fontWeight: 700, marginTop: 6, color }}>{v}</div>
    </div>
  );
}
