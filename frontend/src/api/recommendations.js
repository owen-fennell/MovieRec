const BASE_URL = '/api';

export async function fetchRecommendations(engine, userId, n = 10) {
  const res = await fetch(`${BASE_URL}/recommend/${engine}/${userId}?n=${n}`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || 'Failed to fetch recommendations');
  }
  return res.json();
}

export async function fetchUsers() {
  const res = await fetch(`${BASE_URL}/users`);
  if (!res.ok) throw new Error('Failed to fetch users');
  return res.json();
}

export async function fetchHealth() {
  const res = await fetch(`${BASE_URL}/health`);
  if (!res.ok) throw new Error('API is unreachable');
  return res.json();
}