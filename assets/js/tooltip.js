(function () {
  const HOVER_DELAY_MS = 90;

  function hidePqdiTooltips(except) {
    document.querySelectorAll('.pqdi-tooltip').forEach(function (el) {
      if (el !== except) {
        el.style.display = 'none';
        el.innerHTML = '';
      }
    });
  }

  function placeTooltip(container, x, y) {
    const pad = 14;
    const rect = container.getBoundingClientRect();
    let left = x + pad;
    let top = y + pad;
    if (left + rect.width > window.innerWidth - 8) {
      left = Math.max(8, x - rect.width - pad);
    }
    if (top + rect.height > window.innerHeight - 8) {
      top = Math.max(8, window.innerHeight - rect.height - 8);
    }
    container.style.left = left + window.scrollX + 'px';
    container.style.top = top + window.scrollY + 'px';
  }

  window.bindPqdiHoverTooltip = function bindPqdiHoverTooltip(options) {
    const container = options.container;
    const findLink = options.findLink;
    const parseId = options.parseId;
    const isCached = options.isCached;
    const load = options.load;
    const render = options.render;
    const delayMs = options.delayMs == null ? HOVER_DELAY_MS : options.delayMs;

    let hoverTimer = null;
    let pendingLink = null;
    let activeLink = null;
    let activeId = null;
    let lastPointer = { x: 0, y: 0 };

    function hide() {
      pendingLink = null;
      activeLink = null;
      activeId = null;
      container.style.display = 'none';
    }

    function showFor(link) {
      const id = parseId(link);
      if (!id) {
        return;
      }

      pendingLink = null;
      activeLink = link;
      activeId = id;

      load(id).then(function (payload) {
        if (!payload || activeId !== id || activeLink !== link) {
          return;
        }
        hidePqdiTooltips(container);
        render(link, payload);
        container.style.display = 'block';
        placeTooltip(container, lastPointer.x, lastPointer.y);
      });
    }

    document.addEventListener('mouseover', function (event) {
      const link = findLink(event.target);
      if (!link || link === activeLink || link === pendingLink) {
        return;
      }

      lastPointer = { x: event.clientX, y: event.clientY };
      pendingLink = link;
      clearTimeout(hoverTimer);

      const id = parseId(link);
      const delay = id && isCached(id) ? 0 : delayMs;
      hoverTimer = setTimeout(function () {
        showFor(link);
      }, delay);
    });

    document.addEventListener('mousemove', function (event) {
      lastPointer = { x: event.clientX, y: event.clientY };
      if (container.style.display === 'block') {
        placeTooltip(container, event.clientX, event.clientY);
      }
    });

    document.addEventListener('mouseout', function (event) {
      const link = findLink(event.target);
      if (!link) {
        return;
      }

      const next = findLink(event.relatedTarget);
      if (next === link) {
        return;
      }

      if (pendingLink === link) {
        pendingLink = null;
      }
      clearTimeout(hoverTimer);

      if (next) {
        return;
      }

      if (activeLink === link) {
        hide();
      }
    });
  };
})();

