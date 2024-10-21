async function loadFieldsForRename() {
    const collectionName = document.getElementById('collection-select').value;
    const response = await fetch(`/api/fields/${collectionName}`);
    const data = await response.json();
    console.log(data)
    const fieldSelect = document.getElementById('field-select');
    fieldSelect.innerHTML = '';

    if (data.fields) {
        data.fields.forEach(field => {
            if (field.field_name !== "_id") {
                const option = document.createElement('option');
                option.value = field.field_name;
                option.textContent = field.field_name;
                fieldSelect.appendChild(option);
            }
        });
    }
}

async function renameField() {
    const collectionName = document.getElementById('collection-select').value;
    const oldFieldName = document.getElementById('field-select').value;
    const newFieldName = document.getElementById('new-field-name').value;

    try {
        const response = await fetch(`/api/fields/${collectionName}/${oldFieldName}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                newFieldName: newFieldName,
            }),
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            location.reload();
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Виникла помилка при перейменуванні поля');
    }
}

async function deleteField() {
    const collectionName = document.getElementById('collection-select').value;
    const fieldName = document.getElementById('field-select').value;
    if (confirm("Ви дійсно хочете видалити колекцію?")) {
        try {


            const response = await fetch(`/api/fields/${collectionName}/${fieldName}`, {
                method: 'DELETE'
            });

            const result = await response.json();
            if (response.ok) {
                alert(result.message);
                location.reload();
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Виникла помилка при видаленнi поля');
        }
    }
}
async function addNewField() {
    const collectionName = document.getElementById('collection-select').value;
    let field = document.getElementById("field-name").value;
    let type = document.getElementById("field-type").value;
    console.log(collectionName)
    console.log(field)
    console.log(type)
    try {
        const response = await fetch(`/api/fields/${collectionName}/${field}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: type,
            }),
        });
        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            location.reload();
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Виникла помилка при додаванні поля');
    }
}