// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    window.openTab = function(evt, tabName) {
        const tabContents = document.getElementsByClassName('tab-content');
        for (let i = 0; i < tabContents.length; i++) {
            tabContents[i].classList.remove('active');
        }

        const tabButtons = document.getElementsByClassName('tab-btn');
        for (let i = 0; i < tabButtons.length; i++) {
            tabButtons[i].classList.remove('active');
        }

        document.getElementById(tabName).classList.add('active');
        evt.currentTarget.classList.add('active');
    };

    // File input handling
    const fileInput = document.getElementById('file-upload');
    const fileLabel = document.getElementById('file-name');

    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            fileLabel.textContent = this.files[0].name;
        } else {
            fileLabel.textContent = 'Choose file';
        }
    });

    // Text analysis form submission
    const textForm = document.getElementById('text-form');
    textForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const textInput = document.getElementById('custom-text').value;
        if (!textInput.trim()) {
            alert('Please enter some text to analyze');
            return;
        }

        const formData = new FormData(textForm);
        
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            
            displayTextResults(data.sentiment);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });

    // File analysis form submission
    const uploadForm = document.getElementById('upload-form');
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('file-upload');
        if (!fileInput.files || fileInput.files.length === 0) {
            alert('Please select a CSV file to upload');
            return;
        }

        // Show loading spinner
        document.getElementById('loading').classList.remove('hidden');
        document.getElementById('file-results').classList.add('hidden');
        
        const formData = new FormData(uploadForm);
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading spinner
            document.getElementById('loading').classList.add('hidden');
            
            if (data.error) {
                alert(data.error);
                return;
            }
            
            displayFileResults(data);
        })
        .catch(error => {
            document.getElementById('loading').classList.add('hidden');
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });

    // Display text analysis results
    function displayTextResults(sentiment) {
        const resultsContainer = document.getElementById('text-results');
        resultsContainer.classList.remove('hidden');

        // Update score bars and values
        updateScoreBar('positive', sentiment.positive);
        updateScoreBar('negative', sentiment.negative);
        updateScoreBar('neutral', sentiment.neutral);
        
        // Update compound score
        document.getElementById('compound-value').textContent = sentiment.compound.toFixed(2);
        
        // Determine overall sentiment based on compound score
        let overallSentiment;
        let sentimentColor;
        
        if (sentiment.compound >= 0.05) {
            overallSentiment = 'Positive';
            sentimentColor = 'var(--positive-color)';
        } else if (sentiment.compound <= -0.05) {
            overallSentiment = 'Negative';
            sentimentColor = 'var(--negative-color)';
        } else {
            overallSentiment = 'Neutral';
            sentimentColor = 'var(--neutral-color)';
        }
        
        const overallElement = document.getElementById('overall-sentiment');
        overallElement.textContent = overallSentiment;
        overallElement.style.color = sentimentColor;
        
        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }

    // Update score bar width and text
    function updateScoreBar(type, value) {
        const percentage = Math.round(value * 100);
        const bar = document.getElementById(`${type}-score`);
        const valueText = document.getElementById(`${type}-value`);
        
        bar.style.width = `${percentage}%`;
        valueText.textContent = `${percentage}%`;
    }

    // Display file analysis results
    function displayFileResults(data) {
        const resultsContainer = document.getElementById('file-results');
        resultsContainer.classList.remove('hidden');
        
        // Update charts with data URLs
        document.getElementById('pie-chart').src = `data:image/png;base64,${data.pie_chart}`;
        document.getElementById('wordcloud').src = `data:image/png;base64,${data.wordcloud}`;
        
        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }
});