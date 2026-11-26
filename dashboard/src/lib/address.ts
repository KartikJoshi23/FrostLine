// Plan 7.2 and 10.1, rule 12: a wallet under a public vote is shown only in a short form
// until its freeze executes. Full addresses appear only for wallets Tether has frozen.

const TRON_ADDRESS = /^T[1-9A-HJ-NP-Za-km-z]{33}$/;

export function isTronAddress(value: string): boolean {
  return TRON_ADDRESS.test(value);
}

export function shortAddress(address: string): string {
  if (!isTronAddress(address)) throw new Error("Not a TRON address");
  return `T…${address.slice(-4)}`;
}

export function displayAddress(address: string, frozen: boolean): string {
  return frozen ? address : shortAddress(address);
}
