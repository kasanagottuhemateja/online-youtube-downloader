document.getElementById('downloadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = document.getElementById('url').value;
    const format = document.getElementById('format').value;
    const quality = document.getElementById('quality').value;
    const status = document.getElementById('status');

    status.textContent = 'Processing...';
    const formData = new FormData();
    formData.append('url', url);
    formData.append('format', format);
    formData.append('quality', quality);

    try {
        const response = await fetch('/download', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error);
        }

        const blob = await response.blob();
        const filename = response.headers.get('Content-Disposition')?.split('filename=')[1] || 'download';
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = filename.replace(/"/g, '');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        status.textContent = 'Download complete!';
    } catch (error) {
        status.textContent = `Error: ${error.message}`;
    }
});

document.getElementById('format').addEventListener('change', (e) => {
    const qualitySelect = document.getElementById('quality');
    qualitySelect.style.display = e.target.value === 'video' ? 'inline' : 'none';
});