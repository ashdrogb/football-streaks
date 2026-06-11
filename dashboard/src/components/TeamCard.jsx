import React, { useState } from 'react';
import FormTape from './FormTape';
import StreakBadge from './StreakBadge';
import styles from './TeamCard.module.css';

function CrestImg({ src, alt, size = 40 }) {
  const [errored, setErrored] = useState(false);
  if (!src || errored) {
    return (
      <div className={styles.crestFallback} style={{ width: size, height: size }}>
        {alt?.[0] ?? '?'}
      </div>
    );
  }
  return (
    <img
      src={src}
      alt={alt}
      width={size}
      height={size}
      className={styles.crest}
      onError={() => setErrored(true)}
    />
  );
}

/**
 * streak shape:
 *   league, team, team_id, crest_url,
 *   streak_type, streak_length,
 *   last_opponent, last_opponent_crest, match_date
 *
 * We synthesise a `results` array from streak_type + streak_length
 * because the API only sends the current streak, not full form history.
 * If the backend is later extended to send form[], we can pass it directly.
 */
function buildSyntheticForm(type, length) {
  const code = type === 'win' ? 'W' : type === 'loss' ? 'L' : 'D';
  return Array(Math.min(length, 5)).fill(code);
}

export default function TeamCard({ streak }) {
  const {
    league, team, crest_url,
    streak_type, streak_length,
    last_opponent, last_opponent_crest, match_date,
  } = streak;

  const results    = buildSyntheticForm(streak_type, streak_length);
  const displayDate = match_date
    ? new Date(match_date).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
    : '—';

  return (
    <article className={`${styles.card} ${styles[streak_type]}`}>

      {/* Top row: crest + name + badge */}
      <div className={styles.header}>
        <CrestImg src={crest_url} alt={team} size={44} />
        <div className={styles.teamInfo}>
          <h3 className={styles.teamName}>{team}</h3>
          <span className={styles.leagueTag}>{league}</span>
        </div>
        <StreakBadge type={streak_type} length={streak_length} />
      </div>

      {/* Form tape */}
      <div className={styles.tapeRow}>
        <span className={styles.tapeLabel}>FORM</span>
        <FormTape results={results} activeCount={Math.min(streak_length, 5)} />
        {streak_length > 5 && (
          <span className={styles.moreCount}>+{streak_length - 5}</span>
        )}
      </div>

      {/* Last match */}
      <div className={styles.matchRow}>
        <div className={styles.matchVs}>
          <span className={styles.vsLabel}>Last vs</span>
          <CrestImg src={last_opponent_crest} alt={last_opponent} size={20} />
          <span className={styles.opponentName}>{last_opponent}</span>
        </div>
        <span className={styles.matchDate}>{displayDate}</span>
      </div>

    </article>
  );
}
