function bindCatalogCollapse(root, options) {
  const sectionSelector = (options && options.sectionSelector) || '[data-expansion]';
  const sections = Array.from(root.querySelectorAll(sectionSelector));
  const nested = Array.from(root.querySelectorAll('[data-family], [data-group]'));
  const tocLinks = Array.from(root.querySelectorAll('.raid-loot-toc a'));

  function caretFor(section) {
    return section.querySelector(':scope > .raid-loot-heading > [data-collapse-toggle]');
  }

  function hashId() {
    return decodeURIComponent((location.hash || '').replace(/^#/, ''));
  }

  function sectionForId(id) {
    if (!id) {
      return null;
    }

    const target = document.getElementById(id);
    if (!target) {
      return null;
    }

    if (target.matches(sectionSelector)) {
      return target;
    }

    return target.closest(sectionSelector);
  }

  function setOpen(section, open) {
    section.classList.toggle('is-collapsed', !open);
    const caret = caretFor(section);
    if (caret) {
      caret.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
  }

  function openAncestors(id) {
    const target = document.getElementById(id);
    if (!target) {
      return;
    }

    const family = target.closest('[data-family]');
    const group = target.closest('[data-group]');
    if (family) {
      setOpen(family, true);
    }
    if (group) {
      setOpen(group, true);
    }
  }

  function applyNavAccordion() {
    const target = sectionForId(hashId());
    const accordion = Boolean(target);

    sections.forEach((section) => {
      setOpen(section, !accordion || section === target);
    });

    tocLinks.forEach((link) => {
      const section = sectionForId((link.getAttribute('href') || '').replace(/^#/, ''));
      link.classList.toggle('is-active', accordion && section === target);
    });

    openAncestors(hashId());
  }

  function expandAll() {
    sections.forEach((section) => {
      setOpen(section, true);
    });
    nested.forEach((section) => {
      setOpen(section, true);
    });
    tocLinks.forEach((link) => {
      link.classList.remove('is-active');
    });
  }

  function collapseAll() {
    sections.forEach((section) => {
      setOpen(section, false);
    });
    tocLinks.forEach((link) => {
      link.classList.remove('is-active');
    });
    if (location.hash) {
      history.replaceState(null, '', location.pathname + location.search);
    }
  }

  function scrollToHash() {
    if (typeof catalogSyncStickyOffset === 'function') {
      catalogSyncStickyOffset();
    }
    const target = document.getElementById(hashId());
    if (target) {
      target.scrollIntoView();
    }
  }

  function bindCaret(section) {
    const caret = caretFor(section);
    if (!caret || caret.dataset.collapseBound) {
      return;
    }

    caret.dataset.collapseBound = '1';
    caret.addEventListener('click', function (event) {
      event.preventDefault();
      event.stopPropagation();
      setOpen(section, section.classList.contains('is-collapsed'));
    });
  }

  sections.forEach(bindCaret);
  nested.forEach(bindCaret);

  if (typeof catalogSyncStickyOffset === 'function') {
    catalogSyncStickyOffset();
  }

  window.addEventListener('hashchange', function () {
    applyNavAccordion();
    requestAnimationFrame(scrollToHash);
  });

  if (location.hash) {
    applyNavAccordion();
    requestAnimationFrame(scrollToHash);
  }

  return {
    applyNavAccordion: applyNavAccordion,
    expandAll: expandAll,
    collapseAll: collapseAll,
    setOpen: setOpen,
    sections: sections,
  };
}
