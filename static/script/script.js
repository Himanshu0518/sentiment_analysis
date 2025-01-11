
about = document.getElementById("about") ;

function showSection(sectionId) {
    about.remove('active')
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active') ;
    });
    document.getElementById(sectionId).classList.add('active');
}


document.getElementById('upload-form').addEventListener('submit', async function (event) {
    event.preventDefault();
   
    const formData = new FormData(this);

    try {
      
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

       
        const data = await response.json();
        document.getElementById('wordcloud').src = 'data:image/png;base64,' + data.wordcloud;
        document.getElementById('pie-chart').src = 'data:image/png;base64,' + data.pie_chart;

    } catch (error) {
       
        console.error('Error:', error);
    }
});

document.getElementById('submit-custom-text').addEventListener('click', async function() {
    const customText = document.getElementById('custom-text').value;

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'custom-text': customText
            })
        });

        const data = await response.json();
        const positive = data.sentiment.positive;
        const negative = data.sentiment.negative;
        const neutral = data.sentiment.neutral;
        const compound = data.sentiment.compound ;
        let text = "";  
        if (compound > 0) {
            text = "Given statement is overall a positive statement";
        } else {
            text = "Given statement is overall a negative statement";
        }
      
        document.getElementById('sentiment').innerHTML = `
           <strong> result : ${text}</strong> <br>,
                 <br>
            Positive: ${positive} ,
            Negative: ${negative} ,
            Neutral: ${neutral} ,<br>
            overall_sentiment : ${compound} 

        `;

        const pieCtx = document.getElementById('myPieChart').getContext('2d');
        new Chart(pieCtx, {
            type: 'pie',
            data: {
                labels: ['Positive', 'Negative', 'Neutral'],
                datasets: [{
                    label: 'Sentiment Distribution',
                    data: [positive, negative, neutral],
                    backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe']
                }]
            },
            options: {
                responsive: false ,
                plugins: {
                    legend: {
                        position: 'top'
                    }
                }
            }
        });

    
        const barCtx = document.getElementById('myBarChart').getContext('2d');
        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: ['Positive', 'Negative', 'Neutral','compound'],
                datasets: [{
                    label: 'Sentiment Score',
                    data: [positive, negative, neutral , compound],
                    backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe' , '#40ff00']
                }]
            },
            options: {
                responsive: false ,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

    } catch (error) {
        console.error('Error:', error);
    }
});

document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();


    document.getElementById('spinner-upload').classList.remove('hidden');


    setTimeout(function() {
        
        document.getElementById('spinner-upload').classList.add('hidden');
      
        document.getElementById('file-results').style.display = 'block';
    }, 4000);  
});

document.getElementById('submit-custom-text').addEventListener('click', function() {
   
    document.getElementById('spinner-custom').classList.remove('hidden');

    setTimeout(function() {
        
        document.getElementById('spinner-custom').classList.add('hidden');
    
        document.getElementById('sentiment').innerText = 'Positive Sentiment';
    }, 3000);  
});

function showExplanation() {
    
    var explanations = document.querySelectorAll('.explanation');
    
    explanations.forEach(function(explanation) {
        explanation.style.display = 'block';
    });
}
