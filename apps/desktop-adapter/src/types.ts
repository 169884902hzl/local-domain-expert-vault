export type StatusKind =
  | "idle"
  | "success"
  | "partial"
  | "missing_config"
  | "blocked"
  | "failed"
  | "unverified"
  | "running";

export interface VaultValidation {
  ok: boolean;
  vault_path: string;
  missing: string[];
  warnings: string[];
}

export interface AdapterConfig {
  vault_path: string;
  daily_time: string;
  codex_time: string;
  weekly_day: string;
  weekly_time: string;
  enabled_modules: string[];
}

export interface EnvStatus {
  zotero_user_id: boolean;
  zotero_api_key: boolean;
  zotero_collection_key: boolean;
}

export interface CommandStarted {
  run_id: string;
  command_id: string;
  label: string;
}

export interface CommandOutput {
  run_id: string;
  stream: "stdout" | "stderr";
  line: string;
}

export interface CommandFinished {
  run_id: string;
  command_id: string;
  exit_code: number | null;
  status: StatusKind;
}

export interface DiagnosticExport {
  path: string;
  content: string;
}
