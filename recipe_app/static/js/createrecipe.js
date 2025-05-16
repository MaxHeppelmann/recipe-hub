// Function to create a new direction input field
function createNewDirectionInput(container) {
    const inputItem = document.createElement('div');
    inputItem.className = 'input-item';
    
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'direction-input';
    input.placeholder = 'Add a direction';
    input.required = true;
    
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'remove-btn squircle';
    removeBtn.textContent = '✕';
    removeBtn.addEventListener('click', function() {
        container.removeChild(inputItem);
    });
    
    inputItem.appendChild(input);
    inputItem.appendChild(removeBtn);
    container.appendChild(inputItem);
    
    return input;
}

// Function to create a new ingredient input with name and amount fields
function createNewIngredientInput(container) {
    const ingredientItem = document.createElement('div');
    ingredientItem.className = 'ingredient-item';
    
    const nameInput = document.createElement('input');
    nameInput.type = 'text';
    nameInput.className = 'ingredient-name';
    nameInput.placeholder = 'Ingredient name';
    nameInput.required = true;
    
    const amountInput = document.createElement('input');
    amountInput.type = 'text';
    amountInput.className = 'ingredient-amount';
    amountInput.placeholder = 'Amount (e.g. 2 cups)';
    amountInput.required = true;
    
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'remove-btn squircle';
    removeBtn.textContent = '✕';
    removeBtn.style.display = 'none';
    removeBtn.addEventListener('click', function() {
        container.removeChild(ingredientItem);
    });
    
    ingredientItem.appendChild(nameInput);
    ingredientItem.appendChild(amountInput);
    ingredientItem.appendChild(removeBtn);
    container.appendChild(ingredientItem);
    
    return { nameInput, amountInput };
}

// Setup the ingredients input functionality
function setupIngredientsInput() {
    const container = document.getElementById('ingredients-container');
    const addBtn = document.getElementById('add-ingredient');
    
    // Add new fields when the add button is clicked
    addBtn.addEventListener('click', function() {
        const { nameInput } = createNewIngredientInput(container);
        nameInput.focus();
    });
    
    // Watch for inputs and show remove buttons when needed
    container.addEventListener('input', function(event) {
        if (event.target.classList.contains('ingredient-name') || event.target.classList.contains('ingredient-amount')) {
            const parent = event.target.parentElement;
            const removeBtn = parent.querySelector('.remove-btn');
            
            // Show remove button if either field has text
            const nameInput = parent.querySelector('.ingredient-name');
            const amountInput = parent.querySelector('.ingredient-amount');
            
            if (nameInput.value.trim() !== '' || amountInput.value.trim() !== '') {
                removeBtn.style.display = 'block';
            } else {
                removeBtn.style.display = 'none';
            }
            
            // Check if this is the last item and both fields have text
            const items = container.querySelectorAll('.ingredient-item');
            const lastItem = items[items.length - 1];
            
            if (parent === lastItem && 
                nameInput.value.trim() !== '' && 
                amountInput.value.trim() !== '') {
                // Create a new empty input field pair
                createNewIngredientInput(container);
            }
        }
    });
}

// Setup the directions input functionality
function setupDirectionsInput() {
    const container = document.getElementById('directions-container');
    const addBtn = document.getElementById('add-direction');
    
    // Add new field when the add button is clicked
    addBtn.addEventListener('click', function() {
        const newInput = createNewDirectionInput(container);
        newInput.focus();
    });
    
    // Watch for inputs and show remove buttons when needed
    container.addEventListener('input', function(event) {
        if (event.target.classList.contains('direction-input')) {
            // Show the remove button for filled inputs
            const parent = event.target.parentElement;
            const removeBtn = parent.querySelector('.remove-btn');
            if (event.target.value.trim() !== '') {
                removeBtn.style.display = 'block';
            } else {
                removeBtn.style.display = 'none';
            }
            
            // Check if this is the last input and it has text
            const inputs = container.querySelectorAll('.direction-input');
            const lastInput = inputs[inputs.length - 1];
            
            if (event.target === lastInput && event.target.value.trim() !== '') {
                // Create a new empty input field
                createNewDirectionInput(container);
            }
        }
    });
}

// Function to collect form data and submit as JSON
async function setupFormSubmission() {
    const form = document.getElementById('recipeForm');
    const submitButton = document.getElementById('submit-recipe');
    
    submitButton.addEventListener('click', async function (event) {
        event.preventDefault();

        // Validate the form
        const name = document.getElementById('name').value.trim();
        const description = document.getElementById('description').value.trim();

        if (!name || !description) {
            alert('Please fill in all required fields');
            return;
        }

        // Collect ingredients (name-amount pairs)
        const ingredients = {};
        const ingredientItems = document.querySelectorAll('.ingredient-item');
        let validIngredients = true;

        ingredientItems.forEach(item => {
            const nameInput = item.querySelector('.ingredient-name');
            const amountInput = item.querySelector('.ingredient-amount');

            const ingredientName = nameInput.value.trim();
            const ingredientAmount = amountInput.value.trim();

            // Skip empty fields (like the last placeholder row)
            if (ingredientName && ingredientAmount) {
                ingredients[ingredientName] = ingredientAmount;
            } else if ((ingredientName && !ingredientAmount) || (!ingredientName && ingredientAmount)) {
                // If one field is filled but not the other
                validIngredients = false;
            }
        });

        if (!validIngredients || Object.keys(ingredients).length === 0) {
            alert('Please fill in all ingredient fields (both name and amount)');
            return;
        }

        // Collect steps (directions)
        const steps = [];
        const directionInputs = document.querySelectorAll('.direction-input');
        let validSteps = true;

        directionInputs.forEach(input => {
            const step = input.value.trim();
            if (step) {
                steps.push(step);
            }
        });

        if (steps.length === 0) {
            alert('Please add at least one direction');
            return;
        }

        // Create the recipe data object
        const recipeData = {
            name: name,
            description: description,
            ingredients: ingredients,
            steps: steps
        };
        // Send data to the server
        let response = await fetch('/createrecipe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(recipeData)
        })
        let responseData = await response.json();
        if (response.status === 200) {
            window.location.href = '/recipes/'+responseData['recipe_id'];
        } else {
            document.getElementById('Error-Box').innerHTML = 'Error: ' + responseData['error'] + '<br>Please try again';
        }

    });
}

// Setup all the dynamic inputs when the document is loaded
document.addEventListener('DOMContentLoaded', function() {
    setupIngredientsInput();
    setupDirectionsInput();
    setupFormSubmission();
});