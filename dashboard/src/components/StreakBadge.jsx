import React from 'react';
import styles from './StreakBadge.module.css';

const TYPE_META = {
  win:  { label: 'WIN STREAK',  var: '--win',  dimVar: '--win-dim'  },
  draw: { label: 'DRAW STREAK', var: '--draw', dimVar: '--draw-dim' },
  loss: { label: 'LOSS STREAK', var: '--loss', dimVar: '--loss-dim' },
};

export default function StreakBadge({ type, length }) {
  const meta = TYPE_META[type] || TYPE_META.draw;
  return (
    <div
      className={styles.badge}
      style={{
        '--badge-color':  `var(${meta.var})`,
        '--badge-bg':     `var(${meta.dimVar})`,
      }}
    >
      <span className={styles.number}>{length}</span>
      <span className={styles.label}>{meta.label}</span>
    </div>
  );
}
