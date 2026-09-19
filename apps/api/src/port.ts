const DEFAULT_PORT = 8787;
const MIN_PORT = 1;
const MAX_PORT = 65535;

export function parsePort(value: string | undefined): number {
  if (value === undefined) {
    return DEFAULT_PORT;
  }

  const parsed = Number(value);

  if (!Number.isInteger(parsed) || parsed < MIN_PORT || parsed > MAX_PORT) {
    throw new Error(
      `PORT must be an integer between ${MIN_PORT} and ${MAX_PORT}, but received "${value}"`,
    );
  }

  return parsed;
}
