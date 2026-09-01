document.addEventListener('DOMContentLoaded', function () {
  const root = document.querySelector('[data-spell-focus]');
  if (!root) {
    return;
  }

  const classButtons = Array.from(root.querySelectorAll('button[data-class]'));
  const familyButtons = Array.from(root.querySelectorAll('button[data-family-filter]'));
  const slotButtons = Array.from(root.querySelectorAll('button[data-slot]'));
  const appliesButtons = Array.from(root.querySelectorAll('button[data-applies]'));
  const elementButtons = Array.from(root.querySelectorAll('button[data-element]'));
  const levelButtons = Array.from(root.querySelectorAll('button[data-level]'));
  const familyKeys = familyButtons.map(function (button) {
    return button.getAttribute('data-family-filter');
  });
  const items = Array.from(root.querySelectorAll('[data-focus-item]'));
  const ranks = Array.from(root.querySelectorAll('[data-rank]'));
  const effects = Array.from(root.querySelectorAll('[data-effect]'));
  const families = Array.from(root.querySelectorAll('[data-family]'));
  const expansions = Array.from(root.querySelectorAll('[data-expansion]'));
  const empty = root.querySelector('.raid-loot-empty');
  const countEl = root.querySelector('[data-focus-count]');
  const searchInput = root.querySelector('[data-focus-search]');
  const clearButton = root.querySelector('[data-focus-clear]');
  const moreFilters = root.querySelector('[data-more-filters]');
  const collapse = bindCatalogCollapse(root, { sectionSelector: '[data-expansion]' });
  catalogBindExpandControls(root, collapse);

  const defaults = {
    class: 'ALL',
    q: '',
    slot: 'ALL',
    family: 'ALL',
    applies: 'ALL',
    element: 'ALL',
    level: 'ALL',
  };
  const requestedFamily = catalogReadParam('family', 'ALL');
  const state = {
    className: catalogReadClass(),
    family: familyKeys.indexOf(requestedFamily) !== -1 ? requestedFamily : 'ALL',
    slot: catalogReadParam('slot', 'ALL'),
    applies: catalogReadParam('applies', 'ALL'),
    element: catalogReadParam('element', 'ALL'),
    level: catalogReadParam('level', 'ALL'),
    query: catalogReadParam('q', '').toLowerCase(),
  };

  function syncUrl() {
    catalogWriteClass(state.className);
    catalogReplaceParams(
      {
        class: state.className,
        q: state.query,
        slot: state.slot,
        family: state.family,
        applies: state.applies,
        element: state.element,
        level: state.level,
      },
      defaults
    );
  }

  function itemMatches(item, skipFamily) {
    if (state.className !== 'ALL') {
      const classes = (item.getAttribute('data-classes') || '').trim();
      if (classes && classes !== 'ALL' && !classes.split(/\s+/).includes(state.className)) {
        return false;
      }
    }

    if (state.slot !== 'ALL') {
      const slots = (item.getAttribute('data-slots') || '').trim();
      if (!slots.split(/\s+/).includes(state.slot)) {
        return false;
      }
    }

    if (state.applies !== 'ALL') {
      const applies = item.getAttribute('data-applies') || 'all';
      if (applies !== 'all' && applies !== state.applies) {
        return false;
      }
    }

    if (state.element !== 'ALL') {
      if ((item.getAttribute('data-element') || '') !== state.element) {
        return false;
      }
    }

    if (state.level !== 'ALL') {
      const maxLevel = Number(item.getAttribute('data-max-level') || 65);
      if (maxLevel < Number(state.level)) {
        return false;
      }
    }

    if (state.query) {
      const haystack = item.getAttribute('data-search') || '';
      if (!haystack.includes(state.query)) {
        return false;
      }
    }

    if (!skipFamily && state.family !== 'ALL' && familyKeyFor(item) !== state.family) {
      return false;
    }

    return true;
  }

  function familyKeyFor(item) {
    const family = item.closest('[data-family]');
    return family ? family.getAttribute('data-family-key') || '' : '';
  }

  function updateFamilyCounts() {
    familyButtons.forEach(function (button) {
      const key = button.getAttribute('data-family-filter');
      if (!key || key === 'ALL') {
        return;
      }

      let count = 0;
      items.forEach(function (item) {
        if (familyKeyFor(item) === key && itemMatches(item, true)) {
          count += 1;
        }
      });

      const countEl = button.querySelector('[data-family-count]');
      if (countEl) {
        countEl.textContent = String(count);
      }
      button.hidden = count === 0 && state.family !== key;
    });
  }

  function hasActiveFilters() {
    return (
      state.className !== 'ALL' ||
      state.family !== 'ALL' ||
      state.slot !== 'ALL' ||
      state.applies !== 'ALL' ||
      state.element !== 'ALL' ||
      state.level !== 'ALL' ||
      state.query !== ''
    );
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

    ranks.forEach((rank) => {
      const hasVisible = Array.from(rank.querySelectorAll('[data-focus-item]')).some((item) => !item.hidden);
      rank.hidden = !hasVisible;
    });

    effects.forEach((effect) => {
      const hasVisible = Array.from(effect.querySelectorAll('[data-rank]')).some((rank) => !rank.hidden);
      effect.hidden = !hasVisible;
    });

    families.forEach((family) => {
      const hasVisible = Array.from(family.querySelectorAll('[data-effect]')).some((effect) => !effect.hidden);
      family.hidden = !hasVisible;
    });

    expansions.forEach((expansion) => {
      const hasVisible = Array.from(expansion.querySelectorAll('[data-family]')).some((family) => !family.hidden);
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

    updateFamilyCounts();

    if (moreFilters) {
      moreFilters.open = state.applies !== 'ALL' || state.element !== 'ALL' || state.level !== 'ALL';
    }

    if (state.query || state.family !== 'ALL') {
      collapse.expandAll();
    }

    catalogSyncStickyOffset();
  }

  function bindGroup(buttons, attr, key) {
    buttons.forEach((button) => {
      button.addEventListener('click', function () {
        state[key] = button.getAttribute(attr) || 'ALL';
        catalogSyncButtons(buttons, attr, state[key]);
        syncUrl();
        applyFilter();
      });
    });
  }

  catalogSyncButtons(classButtons, 'data-class', state.className);
  catalogSyncButtons(familyButtons, 'data-family-filter', state.family);
  catalogSyncButtons(slotButtons, 'data-slot', state.slot);
  catalogSyncButtons(appliesButtons, 'data-applies', state.applies);
  catalogSyncButtons(elementButtons, 'data-element', state.element);
  catalogSyncButtons(levelButtons, 'data-level', state.level);
  if (searchInput) {
    searchInput.value = state.query;
  }

  bindGroup(classButtons, 'data-class', 'className');
  bindGroup(familyButtons, 'data-family-filter', 'family');
  bindGroup(slotButtons, 'data-slot', 'slot');
  bindGroup(appliesButtons, 'data-applies', 'applies');
  bindGroup(elementButtons, 'data-element', 'element');
  bindGroup(levelButtons, 'data-level', 'level');

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
      state.family = 'ALL';
      state.slot = 'ALL';
      state.applies = 'ALL';
      state.element = 'ALL';
      state.level = 'ALL';
      state.query = '';
      if (searchInput) {
        searchInput.value = '';
      }
      catalogSyncButtons(classButtons, 'data-class', 'ALL');
      catalogSyncButtons(familyButtons, 'data-family-filter', 'ALL');
      catalogSyncButtons(slotButtons, 'data-slot', 'ALL');
      catalogSyncButtons(appliesButtons, 'data-applies', 'ALL');
      catalogSyncButtons(elementButtons, 'data-element', 'ALL');
      catalogSyncButtons(levelButtons, 'data-level', 'ALL');
      syncUrl();
      applyFilter();
    });
  }

  syncUrl();
  applyFilter();
});
