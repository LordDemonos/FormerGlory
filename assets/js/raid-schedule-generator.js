const fs = require('fs');
const path = require('path');

// Function to parse date from raid schedule line
function parseDate(line) {
    const dateMatch = line.match(/(\d{1,2})\/(\d{1,2})/);
    if (!dateMatch) return null;
    
    const [_, month, day] = dateMatch;
    return {
        month: parseInt(month),
        day: parseInt(day)
    };
}

// Function to parse date from offnight schedule line
function parseOffnightDate(line) {
    const dateMatch = line.match(/(\d{1,2})\/(\d{1,2})/);
    if (!dateMatch) return null;
    
    const [_, month, day] = dateMatch;
    return {
        month: parseInt(month),
        day: parseInt(day)
    };
}

// Function to check if a date is in the past
function isDateInPast(date) {
    const today = new Date();
    const currentYear = today.getFullYear();
    const raidDate = new Date(currentYear, date.month - 1, date.day);
    
    // If the raid date is in the past, it might be for next year
    if (raidDate < today) {
        raidDate.setFullYear(currentYear + 1);
    }
    
    // Reset hours to compare just the dates
    today.setHours(0, 0, 0, 0);
    raidDate.setHours(0, 0, 0, 0);
    
    return raidDate < today;
}

// Function to get week range for a date
function getWeekRange(date) {
    const currentYear = new Date().getFullYear();
    const baseDate = new Date(currentYear, date.month - 1, date.day);

    // Clone baseDate for weekStart
    const weekStart = new Date(baseDate);
    // Set weekStart to the previous Sunday (or the same day if it's Sunday)
    weekStart.setDate(baseDate.getDate() - baseDate.getDay());

    // Clone weekStart for weekEnd
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 6);

    return {
        start: weekStart,
        end: weekEnd
    };
}

// Function to format date for display
function formatDate(date) {
    return `${date.getMonth() + 1}/${date.getDate()}`;
}

// Function to get week key that properly handles cross-month weeks
function getWeekKey(date) {
    const weekRange = getWeekRange(date);
    const startMonth = weekRange.start.getMonth() + 1;
    const endMonth = weekRange.end.getMonth() + 1;
    
    // If the week spans two months, use the month where the week starts
    const displayMonth = startMonth;
    const startDate = formatDate(weekRange.start);
    const endDate = formatDate(weekRange.end);
    
    return {
        monthKey: displayMonth,
        weekKey: `${startDate} - ${endDate}`,
        weekStart: weekRange.start
    };
}

// Function to generate copy-to-clipboard HTML for regular raids
function generateCopyBlock(raidText) {
    const id = `copy-box-${Math.random().toString(36).substr(2, 9)}`;
    return `<div class="copy-text-container"><pre class="copy-text-content" id="${id}">&lt;Next Scheduled Raid&gt;${raidText} - Lv55+ to raid - Join us at FormerGlory.LOL</pre><button class="copy-button" onclick="copyText('${id}')">Copy to Clipboard</button></div>`;
}

// Function to generate copy-to-clipboard HTML for offnight raids
function generateOffnightCopyBlock(raidText) {
    const id = `copy-box-${Math.random().toString(36).substr(2, 9)}`;
    return `<div class="copy-text-container"><pre class="copy-text-content" id="${id}">&lt;Offnight Raid&gt;${raidText} - Lv55+ to raid - Join us at FormerGlory.LOL</pre><button class="copy-button" onclick="copyText('${id}')">Copy to Clipboard</button></div>`;
}

// Function to generate copy-to-clipboard HTML for static groups
function generateStaticGroupCopyBlock(raidText) {
    const id = `copy-box-${Math.random().toString(36).substr(2, 9)}`;
    return `<div class="copy-text-container"><pre class="copy-text-content" id="${id}">&lt;Static Group&gt;${raidText} - Lv55+ to raid - Join us at FormerGlory.LOL</pre><button class="copy-button" onclick="copyText('${id}')">Copy to Clipboard</button></div>`;
}

// Function to check if an entry is a static group
function isStaticGroup(raidText) {
    return raidText.toLowerCase().includes('hosted by');
}

// Function to get raid date for sorting
function getRaidDate(raid) {
    const date = parseDate(raid) || parseOffnightDate(raid);
    if (!date) return null;
    
    const currentYear = new Date().getFullYear();
    const today = new Date();
    
    // For September-November dates, assume they're for the current year
    // unless they're clearly in the past (more than 6 months ago)
    let raidDate = new Date(currentYear, date.month - 1, date.day);
    
    // If the raid date is more than 6 months in the past, it's probably for next year
    const sixMonthsAgo = new Date(today.getFullYear(), today.getMonth() - 6, today.getDate());
    if (raidDate < sixMonthsAgo) {
        raidDate = new Date(currentYear + 1, date.month - 1, date.day);
    }
    
    return raidDate;
}

