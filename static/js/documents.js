async function loadDocuments(collectionName) {
    try {
        const response = await fetch(`/api/documents/${collectionName}`);
        if (!response.ok) {
            throw new Error('Failed to fetch documents');
        }
        const data = await response.json();

        // Отримуємо контейнер для документів
        const documentContainer = document.getElementById('document-container');
        documentContainer.innerHTML = ''; // Очищуємо контейнер перед додаванням нових карток

        // Перебір документів і створення карток
        data.documents.forEach(doc => {
            const card = document.createElement('div');
            card.classList.add('document-card'); // Картка документа
            let documentId = null;
            doc.forEach(field => {
                if (field.field_name === "_id")
                    documentId = field.field_value;
            });
            doc.forEach(field => {
                const fieldElement = document.createElement('div');
                fieldElement.classList.add('document-field'); // Поле документа
                // Створюємо HTML-контент для поля
                const fieldValueElement = document.createElement('span');
                fieldValueElement.classList.add('field-value');
                fieldValueElement.innerText = JSON.stringify(field.field_value);

                // Створюємо кнопку редагування
                const editButton = document.createElement('button');
                editButton.classList.add('edit-button');
                editButton.classList.add('operator_access');
                editButton.innerText = 'Редагувати';

                // Обробник кліку на кнопку "Редагувати"
                editButton.addEventListener('click', () => {
                    console.log(field.field_type)
                    // Перевіряємо тип поля і замінюємо його на відповідний інпут
                    let inputElement;
                    switch (field.field_type) {
                        case 'number':
                            inputElement = document.createElement('input');
                            inputElement.type = 'number';
                            inputElement.value = field.field_value;
                            break;
                        case 'boolean':
                            inputElement = document.createElement('input');
                            inputElement.type = 'checkbox';
                            inputElement.checked = field.field_value;
                            break;
                        case 'date':
                            inputElement = document.createElement('input');
                            inputElement.type = 'date';
                            inputElement.value = new Date(field.field_value).toISOString().split('T')[0];
                            break;
                        default: // Стандартний випадок для string
                            inputElement = document.createElement('input');
                            inputElement.type = 'text';
                            inputElement.value = field.field_value;
                    }

                    // Оновлюємо поле на інпут
                    fieldValueElement.replaceWith(inputElement);

                    // Заміна кнопки на "Зберегти"
                    editButton.classList.add ("operator_access");
                    editButton.innerText = 'Зберегти';
                    editButton.addEventListener('click', () => {
                        // Зберігаємо нове значення в залежності від типу
                        if (inputElement.type === 'checkbox') {
                            field.field_value = inputElement.checked;
                        } else {
                            field.field_value = inputElement.value;
                        }
                        updateDocument(collectionName, documentId, field);
                    });
                });

                fieldElement.innerHTML = `<strong>${field.field_name}:</strong> `;
                fieldElement.appendChild(fieldValueElement);
                fieldElement.appendChild(editButton);
                card.appendChild(fieldElement);
            });

            const deleteButton = document.createElement('button');
            deleteButton.classList.add('delete-button');
            deleteButton.classList.add('operator_access');
            deleteButton.innerText = 'Видалити';
            deleteButton.addEventListener('click', async () => {
                deleteDocument(collectionName, documentId)
            });

            card.appendChild(deleteButton); // Додаємо кнопку видалення до картки

            documentContainer.appendChild(card);
        });
    } catch (error) {
        console.log('Помилка при завантаженні документа:', error);
    }
}
async function deleteDocument(collectionName, doc_id) {
    const confirmed = confirm('Ви впевнені, що хочете видалити цей документ?');
    if (confirmed) {
        try {
            const deleteResponse = await fetch(`/api/documents/${collectionName}/${doc_id}`, {
                method: 'DELETE'
            });

            if (deleteResponse.ok) {
                alert('Документ видалено успішно');
               location.reload();
            } else {
                const deleteResult = await deleteResponse.json();
                alert(`Помилка: ${deleteResult.message || 'Не вдалося видалити документ'}`);
            }
        } catch (error) {
            console.error('Помилка при видаленні документа:', error);
            alert('Помилка при видаленні документа');
        }
    }
}
async function updateDocument(collectionName, docId, updatedFields) {
    try {
        const response = await fetch(`/api/documents/${collectionName}/${docId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedFields)
        });

        const data = await response.json();
        if (response.ok) {
            alert('Документ оновлено успішно:', data);
            location.reload();
        } else {
            alert('Помилка при оновленні документа:', response.statusText);
        }
    } catch (error) {
        alert('Помилка при оновленні документа:', error);
    }
}
async function loadFieldsForDocument() {
    const collectionName = document.getElementById('collection-select').value;

    if (!collectionName) return;

    const response = await fetch(`/api/fields/${collectionName}`);
    const data = await response.json();

    const fieldsContainer = document.getElementById('document-fields-container');
    fieldsContainer.innerHTML = '';

    if (data.fields) {
        data.fields.forEach(field => {
            const fieldDiv = document.createElement('div');
            fieldDiv.className = 'field-input';

            const label = document.createElement('label');
            label.textContent = field.field_name;
            fieldDiv.appendChild(label);
            
            fieldDiv.innerHTML += "</br>";
            const input = document.createElement('input');
            input.type = field.field_type; // Default to text input; you can modify this to match the type if needed
            input.id = field.field_name; // Set the ID to the field name
            input.placeholder = `Введіть ${field.field_name}`;
            input.setAttribute("data-type", field.field_type);
            switch (field.field_type) {
                case 'string':
                    input.type = 'text';
                    break;
                case 'number':
                    input.type = 'number';
                    break;
                case 'date':
                    input.type = 'date';
                    break;
                case 'boolean':
                    input.type = 'checkbox'; // Checkbox for boolean
                    break;
                case 'objectId':
                    input.type = 'text'; // Assuming objectId can be entered as a text field
                    break;
                default:
                    input.type = 'text'; // Default to text if type is unknown
                    break;
            }
            fieldDiv.appendChild(input);

            fieldsContainer.appendChild(fieldDiv);
        });
    }
}

async function createDocument(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const collectionName = document.getElementById('collection-select').value;
    const documentData = {};

    // Gather all input data
    const fields = document.querySelectorAll('#document-fields-container input, #document-fields-container select');
    fields.forEach(field => {
        if (field.type === 'checkbox') {
            documentData[field.id] = {
                value: field.checked,
                type: field.getAttribute("data-type")
            }; // Use field id as key and checked state as value
        } // Use field id as key and checked state as value
        else {
            documentData[field.id] = {
                value: field.value,
                type: field.getAttribute("data-type")
            }; // Use field id as key and field value as value
        }
    });

    try {
        const response = await fetch(`/api/documents/${collectionName}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(documentData),
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            document.getElementById('document-form').reset(); // Reset the form
            location.reload();
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Виникла помилка при додаванні документа');
    }
}