import React from 'react';
import styles from './FormTape.module.css';

const RESULT_META = {
  W: { label: 'W', color: 'var(--win)',  title: 'Win'  },
  D: { label: 'D', color: 'var(--draw)', title: 'Draw' },
  L: { label: 'L', color: 'var(--loss)', title: 'Loss' },
};

/**
 * Renders a horizontal strip of coloured result pills.
 * `results` is an array like ["L","L","L","W","D"] — index 0 = most recent.
 * `activeCount` dims results beyond the active streak.
 */
export default function FormTape({ results = [], activeCount = 0 }) {
  return (
    <div className={styles.tape} aria-label={`Form: ${results.join(' ')}`}>
      {results.map((r, i) => {
        const meta    = RESULT_META[r] || RESULT_META.D;
        const isActive = i < activeCount;
        return (
          <span
            key={i}
            className={`${styles.pip} ${isActive ? styles.active : styles.dim}`}
            style={{ '--pip-color': meta.color }}
            title={`${i === 0 ? 'Latest: ' : ''}${meta.title}`}
          >
            {meta.label}
          </span>
        );
      })}
    </div>
  );
}
