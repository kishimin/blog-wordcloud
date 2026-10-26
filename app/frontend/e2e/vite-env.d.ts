/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly SOURCE_JA_LABEL: string;
  readonly SOURCE_OPTION_NAME: string;
  readonly ENTITY_JA_LABEL: string;
  readonly ENTITY_OPTION_NAME: string;
  readonly BASE_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
