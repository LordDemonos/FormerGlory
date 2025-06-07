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
    const raidDate = new Date(today.getFullYear(), date.month - 1, date.day);
    
    // Reset hours to compare just the dates
    today.setHours(0, 0, 0, 0);
    raidDate.setHours(0, 0, 0, 0);
    
    return raidDate < today;
}

// Function to get week range for a date
function getWeekRange(date) {
    const startDate = new Date(2024, date.month - 1, date.day);
    const dayOfWeek = startDate.getDay();
    const diff = startDate.getDate() - dayOfWeek;
    
    const weekStart = new Date(startDate.setDate(diff));
    const weekEnd = new Date(startDate.setDate(diff + 6));
    
    return {
        start: weekStart,
        end: weekEnd
    };
}

// Function to format date for display
function formatDate(date) {
    return `${date.getMonth() + 1}/${date.getDate()}`;
}

// Function to generate copy-to-clipboard HTML for regular raids
function generateCopyBlock(raidText) {
    const id = `copy-box-${Math.random().toString(36).substr(2, 9)}`;
    return `<div class="copy-text-container"><pre class="copy-text-content" id="${id}">&lt;Next Scheduled Raid&gt;${raidText} - Join us at formerglory.lol</pre><button class="copy-button" onclick="copyText('${id}')">Copy to Clipboard</button></div>`;
}

// Function to generate copy-to-clipboard HTML for offnight raids
function generateOffnightCopyBlock(raidText) {
    const id = `copy-box-${Math.random().toString(36).substr(2, 9)}`;
    return `<div class="copy-text-container"><pre class="copy-text-content" id="${id}">&lt;Offnight Raid&gt;${raidText} - Join us at formerglory.lol</pre><button class="copy-button" onclick="copyText('${id}')">Copy to Clipboard</button></div>`;
}

// Function to get raid date for sorting
function getRaidDate(raid) {
    const date = parseDate(raid) || parseOffnightDate(raid);
    if (!date) return null;
    return new Date(2024, date.month - 1, date.day);
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
        
        const weekRange = getWeekRange(date);
        const monthKey = date.month;
        const weekKey = `${formatDate(weekRange.start)} - ${formatDate(weekRange.end)}`;
        
        if (!organizedRaids[monthKey]) {
            organizedRaids[monthKey] = {};
        }
        if (!organizedRaids[monthKey][weekKey]) {
            organizedRaids[monthKey][weekKey] = {
                regular: [],
                offnight: []
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
        
        const weekRange = getWeekRange(date);
        const monthKey = date.month;
        const weekKey = `${formatDate(weekRange.start)} - ${formatDate(weekRange.end)}`;
        
        if (!organizedRaids[monthKey]) {
            organizedRaids[monthKey] = {};
        }
        if (!organizedRaids[monthKey][weekKey]) {
            organizedRaids[monthKey][weekKey] = {
                regular: [],
                offnight: []
            };
        }
        
        organizedRaids[monthKey][weekKey].offnight.push(raid);
    });

    console.log('Organized raids:', organizedRaids);

    // Generate TOC
    let toc = '## Table of Contents\n\n';

    // Generate content
    let mainContent = '';
    Object.keys(organizedRaids).sort((a, b) => a - b).forEach(month => {
        const monthName = new Date(2024, month - 1, 1).toLocaleString('default', { month: 'long' });
        mainContent += `\n## ${monthName}\n\n`;
        
        Object.keys(organizedRaids[month]).sort((a, b) => {
            const [aStart] = a.split(' - ');
            const [bStart] = b.split(' - ');
            return new Date(2024, month - 1, parseInt(aStart.split('/')[1])) - 
                   new Date(2024, month - 1, parseInt(bStart.split('/')[1]));
        }).forEach(week => {
            const anchor = `week-${month}-${week.replace(/[^0-9]/g, '-')}`;
            toc += `- [Week of ${week}](#${anchor})\n`;
            
            mainContent += `\n### Week of ${week} {#${anchor}}\n\n`;
            
            // Combine and sort all raids for this week
            const allRaids = [
                ...organizedRaids[month][week].offnight.map(raid => ({ type: 'offnight', raid })),
                ...organizedRaids[month][week].regular.map(raid => ({ type: 'regular', raid }))
            ].sort((a, b) => {
                const dateA = getRaidDate(a.raid);
                const dateB = getRaidDate(b.raid);
                return dateA - dateB;
            });
            
            // Output sorted raids
            allRaids.forEach(({ type, raid }) => {
                if (type === 'offnight') {
                    mainContent += generateOffnightCopyBlock(raid) + '\n\n';
                } else {
                    mainContent += generateCopyBlock(raid) + '\n\n';
                }
            });
        });
    });

    return content + toc + '\n' + mainContent;
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
            .filter(line => line.startsWith('•'))
            .map(line => line.substring(1).trim());
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
    const outputFile = path.join(__dirname, '..', 'raids.md');
    fs.writeFileSync(outputFile, markdown);
    console.log(`Generated markdown file: ${outputFile}`);
}

main(); 