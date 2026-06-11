import React, { useState, useMemo } from 'react';
import { useStreaks } from './hooks/useStreaks';
import LeagueTabs from './components/LeagueTabs';
import FilterBar   from './components/FilterBar';
import StatsBar    from './components/StatsBar';
import TeamCard    from './components/TeamCard';
import styles      from './App.module.css';

// Map full league name → short code (mirrors app/config/leagues.py)
const LEAGUE_CODE_MAP = {
  'Premier League': 'PL',
  'La Liga':        'PD',
  'Bundesliga':     'BL1',
  'Serie A':        'SA',
  'Ligue 1':        'FL1',
};

function leagueCode(leagueName) {
  return LEAGUE_CODE_MAP[leagueName] || leagueName;
}

function sortStreaks(streaks, sortKey) {
  const copy = [...streaks];
  switch (sortKey) {
    case 'length_asc':  return copy.sort((a, b) => a.streak_length - b.streak_length);
    case 'date_desc':   return copy.sort((a, b) => b.match_date?.localeCompare(a.match_date));
    case 'alpha':       return copy.sort((a, b) => a.team.localeCompare(b.team));
    case 'length_desc':
    default:            return copy.sort((a, b) => b.streak_length - a.streak_length);
  }
}

export default function App() {
  const { streaks, leagues, loading, error, refetch, lastFetched } = useStreaks();

  const [activeLeague, setActiveLeague] = useState('ALL');
  const [typeFilter,   setTypeFilter]   = useState('ALL');
  const [sort,         setSort]         = useState('length_desc');

  // Build counts per league-code for the tab badges
  const counts = useMemo(() => {
    const map = { total: streaks.length };
    for (const s of streaks) {
      const code = leagueCode(s.league);
      map[code] = (map[code] || 0) + 1;
    }
    return map;
  }, [streaks]);

  // Filter + sort
  const visible = useMemo(() => {
    let filtered = streaks;

    if (activeLeague !== 'ALL') {
      filtered = filtered.filter(s => leagueCode(s.league) === activeLeague);
    }

    if (typeFilter !== 'ALL') {
      filtered = filtered.filter(s => s.streak_type === typeFilter);
    }

    return sortStreaks(filtered, sort);
  }, [streaks, activeLeague, typeFilter, sort]);

  return (
    <div className={styles.app}>

      {/* ── Header ──────────────────────────────────────────────────── */}
      <header className={styles.header}>
        <div className={styles.wordmark}>
          <span className={styles.wordmarkAccent}>◆</span>
          <span className={styles.wordmarkText}>STREAK SCOUT</span>
        </div>
        <p className={styles.tagline}>Live win / draw / loss streaks across Europe's top 5 leagues</p>
      </header>

      {/* ── League tabs ─────────────────────────────────────────────── */}
      <LeagueTabs
        leagues={leagues}
        active={activeLeague}
        onChange={setActiveLeague}
        counts={counts}
      />

      {/* ── Filter + sort bar ───────────────────────────────────────── */}
      <FilterBar
        typeFilter={typeFilter}
        onTypeFilter={setTypeFilter}
        sort={sort}
        onSort={setSort}
        onRefresh={refetch}
        loading={loading}
        lastFetched={lastFetched}
      />

      {/* ── Stats summary bar ───────────────────────────────────────── */}
      {!loading && !error && <StatsBar streaks={visible} />}

      {/* ── Main content ────────────────────────────────────────────── */}
      <main className={styles.main}>

        {loading && (
          <div className={styles.centred}>
            <div className={styles.spinner} aria-label="Loading streaks…" />
            <p className={styles.loadingText}>Scanning all leagues…</p>
          </div>
        )}

        {!loading && error && (
          <div className={styles.centred}>
            <div className={styles.errorIcon}>⚠</div>
            <p className={styles.errorHeading}>Couldn't load data</p>
            <p className={styles.errorDetail}>{error}</p>
            <button className={styles.retryBtn} onClick={refetch}>Try again</button>
          </div>
        )}

        {!loading && !error && visible.length === 0 && (
          <div className={styles.centred}>
            <p className={styles.emptyHeading}>No streaks match this filter</p>
            <p className={styles.emptyDetail}>
              Try a different league or streak type, or{' '}
              <button className={styles.inlineBtn} onClick={refetch}>refresh the data</button>.
            </p>
          </div>
        )}

        {!loading && !error && visible.length > 0 && (
          <div className={styles.grid}>
            {visible.map(streak => (
              <TeamCard
                key={`${streak.league}-${streak.team}`}
                streak={streak}
              />
            ))}
          </div>
        )}

      </main>

    </div>
  );
}
