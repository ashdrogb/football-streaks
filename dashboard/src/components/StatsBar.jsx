import React from 'react';
import styles from './StatsBar.module.css';

export default function StatsBar({ streaks }) {
  const wins  = streaks.filter(s => s.streak_type === 'win').length;
  const draws = streaks.filter(s => s.streak_type === 'draw').length;
  const losses= streaks.filter(s => s.streak_type === 'loss').length;
  const longest = streaks.length ? Math.max(...streaks.map(s => s.streak_length)) : 0;
  const longestTeam = streaks.find(s => s.streak_length === longest);

  return (
    <div className={styles.bar}>
      <Stat label="Teams tracked" value={streaks.length} color="var(--cyan)" />
      <Stat label="Win streaks"  value={wins}   color="var(--win)"  />
      <Stat label="Draw streaks" value={draws}  color="var(--draw)" />
      <Stat label="Loss streaks" value={losses} color="var(--loss)" />
      {longestTeam && (
        <div className={styles.longest}>
          <span className={styles.longestLabel}>Longest streak</span>
          <span className={styles.longestValue} style={{ color: 'var(--cyan)' }}>
            {longest} — {longestTeam.team}
          </span>
        </div>
      )}
    </div>
  );
}

function Stat({ label, value, color }) {
  return (
    <div className={styles.stat}>
      <span className={styles.statVal} style={{ color }}>{value}</span>
      <span className={styles.statLabel}>{label}</span>
    </div>
  );
}
