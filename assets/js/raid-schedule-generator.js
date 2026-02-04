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
// Handles year boundaries correctly (e.g., if today is Jan 1 and date is Dec 25, assume it's Dec 25 of previous year)
function isDateInPast(date) {
    const today = new Date();
    const currentYear = today.getFullYear();
    
    // Try current year first
    let raidDate = new Date(currentYear, date.month - 1, date.day);
    
    // If the date is more than 6 months in the past, it's probably for next year
    // (e.g., if today is Jan 1 and date is Dec 25, Dec 25 is less than 6 months ago, so use current year)
    // (e.g., if today is Dec 25 and date is Jan 1, Jan 1 is more than 6 months ago, so use next year)
    const sixMonthsAgo = new Date(today.getFullYear(), today.getMonth() - 6, today.getDate());
    
    if (raidDate < sixMonthsAgo) {
        // Date is more than 6 months in the past, assume it's for next year
        raidDate = new Date(currentYear + 1, date.month - 1, date.day);
    }
    
    // Reset hours to compare just the dates (ignore time)
    today.setHours(0, 0, 0, 0);
    raidDate.setHours(0, 0, 0, 0);
    
    // Return true if the raid date is before today
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
    return `<div class="copy-text-container"><pre class="copy-text-content" id="${id}">&lt;Next Scheduled Raid&gt;${raidText} - Lv60+ to raid - Join us at FormerGlory.LOL</pre><button class="copy-button" onclick="copyText('${id}')">Copy to Clipboard</button></div>`;
}

// Function to generate copy-to-clipboard HTML for offnight raids
function generateOffnightCopyBlock(raidText) {
    const id = `copy-box-${Math.random().toString(36).substr(2, 9)}`;
    return `<div class="copy-text-container"><pre class="copy-text-content" id="${id}">&lt;Offnight Raid&gt;${raidText} - Lv60+ to raid - Join us at FormerGlory.LOL</pre><button class="copy-button" onclick="copyText('${id}')">Copy to Clipboard</button></div>`;
}

