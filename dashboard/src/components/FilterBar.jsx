import React from 'react';
import styles from './FilterBar.module.css';

const TYPES = [
  { code: 'ALL',  label: 'All' },
  { code: 'win',  label: 'Win'  },
  { code: 'draw', label: 'Draw' },
  { code: 'loss', label: 'Loss' },
];

const SORTS = [
  { code: 'length_desc', label: 'Longest first'  },
  { code: 'length_asc',  label: 'Shortest first' },
  { code: 'date_desc',   label: 'Most recent'    },
  { code: 'alpha',       label: 'A → Z'          },
];

export default function FilterBar({ typeFilter, onTypeFilter, sort, onSort, onRefresh, loading, lastFetched }) {
  const timeStr = lastFetched
    ? lastFetched.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })
    : null;

  return (
    <div className={styles.bar}>
      {/* Streak type pills */}
      <div className={styles.pills} role="group" aria-label="Filter by streak type">
        {TYPES.map(({ code, label }) => (
          <button
            key={code}
            className={`${styles.pill} ${typeFilter === code ? styles[`active_${code}`] || styles.activePill : ''}`}
            onClick={() => onTypeFilter(code)}
            aria-pressed={typeFilter === code}
          >
            {label}
          </button>
        ))}
      </div>

      <div className={styles.right}>
        {/* Sort select */}
        <select
          className={styles.select}
          value={sort}
          onChange={e => onSort(e.target.value)}
          aria-label="Sort order"
        >
          {SORTS.map(({ code, label }) => (
            <option key={code} value={code}>{label}</option>
          ))}
        </select>

        {/* Refresh */}
        <button
          className={`${styles.refreshBtn} ${loading ? styles.spinning : ''}`}
          onClick={onRefresh}
          disabled={loading}
          aria-label="Refresh data"
          title={timeStr ? `Last updated ${timeStr}` : 'Refresh'}
        >
          <RefreshIcon />
          {timeStr && <span className={styles.timeStr}>{timeStr}</span>}
        </button>
      </div>
    </div>
  );
}

function RefreshIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <path d="M13.65 2.35A8 8 0 1 0 15 8h-2a6 6 0 1 1-1.05-3.4L10 6h4V2l-0.35 0.35Z"
        fill="currentColor"/>
    </svg>
  );
}
