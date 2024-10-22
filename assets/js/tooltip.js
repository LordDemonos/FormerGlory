document.addEventListener('DOMContentLoaded', function () {
  const BASE_URL = 'https://www.pqdi.cc'; // Set the base URL for the images
  const SPRITE_SHEET_WIDTH = 640;
  const SPRITE_SHEET_HEIGHT = 480;
  const ICON_SIZE = 40;

  const tooltipContainer = document.createElement('div');
  tooltipContainer.id = 'tooltip-container';
  document.body.appendChild(tooltipContainer);

  let hideTooltipTimeout;

  document.querySelectorAll('a[href*="pqdi.cc/item/"]').forEach((link) => {
    const urlParts = link.href.split('/');
    const itemId = urlParts[urlParts.length - 1];
    link.classList.add('tooltip-link');
    link.setAttribute('data-item-id', itemId);

    // Tooltip functionality
    link.addEventListener('mouseenter', function (event) {
      clearTimeout(hideTooltipTimeout);
      const linkRect = link.getBoundingClientRect();
      const linkTop = linkRect.top + window.scrollY;
      const linkBottom = linkRect.bottom + window.scrollY;
      const linkLeft = linkRect.left + window.scrollX;

      fetch(`${BASE_URL}/get-item-tooltip/${itemId}`)
        .then((response) => response.text())
        .then((html) => {
          const tempDiv = document.createElement('div');
          tempDiv.innerHTML = html;

          tempDiv.querySelectorAll('script').forEach(script => script.remove());

          tempDiv.querySelectorAll('td').forEach(td => {
            if (!td.textContent.trim()) td.remove();
          });
          tempDiv.querySelectorAll('tr').forEach(tr => {
            if (!tr.textContent.trim()) tr.remove();
          });

          tooltipContainer.innerHTML = tempDiv.innerHTML;
          tooltipContainer.style.left = `${linkLeft}px`;
          tooltipContainer.style.top = `${linkBottom + 5}px`;
          tooltipContainer.style.display = 'block';

          const tooltipRect = tooltipContainer.getBoundingClientRect();
          if (tooltipRect.bottom > window.innerHeight) {
            tooltipContainer.style.top = `${linkTop - tooltipRect.height - 5}px`;
          }
        });
    });

    link.addEventListener('mouseleave', function () {
      hideTooltipTimeout = setTimeout(() => {
        tooltipContainer.style.display = 'none';
      }, 300);
    });

    // Icon functionality
    fetch(`${BASE_URL}/get-item-tooltip/${itemId}`)
      .then((response) => response.text())
      .then((html) => {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        const iconSpan = tempDiv.querySelector('.item-icon');
        if (iconSpan) {
          const newIconSpan = document.createElement('span');
          newIconSpan.classList.add('item-icon');
          newIconSpan.style.backgroundImage = iconSpan.style.backgroundImage;
          console.log('Background Image URL:', newIconSpan.style.backgroundImage); // Log the URL
          newIconSpan.style.display = 'inline-block';
          newIconSpan.style.verticalAlign = 'middle';
          newIconSpan.style.width = '1em';
          newIconSpan.style.height = '1em';
          newIconSpan.style.marginRight = '0.25em';
          newIconSpan.title = iconSpan.title;

          const match = iconSpan.style.backgroundPosition.match(/(-?\d+)px\s+(-?\d+)px/);
          if (match) {
            const [, x, y] = match;
            const originalX = parseInt(x);
            const originalY = parseInt(y);

            const scaleFactor = 1 / ICON_SIZE;

            const scaledX = originalX * scaleFactor;
            const scaledY = originalY * scaleFactor;

            newIconSpan.style.backgroundPosition = `${scaledX}em ${scaledY}em`;

            const scaledSheetWidth = SPRITE_SHEET_WIDTH * scaleFactor;
            const scaledSheetHeight = SPRITE_SHEET_HEIGHT * scaleFactor;
            newIconSpan.style.backgroundSize = `${scaledSheetWidth}em ${scaledSheetHeight}em`;
          }

          link.parentNode.insertBefore(newIconSpan, link);
        }
      });
  });
});