// Function to generate copy-to-clipboard HTML for static groups
function generateStaticGroupCopyBlock(raidText) {
    const id = `copy-box-${Math.random().toString(36).substr(2, 9)}`;
    return `<div class="copy-text-container"><pre class="copy-text-content" id="${id}">&lt;Static Group&gt;${raidText} - Lv60+ to raid - Join us at FormerGlory.LOL</pre><button class="copy-button" onclick="copyText('${id}')">Copy to Clipboard</button></div>`;
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
    const today = new Date();
    const todayStr = today.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    console.log(`\n📅 Today's date: ${todayStr}`);
    console.log(`🔄 Filtering out any raids before today (handles year boundaries automatically)`);
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
    let includedRegular = 0;
    let skippedRegular = 0;
    let includedOffnight = 0;
    let skippedOffnight = 0;
    
    // Process regular raids
    raids.forEach(raid => {
        const date = parseDate(raid);
        if (!date) {
            console.log(`⚠️  Skipping invalid date for raid: "${raid}"`);
            skippedRegular++;
            return;
        }
        if (isDateInPast(date)) {
            console.log(`⚠️  Skipping past date for raid: "${raid}"`);
            skippedRegular++;
            return;
        }
        
        includedRegular++;
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
            console.log(`⚠️  Skipping invalid date for offnight raid: "${raid}"`);
            skippedOffnight++;
            return;
        }
        if (isDateInPast(date)) {
            console.log(`⚠️  Skipping past date for offnight raid: "${raid}"`);
            skippedOffnight++;
            return;
        }
        
        includedOffnight++;
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

    console.log('\n📊 Processing Summary:');
    console.log(`   Regular raids: ${includedRegular} included, ${skippedRegular} skipped`);
    console.log(`   Offnight raids: ${includedOffnight} included, ${skippedOffnight} skipped`);
    console.log(`   Total included: ${includedRegular + includedOffnight}`);
    console.log(`   Total skipped: ${skippedRegular + skippedOffnight}`);
    console.log(`\n📅 Dates will be sorted chronologically regardless of input order`);
    console.log(`🗑️  Past dates (before ${todayStr}) are automatically filtered out`);
    
    if (skippedRegular + skippedOffnight > 0) {
        console.log('\n💡 Tip: Skipped raids are usually due to:');
        console.log(`   - Dates in the past (before ${todayStr})`);
        console.log('   - Invalid date format (must be MM/DD)');
    }

    // Generate TOC
    let toc = '## Table of Contents\n\n';

    // Generate content
    let mainContent = '';
    
    // Sort months chronologically by their earliest week's start date
    // This ensures proper ordering regardless of input order in raids.txt
    // and correctly handles year boundaries (e.g., December -> January of next year)
    const sortedMonths = Object.keys(organizedRaids).sort((a, b) => {
        // Get the earliest week start date for each month
        const weeksA = Object.values(organizedRaids[a]);
        const weeksB = Object.values(organizedRaids[b]);
        const earliestA = Math.min(...weeksA.map(w => w.weekStart.getTime()));
        const earliestB = Math.min(...weeksB.map(w => w.weekStart.getTime()));
        return earliestA - earliestB;
    });
    
    sortedMonths.forEach(month => {
        const monthName = new Date(2024, month - 1, 1).toLocaleString('default', { month: 'long' });
        mainContent += `\n## ${monthName}\n\n`;
        
        // Sort weeks by their start date (chronologically)
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
    // const calendarEmbed = `
    // <div class="calendar-container" style="margin: 20px 0;">
    // <iframe src="https://calendar.google.com/calendar/embed?src=66d83074080df7c55ea03673842f6e7b2c2f37ce0c38edf7137603c80e399802%40group.calendar.google.com&ctz=America%2FNew_York" 
    // style="border: 0" 
    // width="100%" 
    // height="600" 
    // frameborder="0" 
    // scrolling="no">
    // </iframe>
    // </div>
    // 
    // `;

    return content + toc + mainContent;
}

// Main function
function main() {
    const inputFile = path.join(__dirname, '..', 'data', 'raids.txt');
    const offnightFile = path.join(__dirname, '..', 'data', 'offnight.txt');
    let raids = [];
    let offnightRaids = [];
    let skippedLines = [];

    try {
        const content = fs.readFileSync(inputFile, 'utf8');
        const allLines = content.split('\n');
        console.log(`📖 Read ${allLines.length} lines from raids.txt`);
        
        raids = allLines
            .map((line, index) => ({ line: line.trim(), originalIndex: index + 1 }))
            .filter(({ line, originalIndex }) => {
                // Skip empty lines and comments
                if (line.length === 0 || line.startsWith('#') || line.startsWith('//')) {
                    return false;
                }
                // Accept lines that start with bullet points, dashes, or are plain text with dates
                const hasDate = line.startsWith('•') || line.startsWith('-') || line.match(/\d{1,2}\/\d{1,2}/);
                if (!hasDate) {
                    skippedLines.push(`Line ${originalIndex}: No date found - "${line}"`);
                }
                return hasDate;
            })
            .map(({ line }) => {
                // Remove bullet points or dashes if present
                if (line.startsWith('•') || line.startsWith('-')) {
                    return line.substring(1).trim();
                }
                return line;
            });
        
        console.log(`✅ Parsed ${raids.length} valid raid entries from raids.txt`);
        if (skippedLines.length > 0) {
            console.log(`⚠️  Skipped ${skippedLines.length} lines without dates:`);
            skippedLines.forEach(msg => console.log(`   ${msg}`));
        }
    } catch (error) {
        console.error('❌ Error reading raids.txt:', error.message);
        process.exit(1);
    }

    try {
        const offnightContent = fs.readFileSync(offnightFile, 'utf8');
        offnightRaids = offnightContent.split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0);
        console.log(`✅ Parsed ${offnightRaids.length} offnight raid entries`);
    } catch (error) {
        console.log('ℹ️  offnight.txt not found or empty (this is OK)');
    }

    const markdown = generateMarkdown(raids, offnightRaids);
    const outputFile = path.join(__dirname, '..', '..', 'raids.md');
    fs.writeFileSync(outputFile, markdown);
    console.log(`✅ Generated markdown file: ${outputFile}`);
    console.log(`📊 Generated ${markdown.split('\n').length} lines of markdown`);
}

main(); 
