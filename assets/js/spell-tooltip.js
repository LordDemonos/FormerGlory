(function () {
  const PQDI_URL = 'https://www.pqdi.cc';
  const spellCache = new Map();

  const tooltipContainer = document.createElement('div');
  tooltipContainer.id = 'spell-tooltip-container';
  tooltipContainer.className = 'pqdi-tooltip';
  tooltipContainer.setAttribute('aria-hidden', 'true');
  document.body.appendChild(tooltipContainer);

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function spellIdFromHref(href) {
    if (!href) {
      return null;
    }
    const parts = href.split('/');
    return parts[parts.length - 1] || null;
  }

  function spellLinkFromNode(node) {
    const el = node && node.nodeType === 1 ? node : node && node.parentElement;
    if (!el || !el.closest) {
      return null;
    }
    return el.closest('a[href^="https://www.pqdi.cc/spell/"]');
  }

  function loadSpell(spellId) {
    const cached = spellCache.get(spellId);
    if (cached) {
      return cached;
    }

    const request = fetch(`${PQDI_URL}/api/v1/spell/${spellId}`)
      .then(function (response) {
        if (!response.ok) {
          throw new Error('HTTP ' + response.status);
        }
        return response.json();
      })
      .then(function (data) {
        spellCache.set(spellId, Promise.resolve(data));
        return data;
      })
      .catch(function () {
        spellCache.delete(spellId);
        return null;
      });

    spellCache.set(spellId, request);
    return request;
  }

  function spellTooltipHtml(data) {
    const effects = Array.isArray(data.effects) ? data.effects : [];
    const effectHtml = effects
      .map(function (effect) {
        return '<div class="spell-effect">' + escapeHtml(effect) + '</div>';
      })
      .join('');

    return (
      '<div class="spell-tooltip">' +
      '<h4>' +
      escapeHtml(data.name) +
      '</h4>' +
      '<div class="spell-meta">' +
      '<div>Mana: ' +
      escapeHtml(data.mana) +
      '</div>' +
      '<div>Cast: ' +
      escapeHtml(data.casting_time) +
      's</div>' +
      '<div>Duration: ' +
      escapeHtml(data.duration) +
      '</div>' +
      '</div>' +
      '<div class="spell-effects">' +
      effectHtml +
      '</div>' +
      '</div>'
    );
  }

  if (typeof window.bindPqdiHoverTooltip !== 'function') {
    return;
  }

  window.bindPqdiHoverTooltip({
    container: tooltipContainer,
    findLink: spellLinkFromNode,
    parseId: function (link) {
      return spellIdFromHref(link.href);
    },
    isCached: function (spellId) {
      return spellCache.has(spellId);
    },
    load: loadSpell,
    render: function (link, data) {
      tooltipContainer.innerHTML = spellTooltipHtml(data);
    },
  });
})();
