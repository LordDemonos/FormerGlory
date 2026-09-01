const CATALOG_CLASS_KEY = 'fg-catalog-class';
const CATALOG_CLASSES = [
  'ALL',
  'WAR',
  'CLR',
  'PAL',
  'RNG',
  'SHD',
  'DRU',
  'MNK',
  'BRD',
  'ROG',
  'SHM',
  'NEC',
  'WIZ',
  'MAG',
  'ENC',
  'BST',
];

function catalogQuery() {
  return new URLSearchParams(location.search);
}

function catalogReplaceParams(values, defaults) {
  const params = catalogQuery();
  Object.keys(values).forEach(function (key) {
    const value = values[key];
    const fallback = defaults[key];
    if (value == null || value === '' || value === fallback) {
      params.delete(key);
    } else {
      params.set(key, String(value));
    }
  });
  const query = params.toString();
  history.replaceState(null, '', location.pathname + (query ? '?' + query : '') + location.hash);
}

function catalogReadParam(key, fallback) {
  const value = catalogQuery().get(key);
  return value == null || value === '' ? fallback : value;
}

function catalogReadClass() {
  const fromUrl = (catalogReadParam('class', '') || '').toUpperCase();
  if (CATALOG_CLASSES.indexOf(fromUrl) !== -1) {
    catalogWriteClass(fromUrl);
    return fromUrl;
  }

  try {
    const stored = (localStorage.getItem(CATALOG_CLASS_KEY) || '').toUpperCase();
    if (CATALOG_CLASSES.indexOf(stored) !== -1) {
      return stored;
    }
  } catch (err) {
    /* ignore */
  }

  return 'ALL';
}

function catalogWriteClass(className) {
  try {
    localStorage.setItem(CATALOG_CLASS_KEY, className);
  } catch (err) {
    /* ignore */
  }
}

function catalogSyncButtons(buttons, attr, value) {
  buttons.forEach(function (button) {
    button.classList.toggle('is-active', (button.getAttribute(attr) || 'ALL') === value);
  });
}

function catalogHideToc(root) {
  root.querySelectorAll('.raid-loot-toc a').forEach(function (link) {
    const id = (link.getAttribute('href') || '').replace(/^#/, '');
    const heading = id ? document.getElementById(id) : null;
    const section = heading ? heading.closest('[data-expansion]') || heading : null;
    link.hidden = !section || section.hidden;
  });

  root.querySelectorAll('.raid-loot-boss-toc').forEach(function (toc) {
    const links = Array.from(toc.querySelectorAll('a'));
    links.forEach(function (link) {
      const id = (link.getAttribute('href') || '').replace(/^#/, '');
      const target = id ? document.getElementById(id) : null;
      if (!target) {
        link.hidden = true;
        return;
      }
      const block = target.closest('[data-boss], [data-group], [data-effect], [data-family]');
      link.hidden = Boolean(target.hidden || (block && block.hidden));
    });
    toc.hidden = !links.some(function (link) {
      return !link.hidden;
    });
  });
}

function catalogBindExpandControls(root, collapse) {
  const expand = root.querySelector('[data-expand-all]');
  const collapseBtn = root.querySelector('[data-collapse-all]');
  if (expand) {
    expand.addEventListener('click', function () {
      collapse.expandAll();
    });
  }
  if (collapseBtn) {
    collapseBtn.addEventListener('click', function () {
      collapse.collapseAll();
    });
  }
}

function catalogCopy(button, text) {
  const original = button.textContent;
  function markCopied() {
    button.textContent = 'Copied';
    window.setTimeout(function () {
      button.textContent = original;
    }, 1500);
  }

  function fallback() {
    const field = document.createElement('textarea');
    field.value = text;
    field.setAttribute('readonly', '');
    field.style.position = 'fixed';
    field.style.left = '-9999px';
    document.body.appendChild(field);
    field.select();
    try {
      document.execCommand('copy');
      markCopied();
    } catch (err) {
      button.textContent = original;
    }
    document.body.removeChild(field);
  }

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(markCopied).catch(fallback);
    return;
  }

  fallback();
}

function catalogSyncStickyOffset() {
  const nav = document.querySelector('.navbar-custom');
  const chrome = document.querySelector('.catalog-chrome');
  if (!chrome) {
    return;
  }

  const navHeight = nav ? nav.getBoundingClientRect().height : 56;
  chrome.style.top = navHeight + 'px';
  const margin = navHeight + chrome.getBoundingClientRect().height + 12;
  document.documentElement.style.setProperty('--catalog-scroll-margin', margin + 'px');
}

document.addEventListener('DOMContentLoaded', function () {
  catalogSyncStickyOffset();
  const more = document.querySelector('[data-more-filters]');
  if (more) {
    more.addEventListener('toggle', catalogSyncStickyOffset);
  }
  window.addEventListener('resize', catalogSyncStickyOffset);
});
