import React from 'react';
import styles from './LeagueTabs.module.css';

export default function LeagueTabs({ leagues, active, onChange, counts }) {
  const all = { name: 'All Leagues', code: 'ALL' };
  const tabs = [all, ...leagues];

  return (
    <nav className={styles.nav} aria-label="Filter by league">
      <div className={styles.scroller}>
        {tabs.map(({ name, code }) => {
          const count  = code === 'ALL' ? counts.total : (counts[code] ?? 0);
          const isActive = active === code;
          return (
            <button
              key={code}
              className={`${styles.tab} ${isActive ? styles.activeTab : ''}`}
              onClick={() => onChange(code)}
              aria-pressed={isActive}
            >
              <span className={styles.name}>{name}</span>
              {count > 0 && (
                <span className={`${styles.count} ${isActive ? styles.activeCount : ''}`}>
                  {count}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
}
