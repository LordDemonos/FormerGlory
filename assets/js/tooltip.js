document.addEventListener('DOMContentLoaded', function () {
  const SPRITE_SHEET_WIDTH = 640;
  const SPRITE_SHEET_HEIGHT = 480;
  const ICON_SIZE = 40;
  const PQDI_URL = 'https://www.pqdi.cc';

  const tooltipContainer = document.createElement('div');
  tooltipContainer.id = 'tooltip-container';
  document.body.appendChild(tooltipContainer);

  let hideTooltipTimeout;

  document.querySelectorAll('a[href*="pqdi.cc/item/"]').forEach((link) => {
    const urlParts = link.href.split('/');
    const itemId = urlParts[urlParts.length - 1];
    link.classList.add('tooltip-link');
    link.setAttribute('data-item-id', itemId);

    // Immediately load the icon
    fetch(`${PQDI_URL}/get-item-tooltip/${itemId}`)
      .then((response) => response.text())
      .then((html) => {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        const iconSpan = tempDiv.querySelector('.item-icon');
        if (iconSpan && !link.previousElementSibling?.classList.contains('item-icon')) {
          const newIconSpan = document.createElement('span');
          newIconSpan.classList.add('item-icon');
          
          // Extract the relative URL from the original background image
          const backgroundImageUrl = iconSpan.style.backgroundImage.match(/url\(["']?([^"']*)["']?\)/)[1];
          
          // Construct the full URL using PQDI_URL
          const fullImageUrl = `${PQDI_URL}${backgroundImageUrl}`;
          newIconSpan.style.backgroundImage = `url("${fullImageUrl}")`;
          
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

    // Cache for tooltip data
    let tooltipData = null;

    // Tooltip functionality
    link.addEventListener('mouseenter', function (event) {
      clearTimeout(hideTooltipTimeout);
      const linkRect = link.getBoundingClientRect();
      const linkTop = linkRect.top + window.scrollY;
      const linkBottom = linkRect.bottom + window.scrollY;
      const linkLeft = linkRect.left + window.scrollX;

      if (!tooltipData) {
        fetch(`${PQDI_URL}/get-item-tooltip/${itemId}`)
          .then((response) => response.text())
          .then((html) => {
            tooltipData = html;
            processTooltipData(html);
          });
      } else {
        processTooltipData(tooltipData);
      }

      function processTooltipData(html) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;

        tempDiv.querySelectorAll('script').forEach(script => script.remove());
        tempDiv.querySelectorAll('td').forEach(td => {
          if (!td.textContent.trim()) td.remove();
        });
        tempDiv.querySelectorAll('tr').forEach(tr => {
          if (!tr.textContent.trim()) tr.remove();
        });

        // Handle all elements with background images
        tempDiv.querySelectorAll('*').forEach(element => {
          const backgroundImage = element.style.backgroundImage;
          if (backgroundImage && !backgroundImage.startsWith('url("http')) {
            const match = backgroundImage.match(/url\(["']?([^"']*)["']?\)/);
            if (match) {
              const relativeUrl = match[1];
              element.style.backgroundImage = `url("${PQDI_URL}${relativeUrl}")`;
            }
          }
          if (element.hasAttribute('src')) {
            const src = element.getAttribute('src');
            if (!src.startsWith('http')) {
              element.setAttribute('src', `${PQDI_URL}${src}`);
            }
          }
        });

        tooltipContainer.innerHTML = tempDiv.innerHTML;
        tooltipContainer.style.left = `${linkLeft}px`;
        tooltipContainer.style.top = `${linkBottom + 5}px`;
        tooltipContainer.style.display = 'block';

        const tooltipRect = tooltipContainer.getBoundingClientRect();
        if (tooltipRect.bottom > window.innerHeight) {
          tooltipContainer.style.top = `${linkTop - tooltipRect.height - 5}px`;
        }
      }
    });

    link.addEventListener('mouseleave', function () {
      hideTooltipTimeout = setTimeout(() => {
        tooltipContainer.style.display = 'none';
      }, 300);
    });
  });
});
