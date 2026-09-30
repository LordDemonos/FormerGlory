(function () {
  var root = document.getElementById('spell-turnins-board');
  if (!root) {
    return;
  }

  var poolsUrl = root.getAttribute('data-pools');
  var boardUrl = root.getAttribute('data-board');

  function itemNoun(item) {
    return item === 'glyph' ? 'Glyph' : 'Parchment';
  }

  function itemFull(item) {
    return item === 'glyph' ? 'Glyphed Rune Words' : 'Spectral Parchments';
  }

  function modeOf(board, item) {
    return item === 'glyph' ? board.glyphMode : board.parchmentMode;
  }

  function classesWithItem(catalog, item) {
    return catalog.classOrder.filter(function (className) {
      return catalog.pools.some(function (pool) {
        return pool.item === item && pool.class === className;
      });
    });
  }

  function securedCount(board, item, className, spell) {
    return board.drops.filter(function (drop) {
      return drop.item === item && drop.class === className && drop.spell === spell && drop.result === 'secured';
    }).length;
  }

  function openCopies(board, item, className) {
    return board.priorities.filter(function (priority) {
      return priority.item === item && priority.class === className;
    }).reduce(function (sum, priority) {
      return sum + Math.max(0, priority.want - securedCount(board, item, className, priority.spell));
    }, 0);
  }

  function turninCount(board, item, className) {
    return board.drops.filter(function (drop) {
      return drop.item === item && drop.class === className;
    }).length;
  }

  function nextClass(board, catalog, item) {
    var mode = modeOf(board, item);
    if (mode === 'equal') {
      var equalClasses = classesWithItem(catalog, item);
      if (equalClasses.length === 0) {
        return { type: 'unmarked' };
      }
      var bestEqual = equalClasses[0];
      var bestCount = turninCount(board, item, bestEqual);
      equalClasses.slice(1).forEach(function (className) {
        var count = turninCount(board, item, className);
        if (count < bestCount) {
          bestEqual = className;
          bestCount = count;
        }
      });
      return { type: 'class', className: bestEqual };
    }
    var marked = board.priorities.some(function (priority) {
      return priority.item === item;
    });
    if (!marked) {
      return { type: 'unmarked' };
    }
    var best = null;
    var bestOpen = 0;
    catalog.priorityClasses.forEach(function (className) {
      var open = openCopies(board, item, className);
      if (open > bestOpen) {
        best = className;
        bestOpen = open;
      }
    });
    if (!best) {
      return { type: 'dkp' };
    }
    return { type: 'class', className: best };
  }

  function nextText(board, catalog, item) {
    var advice = nextClass(board, catalog, item);
    if (advice.type === 'class') {
      return 'Next: ' + advice.className + '.';
    }
    if (advice.type === 'unmarked') {
      return 'No next class yet. Mark the spells the raid needs. The next ' + itemNoun(item).toLowerCase() + ' goes to the class with the most of those still short.';
    }
    return 'Coverage is full. DKP ' + itemFull(item) + '.';
  }

  function spellsFor(catalog, item, className) {
    var seen = {};
    return catalog.pools.filter(function (pool) {
      if (pool.item !== item || pool.class !== className || seen[pool.spell]) {
        return false;
      }
      seen[pool.spell] = true;
      return true;
    });
  }

  function findPriority(board, item, className, spell) {
    for (var i = 0; i < board.priorities.length; i++) {
      var priority = board.priorities[i];
      if (priority.item === item && priority.class === className && priority.spell === spell) {
        return priority;
      }
    }
    return null;
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function renderItem(board, catalog, item) {
    var mode = modeOf(board, item);
    var html = '<h2>' + escapeHtml(itemFull(item)) + '</h2>';
    html += '<p><strong>' + (mode === 'equal' ? 'Equal' : 'Priority') + '.</strong> ' + escapeHtml(nextText(board, catalog, item)) + '</p>';
    if (mode === 'equal') {
      html += '<table><thead><tr><th>Class</th><th>Turn-ins</th></tr></thead><tbody>';
      classesWithItem(catalog, item).forEach(function (className) {
        html += '<tr><td>' + escapeHtml(className) + '</td><td>' + turninCount(board, item, className) + '</td></tr>';
      });
      html += '</tbody></table>';
    }
    catalog.priorityClasses.forEach(function (className) {
      var spells = spellsFor(catalog, item, className);
      if (spells.length === 0) {
        return;
      }
      html += '<h3>' + escapeHtml(className) + '</h3>';
      html += '<p>' + escapeHtml(spells[0].librarian) + '. Each turn-in is 1/' + spells.length + '.</p>';
      html += '<table><thead><tr><th>Spell</th><th>Copies</th></tr></thead><tbody>';
      spells.forEach(function (pool) {
        var priority = findPriority(board, item, className, pool.spell);
        var copies = priority
          ? securedCount(board, item, className, pool.spell) + '/' + priority.want
          : '—';
        html += '<tr><td>' + escapeHtml(pool.spell) + '</td><td>' + copies + '</td></tr>';
      });
      html += '</tbody></table>';
    });
    return html;
  }

  function renderLog(board) {
    var html = '<h2>Recent drops</h2>';
    if (!board.drops.length) {
      return html + '<p>No drops recorded yet.</p>';
    }
    var recent = board.drops.slice(-8).reverse();
    html += '<table><thead><tr><th>Item</th><th>Class</th><th>Spell</th><th>Result</th></tr></thead><tbody>';
    recent.forEach(function (drop) {
      html += '<tr><td>' + escapeHtml(itemNoun(drop.item)) + '</td><td>' + escapeHtml(drop.class) + '</td><td>' + escapeHtml(drop.spell) + '</td><td>' + escapeHtml(drop.result) + '</td></tr>';
    });
    html += '</tbody></table>';
    return html;
  }

  Promise.all([
    fetch(poolsUrl).then(function (response) { return response.json(); }),
    fetch(boardUrl).then(function (response) { return response.json(); })
  ]).then(function (files) {
    var catalog = files[0];
    var board = files[1];
    root.innerHTML = renderItem(board, catalog, 'glyph') + renderItem(board, catalog, 'parchment') + renderLog(board);
  }).catch(function () {
    root.textContent = 'The board could not be loaded.';
  });
})();
