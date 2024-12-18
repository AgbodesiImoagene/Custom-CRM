async function pushToGong() {
    try {
        const response = await fetch(`${BASE_URL}/gong/full_db_dump`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to push data to Gong');
        }

        const result = await response.json();
        alert(result.message);
    } catch (error) {
        alert(error.message);
    }
}