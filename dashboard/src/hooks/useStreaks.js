import { useState, useEffect, useCallback } from 'react';

const API_BASE = process.env.REACT_APP_API_URL || '';

export function useStreaks() {
  const [streaks, setStreaks]   = useState([]);
  const [leagues, setLeagues]   = useState([]);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState(null);
  const [lastFetched, setLastFetched] = useState(null);

  const fetchAll = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [streakRes, leagueRes] = await Promise.all([
        fetch(`${API_BASE}/api/streaks`),
        fetch(`${API_BASE}/api/leagues`),
      ]);

      if (!streakRes.ok) throw new Error(`Streaks API error: ${streakRes.status}`);
      if (!leagueRes.ok) throw new Error(`Leagues API error: ${leagueRes.status}`);

      const [streakData, leagueData] = await Promise.all([
        streakRes.json(),
        leagueRes.json(),
      ]);

      setStreaks(streakData);
      setLeagues(leagueData);
      setLastFetched(new Date());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchAll(); }, [fetchAll]);

  return { streaks, leagues, loading, error, refetch: fetchAll, lastFetched };
}
