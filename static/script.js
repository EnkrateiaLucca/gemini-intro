document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const storyInput = document.getElementById('storyInput');
    const statusMessage = document.getElementById('statusMessage');
    const storyboard = document.getElementById('storyboard');

    generateBtn.addEventListener('click', async () => {
        const story = storyInput.value.trim();
        if (!story) {
            alert('Please enter a story first.');
            return;
        }

        // Reset UI
        generateBtn.disabled = true;
        storyboard.innerHTML = '';
        storyboard.style.display = 'none';
        statusMessage.textContent = 'Generating 6 frame descriptions...';
        statusMessage.style.color = '#333';

        try {
            // 1. Generate descriptions
            const descResponse = await fetch('/api/generate_descriptions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ story })
            });

            const descData = await descResponse.json();

            if (!descResponse.ok) {
                throw new Error(descData.error || 'Failed to generate descriptions');
            }

            const prompts = descData.prompts;
            if (!prompts || prompts.length !== 6) {
                throw new Error('Did not receive exactly 6 prompts.');
            }

            // 2. Setup the UI for the 6 frames
            storyboard.style.display = 'grid';
            prompts.forEach((prompt, index) => {
                const card = createFrameCard(index + 1, prompt);
                storyboard.appendChild(card);
            });

            statusMessage.textContent = 'Generating images...';

            // 3. Generate images concurrently
            const imagePromises = prompts.map((prompt, index) => {
                return generateImage(prompt, index + 1);
            });

            await Promise.allSettled(imagePromises);

            statusMessage.textContent = 'Storyboard generation complete!';
            statusMessage.style.color = 'green';

        } catch (error) {
            console.error('Error:', error);
            statusMessage.textContent = `Error: ${error.message}`;
            statusMessage.style.color = 'red';
        } finally {
            generateBtn.disabled = false;
        }
    });

    function createFrameCard(number, description) {
        const card = document.createElement('div');
        card.className = 'frame-card';
        card.id = `frame-${number}`;

        card.innerHTML = `
            <div class="frame-image-container" id="img-container-${number}">
                <div class="loading-spinner" id="spinner-${number}"></div>
                <img id="img-${number}" alt="Frame ${number}" />
            </div>
            <div class="frame-content">
                <div class="frame-number">Frame ${number}</div>
                <div class="frame-description">${description}</div>
            </div>
        `;
        return card;
    }

    async function generateImage(prompt, number) {
        try {
            const response = await fetch('/api/generate_image', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate image');
            }

            const imgElement = document.getElementById(`img-${number}`);
            const spinnerElement = document.getElementById(`spinner-${number}`);
            
            imgElement.src = data.image;
            imgElement.style.display = 'block';
            spinnerElement.style.display = 'none';

        } catch (error) {
            console.error(`Error generating image for frame ${number}:`, error);
            const container = document.getElementById(`img-container-${number}`);
            container.innerHTML = `<div style="padding: 1rem; color: red; text-align: center; font-size: 0.8rem;">Failed to load image: ${error.message}</div>`;
        }
    }
});