// Function to generate markdown content
function generateMarkdown(raids, offnightRaids) {
    console.log('Processing raids:', raids);
    console.log('Processing offnight raids:', offnightRaids);

    // Add front matter
    let content = `---
resize_images: true
layout: page
title: Raid Schedule
subtitle: Guild Message of the Day
cover-img: /assets/img/raids.webp
---

`;

    // Group raids by month and week
    const organizedRaids = {};
    
    // Process regular raids
    raids.forEach(raid => {
        const date = parseDate(raid);
        if (!date) {
            console.log('Skipping invalid date for raid:', raid);
            return;
        }
        if (isDateInPast(date)) {
            console.log('Skipping past date for raid:', raid);
            return;
        }
        
        const weekInfo = getWeekKey(date);
        const monthKey = weekInfo.monthKey;
        const weekKey = weekInfo.weekKey;
        
        if (!organizedRaids[monthKey]) {
            organizedRaids[monthKey] = {};
        }
        if (!organizedRaids[monthKey][weekKey]) {
            organizedRaids[monthKey][weekKey] = {
                regular: [],
                offnight: [],
                static: [],
                weekStart: weekInfo.weekStart
            };
        }
        
        organizedRaids[monthKey][weekKey].regular.push(raid);
    });

    // Process offnight raids
    offnightRaids.forEach(raid => {
        const date = parseOffnightDate(raid);
        if (!date) {
            console.log('Skipping invalid date for offnight raid:', raid);
            return;
        }
        if (isDateInPast(date)) {
            console.log('Skipping past date for offnight raid:', raid);
            return;
        }
        
        const weekInfo = getWeekKey(date);
        const monthKey = weekInfo.monthKey;
        const weekKey = weekInfo.weekKey;
        
        if (!organizedRaids[monthKey]) {
            organizedRaids[monthKey] = {};
        }
        if (!organizedRaids[monthKey][weekKey]) {
            organizedRaids[monthKey][weekKey] = {
                regular: [],
                offnight: [],
                static: [],
                weekStart: weekInfo.weekStart
            };
        }
        
        // Check if this is a static group or offnight raid
        if (isStaticGroup(raid)) {
            organizedRaids[monthKey][weekKey].static.push(raid);
        } else {
            organizedRaids[monthKey][weekKey].offnight.push(raid);
        }
    });

    console.log('Organized raids:', organizedRaids);

    // Generate TOC
    let toc = '## Table of Contents\n\n';

    // Generate content
    let mainContent = '';
    Object.keys(organizedRaids).sort((a, b) => a - b).forEach(month => {
        const monthName = new Date(2024, month - 1, 1).toLocaleString('default', { month: 'long' });
        mainContent += `\n## ${monthName}\n\n`;
        
        // Sort weeks by their start date
        Object.keys(organizedRaids[month]).sort((a, b) => {
            const weekA = organizedRaids[month][a];
            const weekB = organizedRaids[month][b];
            return weekA.weekStart - weekB.weekStart;
        }).forEach(week => {
            const anchor = `week-${month}-${week.replace(/[^0-9]/g, '-')}`;
            toc += `- [Week of ${week}](#${anchor})\n`;
            
            mainContent += `\n### Week of ${week} {#${anchor}}\n\n`;
            
            // Combine and sort all raids for this week
            const allRaids = [
                ...organizedRaids[month][week].offnight.map(raid => ({ type: 'offnight', raid })),
                ...organizedRaids[month][week].regular.map(raid => ({ type: 'regular', raid })),
                ...organizedRaids[month][week].static.map(raid => ({ type: 'static', raid }))
            ].sort((a, b) => {
                const dateA = getRaidDate(a.raid);
                const dateB = getRaidDate(b.raid);
                return dateA - dateB;
            });
            
            // Output sorted raids
            allRaids.forEach(({ type, raid }) => {
                if (type === 'offnight') {
                    mainContent += generateOffnightCopyBlock(raid) + '\n\n';
                } else if (type === 'static') {
                    mainContent += generateStaticGroupCopyBlock(raid) + '\n\n';
                } else {
                    mainContent += generateCopyBlock(raid) + '\n\n';
                }
            });
        });
    });

    // Add calendar embed after TOC
    const calendarEmbed = `
<div class="calendar-container" style="margin: 20px 0;">
<iframe src="https://calendar.google.com/calendar/embed?src=66d83074080df7c55ea03673842f6e7b2c2f37ce0c38edf7137603c80e399802%40group.calendar.google.com&ctz=America%2FNew_York" 
style="border: 0" 
width="100%" 
height="600" 
frameborder="0" 
scrolling="no">
</iframe>
</div>

`;

    return content + toc + calendarEmbed + mainContent;
}

// Main function
function main() {
    const inputFile = path.join(__dirname, '..', 'data', 'raids.txt');
    const offnightFile = path.join(__dirname, '..', 'data', 'offnight.txt');
    let raids = [];
    let offnightRaids = [];

    try {
        const content = fs.readFileSync(inputFile, 'utf8');
        raids = content.split('\n')
            .map(line => line.trim())
            .filter(line => {
                // Skip empty lines and comments
                if (line.length === 0 || line.startsWith('#') || line.startsWith('//')) {
                    return false;
                }
                // Accept lines that start with bullet points, dashes, or are plain text with dates
                return line.startsWith('•') || line.startsWith('-') || line.match(/\d{1,2}\/\d{1,2}/);
            })
            .map(line => {
                // Remove bullet points or dashes if present
                if (line.startsWith('•') || line.startsWith('-')) {
                    return line.substring(1).trim();
                }
                return line;
            });
    } catch (error) {
        console.error('Error reading raids.txt:', error.message);
        process.exit(1);
    }

    try {
        const offnightContent = fs.readFileSync(offnightFile, 'utf8');
        offnightRaids = offnightContent.split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0);
    } catch (error) {
        // It's ok if offnight.txt doesn't exist
    }

    const markdown = generateMarkdown(raids, offnightRaids);
    const outputFile = path.join(__dirname, '..', '..', 'raids.md');
    fs.writeFileSync(outputFile, markdown);
    console.log(`Generated markdown file: ${outputFile}`);
}

main(); 