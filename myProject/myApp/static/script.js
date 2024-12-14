
setInterval(() => {
    fetch('/live_data/')
        .then(response => response.json())
        .then(data => {
            // Update usage
            document.getElementById('fridge-usage').textContent = `${data.Fridge} kWh`;
            document.getElementById('ac-usage').textContent = `${data.AC} kWh`;
            document.getElementById('tv-usage').textContent = `${data.TV} kWh`;

            // Update tips
            const tipsList = document.getElementById('energy-tips');
            tipsList.innerHTML = ''; // Clear previous tips
            data.Tips.forEach(tip => {
                const li = document.createElement('li');
                li.textContent = tip;
                li.className = 'list-group-item';
                tipsList.appendChild(li);
            });
        });
}, 5000);

