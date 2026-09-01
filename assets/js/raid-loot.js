document.addEventListener('DOMContentLoaded', function () {
  const root = document.querySelector('[data-raid-loot]');
  if (!root) {
    return;
  }

  const classButtons = Array.from(root.querySelectorAll('button[data-class]'));
  const items = Array.from(root.querySelectorAll('[data-loot-item]'));
  const tables = Array.from(root.querySelectorAll('[data-loot-table]'));
  const bosses = Array.from(root.querySelectorAll('[data-boss]'));
  const zones = Array.from(root.querySelectorAll('[data-zone]'));
  const expansions = Array.from(root.querySelectorAll('[data-expansion]'));
  const empty = root.querySelector('.raid-loot-empty');
  const countEl = root.querySelector('[data-loot-count]');
  const searchInput = root.querySelector('[data-loot-search]');
  const clearButton = root.querySelector('[data-loot-clear]');
  const retiredToggle = root.querySelector('[data-retired-toggle]');
  const collapse = bindCatalogCollapse(root, { sectionSelector: '[data-expansion]' });
  catalogBindExpandControls(root, collapse);

  const defaults = { class: 'ALL', q: '', retired: '0' };
  const state = {
    className: catalogReadClass(),
    query: catalogReadParam('q', '').toLowerCase(),
    hideRetired: catalogReadParam('retired', '0') !== '1',
  };

  function syncUrl() {
    catalogWriteClass(state.className);
    catalogReplaceParams(
      {
        class: state.className,
        q: state.query,
        retired: state.hideRetired ? '0' : '1',
      },
      defaults
    );
  }

  function itemMatches(item) {
    if (state.hideRetired && item.getAttribute('data-retired') === '1') {
      return false;
    }

    if (state.className !== 'ALL') {
      const classes = (item.getAttribute('data-classes') || '').trim();
      if (classes && classes !== 'ALL' && !classes.split(/\s+/).includes(state.className)) {
        return false;
      }
    }

    if (state.query) {
      const haystack = item.getAttribute('data-search') || '';
      if (!haystack.includes(state.query)) {
        return false;
      }
    }

    return true;
  }

  function hasActiveFilters() {
    return state.className !== 'ALL' || state.query !== '' || !state.hideRetired;
  }

  function applyFilter() {
    let visibleCount = 0;

    items.forEach((item) => {
      const show = itemMatches(item);
      item.hidden = !show;
      if (show) {
        visibleCount += 1;
      }
    });

    tables.forEach((table) => {
      const hasVisible = Array.from(table.querySelectorAll('[data-loot-item]')).some((item) => !item.hidden);
      table.hidden = !hasVisible;
    });

    bosses.forEach((boss) => {
      const hasVisible = Array.from(boss.querySelectorAll('[data-loot-item]')).some((item) => !item.hidden);
      boss.hidden = !hasVisible;
    });

    zones.forEach((zone) => {
      const hasVisible = Array.from(zone.querySelectorAll('[data-boss]')).some((boss) => !boss.hidden);
      zone.hidden = !hasVisible;
    });

    expansions.forEach((expansion) => {
      const hasVisible = Array.from(expansion.querySelectorAll('[data-zone]')).some((zone) => !zone.hidden);
      expansion.hidden = !hasVisible;
    });

    catalogHideToc(root);

    if (empty) {
      empty.hidden = visibleCount > 0;
    }

    if (countEl) {
      countEl.textContent = visibleCount + (visibleCount === 1 ? ' item' : ' items');
    }

    if (clearButton) {
      clearButton.hidden = !hasActiveFilters();
    }

    if (retiredToggle) {
      retiredToggle.classList.toggle('is-active', state.hideRetired);
    }

    if (state.query) {
      collapse.expandAll();
    }

    catalogSyncStickyOffset();
  }

  catalogSyncButtons(classButtons, 'data-class', state.className);
  if (searchInput) {
    searchInput.value = state.query;
  }

  classButtons.forEach((button) => {
    button.addEventListener('click', function () {
      state.className = button.getAttribute('data-class') || 'ALL';
      catalogSyncButtons(classButtons, 'data-class', state.className);
      syncUrl();
      applyFilter();
    });
  });

  if (retiredToggle) {
    retiredToggle.addEventListener('click', function () {
      state.hideRetired = !state.hideRetired;
      syncUrl();
      applyFilter();
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', function () {
      state.query = searchInput.value.trim().toLowerCase();
      syncUrl();
      applyFilter();
    });
  }

  if (clearButton) {
    clearButton.addEventListener('click', function () {
      state.className = 'ALL';
      state.query = '';
      state.hideRetired = true;
      if (searchInput) {
        searchInput.value = '';
      }
      catalogSyncButtons(classButtons, 'data-class', 'ALL');
      syncUrl();
      applyFilter();
    });
  }

  syncUrl();
  applyFilter();
});
