const bounds = [5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 15000, 60000];

export class Summary {
  #services = new Map();

  add(record) {
    if (!record || Array.isArray(record) || typeof record !== "object")
      throw Error("expected a JSON object");
    const {service, status, ms} = record;
    if (typeof service !== "string" || !/^[a-z0-9_-]{1,48}$/.test(service) ||
        !Number.isInteger(status) || status < 100 || status > 599 ||
        !Number.isFinite(ms) || ms < 0 || ms > 60000) throw Error("invalid record");

    if (!this.#services.has(service)) {
      if (this.#services.size >= 256) throw Error("too many services");
      this.#services.set(service, {requests: 0, errors: 0, bins: Array(bounds.length).fill(0)});
    }
    const row = this.#services.get(service);
    row.requests++;
    if (status >= 500) row.errors++;
    row.bins[bounds.findIndex(bound => ms <= bound)]++;
  }

  report() {
    return [...this.#services.keys()].sort().map(service => {
      const {requests, errors, bins} = this.#services.get(service);
      let accumulated = 0;
      const rank = Math.ceil(requests * .95);
      const index = bins.findIndex(count => (accumulated += count) >= rank);
      return {service, requests, errors, p95_upper_ms: bounds[index]};
    });
  }
}
