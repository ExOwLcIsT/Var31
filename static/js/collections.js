async function loadCollections() {
    try {
        const response = await fetch('/api/collections');
        if (!response.ok) {
            throw new Error('Failed to fetch collections');
        }
        const collections = await response.json();

        const collectionSelect = document.getElementById('collection-select');

        collectionSelect.innerHTML = '';

        collections.forEach(collection => {
            const option = document.createElement('option');
            option.value = collection;
            option.textContent = collection;
            collectionSelect.appendChild(option);
        });
        collectionSelect.selectedIndex = 0
    } catch (error) {
        console.error('Error loading collections:', error);
    }
}
async function addNewCollection() {
    const collectionName = document.getElementById('new-collection-name').value.trim();

    if (!collectionName) {
        alert('Будь ласка, введіть назву колекції');
        return;
    }

    try {
        const response = await fetch(`/api/collections/${collectionName}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        if (response.ok) {
            alert(`Колекцію "${collectionName}" створено успішно!`);
            location.reload();
        } else {
            alert(`Помилка: ${result.error || 'Щось пішло не так'}`);
        }
    } catch (error) {
        console.error('Error:', error.message);
        alert('Помилка під час створення колекції');
    }
}
async function deleteCollection() {
    try {
        const collectionName = document.getElementById('collection-select').value;

        if (!collectionName) {
            alert('Потрібно обрати колекцію для видалення');
            return;
        }
        if (confirm("Ви дійсно хочете видалити колекцію?")) {
            const response = await fetch(`/api/collections/${collectionName}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        

        if (!response.ok) {
            throw new Error('Не вдалося видалити колекцію');
        }

        const result = await response.json();

        if (result.message) {
            alert(result.message);
            location.reload();
        } else if (result.error) {
            console.error(result.error);
            alert('Помилка: ' + result.error);
        }
    }
    } catch (error) {
        console.error('Помилка при видаленні колекції:', error);
        alert('Помилка при видаленні колекції: ' + error.message);
    }
}