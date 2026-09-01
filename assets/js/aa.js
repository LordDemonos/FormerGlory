document.addEventListener('DOMContentLoaded', function () {
  const root = document.querySelector('[data-aa-guide]');
  if (!root) {
    return;
  }

  const classButtons = Array.from(root.querySelectorAll('button[data-class]'));
  const abilities = Array.from(root.querySelectorAll('[data-aa]'));
  const activates = Array.from(root.querySelectorAll('[data-aa-activate]'));
  const groups = Array.from(root.querySelectorAll('[data-group]'));
  const expansions = Array.from(root.querySelectorAll('[data-expansion]'));
  const empty = root.querySelector('.raid-loot-empty');
  const countEl = root.querySelector('[data-aa-count]');
  const searchInput = root.querySelector('[data-aa-search]');
  const clearButton = root.querySelector('[data-aa-clear]');
  const collapse = bindCatalogCollapse(root, { sectionSelector: '[data-expansion]' });
  catalogBindExpandControls(root, collapse);

  const defaults = { class: 'ALL', q: '' };
  const state = {
    className: catalogReadClass(),
    query: catalogReadParam('q', '').toLowerCase(),
  };

  function syncUrl() {
    catalogWriteClass(state.className);
    catalogReplaceParams(
      {
        class: state.className,
        q: state.query,
      },
      defaults
    );
  }

  function classMatch(classes, label) {
    if (state.className === 'ALL') {
      return true;
    }
    if (classes) {
      const tokens = classes.trim();
      if (!tokens || tokens === 'ALL') {
        return true;
      }
      return tokens.split(/\s+/).includes(state.className);
    }
    if (!label) {
      return true;
    }
    return label.includes(state.className);
  }

  function queryMatch(search) {
    if (!state.query) {
      return true;
    }
    return (search || '').includes(state.query);
  }

  function hasActiveFilters() {
    return state.className !== 'ALL' || state.query !== '';
  }

  function applyFilter() {
    let visibleCount = 0;

    abilities.forEach((ability) => {
      const show = classMatch(ability.getAttribute('data-classes') || '', '') && queryMatch(ability.getAttribute('data-search') || '');
      ability.hidden = !show;
      if (show) {
        visibleCount += 1;
      }
    });

    activates.forEach((row) => {
      const show = classMatch('', row.getAttribute('data-classes-label') || '') && queryMatch(row.getAttribute('data-search') || '');
      row.hidden = !show;
    });

    groups.forEach((group) => {
      const hasVisible = Array.from(group.querySelectorAll('[data-aa]')).some((ability) => !ability.hidden);
      group.hidden = !hasVisible;
    });

    expansions.forEach((expansion) => {
      const hasAbility = Array.from(expansion.querySelectorAll('[data-aa]')).some((ability) => !ability.hidden);
      const hasActivate = Array.from(expansion.querySelectorAll('[data-aa-activate]')).some((row) => !row.hidden);
      expansion.hidden = !hasAbility && !hasActivate;
    });

    catalogHideToc(root);

    if (empty) {
      empty.hidden = visibleCount > 0 || activates.some((row) => !row.hidden);
    }

    if (countEl) {
      countEl.textContent = visibleCount + (visibleCount === 1 ? ' AA' : ' AAs');
    }

    if (clearButton) {
      clearButton.hidden = !hasActiveFilters();
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
      if (searchInput) {
        searchInput.value = '';
      }
      catalogSyncButtons(classButtons, 'data-class', 'ALL');
      syncUrl();
      applyFilter();
    });
  }

  root.querySelectorAll('[data-copy-activate]').forEach((button) => {
    button.addEventListener('click', function () {
      catalogCopy(button, button.getAttribute('data-copy-activate') || '');
    });
  });

  syncUrl();
  applyFilter();
});