(function () {
  const SPRITE_SHEET_WIDTH = 640;
  const SPRITE_SHEET_HEIGHT = 480;
  const ICON_SIZE = 40;
  const PQDI_URL = 'https://www.pqdi.cc';
  const FALLBACK_URL = 'https://lorddemonos.github.io/static/icons/';

  const tooltipCache = new Map();

  const tooltipContainer = document.createElement('div');
  tooltipContainer.id = 'tooltip-container';
  tooltipContainer.className = 'pqdi-tooltip';
  tooltipContainer.setAttribute('aria-hidden', 'true');
  document.body.appendChild(tooltipContainer);

  function itemIdFromHref(href) {
    if (!href) {
      return null;
    }
    const parts = href.split('/');
    return parts[parts.length - 1] || null;
  }

  function itemLinkFromNode(node) {
    const el = node && node.nodeType === 1 ? node : node && node.parentElement;
    if (!el || !el.closest) {
      return null;
    }
    const link = el.closest('a[href^="https://www.pqdi.cc/item/"]');
    if (link) {
      return link;
    }
    if (el.classList && el.classList.contains('item-icon')) {
      const next = el.nextElementSibling;
      if (next && next.matches && next.matches('a[href^="https://www.pqdi.cc/item/"]')) {
        return next;
      }
    }
    return null;
  }

  function loadTooltip(itemId) {
    const cached = tooltipCache.get(itemId);
    if (cached) {
      return cached;
    }

    const request = fetch(`${PQDI_URL}/get-item-tooltip/${itemId}`)
      .then(function (response) {
        if (!response.ok) {
          throw new Error(String(response.status));
        }
        return response.text();
      })
      .then(function (html) {
        tooltipCache.set(itemId, Promise.resolve(html));
        return html;
      })
      .catch(function () {
        tooltipCache.delete(itemId);
        return null;
      });

    tooltipCache.set(itemId, request);
    return request;
  }

  function applyIcon(link, html) {
    if (link.querySelector('.item-icon')) {
      return;
    }

    const sibling = link.previousElementSibling;
    if (sibling && sibling.classList.contains('item-icon')) {
      link.insertBefore(sibling, link.firstChild);
      return;
    }

    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    const iconSpan = tempDiv.querySelector('.item-icon');
    if (!iconSpan) {
      return;
    }

    const urlMatch = (iconSpan.style.backgroundImage || '').match(/url\(["']?([^"']*)["']?\)/);
    if (!urlMatch) {
      return;
    }

    const itemId = itemIdFromHref(link.href);
    const backgroundPath = urlMatch[1];
    const fullImageUrl = backgroundPath.indexOf('http') === 0 ? backgroundPath : PQDI_URL + backgroundPath;
    const newIconSpan = document.createElement('span');
    newIconSpan.className = 'item-icon';
    newIconSpan.style.backgroundImage = `url("${fullImageUrl}")`;
    newIconSpan.style.backgroundRepeat = 'no-repeat';
    newIconSpan.style.display = 'inline-block';
    newIconSpan.style.verticalAlign = 'middle';
    newIconSpan.style.width = '1em';
    newIconSpan.style.height = '1em';
    newIconSpan.style.marginRight = '0.25em';
    if (iconSpan.title) {
      newIconSpan.title = iconSpan.title;
    }

    const img = new Image();
    img.src = fullImageUrl;
    img.onerror = function () {
      newIconSpan.style.backgroundImage = `url("${FALLBACK_URL}item_${itemId}.png")`;
      newIconSpan.style.backgroundSize = 'contain';
      newIconSpan.style.backgroundPosition = 'center';
    };

    const match = (iconSpan.style.backgroundPosition || '').match(/(-?\d+)px\s+(-?\d+)px/);
    if (match) {
      const scaleFactor = 1 / ICON_SIZE;
      const scaledX = parseInt(match[1], 10) * scaleFactor;
      const scaledY = parseInt(match[2], 10) * scaleFactor;
      newIconSpan.style.backgroundPosition = `${scaledX}em ${scaledY}em`;
      newIconSpan.style.backgroundSize =
        `${SPRITE_SHEET_WIDTH * scaleFactor}em ${SPRITE_SHEET_HEIGHT * scaleFactor}em`;
    } else {
      newIconSpan.style.backgroundSize = 'contain';
    }

    link.insertBefore(newIconSpan, link.firstChild);
  }

  function prepareTooltipHtml(html) {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    tempDiv.querySelectorAll('script').forEach(function (script) {
      script.remove();
    });
    tempDiv.querySelectorAll('td').forEach(function (td) {
      if (!td.textContent.trim()) {
        td.remove();
      }
    });
    tempDiv.querySelectorAll('tr').forEach(function (tr) {
      if (!tr.textContent.trim()) {
        tr.remove();
      }
    });

    tempDiv.querySelectorAll('*').forEach(function (element) {
      const backgroundImage = element.style.backgroundImage;
      if (
        backgroundImage &&
        backgroundImage.indexOf('url("http') !== 0 &&
        backgroundImage.indexOf("url('http") !== 0 &&
        backgroundImage.indexOf('url(http') !== 0
      ) {
        const match = backgroundImage.match(/url\(["']?([^"']*)["']?\)/);
        if (match) {
          element.style.backgroundImage = `url("${PQDI_URL}${match[1]}")`;
        }
      }
      if (element.hasAttribute('src')) {
        const src = element.getAttribute('src');
        if (src && src.indexOf('http') !== 0 && src.indexOf('data:') !== 0) {
          element.setAttribute('src', PQDI_URL + src);
        }
      }
    });

    return tempDiv.innerHTML;
  }

  window.bindPqdiHoverTooltip({
    container: tooltipContainer,
    findLink: itemLinkFromNode,
    parseId: function (link) {
      return itemIdFromHref(link.href);
    },
    isCached: function (itemId) {
      return tooltipCache.has(itemId);
    },
    load: loadTooltip,
    render: function (link, html) {
      if (!link.classList.contains('tooltip-link')) {
        link.classList.add('tooltip-link');
        link.setAttribute('data-item-id', itemIdFromHref(link.href));
      }
      applyIcon(link, html);
      tooltipContainer.innerHTML = prepareTooltipHtml(html);
    },
  });
})();
