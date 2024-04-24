function fetchCurrentModel() {
    // Fetch and display models
    fetch('/models/activate')
        .then(response => response.json())
        .then(data => {
//            document.getElementById('modelName').textContent = "Model Name: " + data.model;
            const modelDisplay = document.getElementById('current-model');
            modelDisplay.textContent = data.model;
            modelDisplay.style.backgroundColor = getRandomColor();
            fetchModels();
        })
        .catch(error => {
            console.error('Error loading models:', error);
            document.getElementById('current-model').textContent = 'Failed to load current model';
        });
};

function fetchModels() {
    fetch('models')
        .then(response => response.json())
        .then(lst => {
            const select = document.getElementById('model-select');
            select.innerHTML = ''; // Clear existing options
            lst.forEach(model => {
                let option = new Option(model);
                select.appendChild(option);
            });
            select.onchange = changeModel;
        })
        .catch(error => {
            console.error('Error fetching model data:', error);
        });
};

function changeModel() {
    const newModel = this.value;
    fetch('/models/activate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({model: newModel})
    })
    .then(fetchCurrentModel)
    .catch(error => {
        console.error('Error updating model:', error);
    })
}

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}


window.onload = fetchCurrentModel;
