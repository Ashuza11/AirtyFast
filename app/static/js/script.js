// Load data from localStorage
let buyers = JSON.parse(localStorage.getItem('buyers')) || [];
let recipients = JSON.parse(localStorage.getItem('recipients')) || [];
let sales = JSON.parse(localStorage.getItem('sales')) || [];
let spends = JSON.parse(localStorage.getItem('spends')) || [];
let initialSold = parseFloat(localStorage.getItem('initialSold')) || null;
let cashRestant = parseFloat(localStorage.getItem('cashRestant')) || null;

// Initialize totals
let totalSales = sales.reduce((sum, sale) => sum + sale.amount, 0);
let totalSpending = spends.reduce((sum, spend) => sum + spend.amount, 0);

// Update Buyer List in the dropdown
function updateBuyerList() {
  const buyerList = document.getElementById('buyerList');
  buyerList.innerHTML = buyers.map(buyer => `<option value="${buyer}">`).join('');
}

// Update Buyers List Display
function updateBuyersDisplay() {
  const buyersList = document.getElementById('buyersList');
  const buyerPayments = {};

  // Group payments by buyer
  sales.forEach(sale => {
    if (!buyerPayments[sale.buyerName]) {
      buyerPayments[sale.buyerName] = [];
    }
    buyerPayments[sale.buyerName].push(sale.amount);
  });

  // Display buyers and their individual payments
  buyersList.innerHTML = Object.keys(buyerPayments)
    .map(buyer => `
      <li>${buyer}:
        <ul>
          ${buyerPayments[buyer].map(payment => `<li>${payment.toFixed(2)} CDF</li>`).join('')}
        </ul>
      </li>
    `).join('');
}

// Update Spends List Display
function updateSpendsDisplay() {
  const spendsList = document.getElementById('spendsList');
  spendsList.innerHTML = spends
    .map(spend => `<li>${spend.recipientName}: <span>${spend.amount.toFixed(2)} CDF</span> (${spend.purpose})</li>`)
    .join('');
}

// Function to update the initial sold display
function updateInitialSoldDisplay() {
  document.getElementById('initialSoldDisplay').textContent = (initialSold || 0).toFixed(2);
}

// Function to update the Cash Restant display
function updateCashRestantDisplay() {
  document.getElementById('cashDisplay').textContent = (cashRestant || 0).toFixed(2);
}

// Function to update the balance and totals
function updateBalance() {
  // Calculate total entries (initialSold + totalSales)
  const totalEntries = (initialSold || 0) + totalSales;

  // Calculate total exits (cashRestant + totalSpending)
  const totalExits = (cashRestant || 0) + totalSpending;

  // Calculate the balance
  const balance = totalEntries - totalExits;

  // Update the UI
  document.getElementById('totalEntries').textContent = totalEntries.toFixed(2);
  document.getElementById('totalExits').textContent = totalExits.toFixed(2);
  document.getElementById('balance').textContent = balance.toFixed(2);

  // Change the balance color based on the value
  const balanceElement = document.getElementById('balance');
  if (balance === 0) {
    balanceElement.style.color = 'green'; // Good situation
  } else {
    balanceElement.style.color = 'red'; // Bad situation
  }
}

// Function to update the summary step with all records
function updateSummaryDisplay() {
  const summarySalesList = document.getElementById('summarySalesList');
  const summarySpendsList = document.getElementById('summarySpendsList');

  // Clear existing lists
  summarySalesList.innerHTML = '';
  summarySpendsList.innerHTML = '';

  // Populate sales records in the left column
  sales.forEach(sale => {
    const li = document.createElement('li');
    li.innerHTML = `
      <span>${sale.buyerName}</span>
      <span>${sale.amount.toFixed(2)} CDF</span>
    `;
    summarySalesList.appendChild(li);
  });

  // Populate spending records in the right column
  spends.forEach(spend => {
    const li = document.createElement('li');
    li.innerHTML = `
      <span>${spend.recipientName}</span>
      <span>${spend.amount.toFixed(2)} CDF</span>
      <span>(${spend.purpose})</span>
    `;
    summarySpendsList.appendChild(li);
  });

  // Update Cash Restant display in the summary
  updateCashRestantDisplay();
}

// Function to navigate between steps
function navigateToStep(step) {
  const steps = ['initials', 'entriesExits', 'summary'];
  const timelineSteps = ['step1', 'step2', 'step3'];

  // Hide all steps
  steps.forEach(stepId => {
    document.getElementById(stepId).style.display = 'none';
  });

  // Remove active class from all timeline steps
  timelineSteps.forEach(stepId => {
    document.getElementById(stepId).classList.remove('active');
  });

  // Show the selected step and mark it as active
  document.getElementById(steps[step - 1]).style.display = 'block';
  document.getElementById(timelineSteps[step - 1]).classList.add('active');

  // If navigating to the summary step, update the results and records
  if (step === 3) {
    updateBalance();
    updateInitialSoldDisplay();
    updateCashRestantDisplay();
    updateSummaryDisplay(); // Update the summary records
  }
}

// Add event listeners to timeline steps
document.getElementById('step1').addEventListener('click', () => navigateToStep(1));
document.getElementById('step2').addEventListener('click', () => navigateToStep(2));
document.getElementById('step3').addEventListener('click', () => navigateToStep(3));

// Initial Sold Form Submission
document.getElementById('initialSoldForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const initialSoldInput = parseFloat(document.getElementById('initialSold').value);

  // Save initial sold to localStorage
  initialSold = initialSoldInput;
  localStorage.setItem('initialSold', initialSold);
  alert('Sold initiales enregistrées avec succès!');

  // Update the display
  updateInitialSoldDisplay();

  // Update balance
  updateBalance();

  // Reset form
  e.target.reset();
});

// Cash Restant Form Submission
document.getElementById('cashRestantForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const cashRestantInput = parseFloat(document.getElementById('cashRestant').value);

  // Save Cash Restant to localStorage
  cashRestant = cashRestantInput;
  localStorage.setItem('cashRestant', cashRestant);
  alert('Cash Restant enregistré avec succès!');

  // Update the display
  updateCashRestantDisplay();

  // Update balance
  updateBalance();

  // Reset form
  e.target.reset();
});

// Sales Form Submission
document.getElementById('salesForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const buyerName = document.getElementById('buyerName').value;
  const amountPaid = parseFloat(document.getElementById('amountPaid').value);

  // Validate input
  if (!buyerName || isNaN(amountPaid) || amountPaid <= 0) {
    alert('Please enter valid buyer name and amount.');
    return;
  }

  // Add buyer to the list if it doesn't exist
  if (!buyers.includes(buyerName)) {
    buyers.push(buyerName);
    localStorage.setItem('buyers', JSON.stringify(buyers));
    updateBuyerList();
  }

  // Update total sales
  totalSales += amountPaid;

  // Save sale to localStorage
  sales.push({ buyerName, amount: amountPaid });
  localStorage.setItem('sales', JSON.stringify(sales));

  // Update results
  updateBalance();
  updateBuyersDisplay();

  // Reset form
  e.target.reset();

  // Show success message
  alert('Sale recorded successfully!');
});

// Spending Form Submission
document.getElementById('spendingForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const recipientName = document.getElementById('recipientName').value;
  const amountSpent = parseFloat(document.getElementById('amountSpent').value);
  const purpose = document.getElementById('purpose').value;

  // Validate input
  if (!recipientName || isNaN(amountSpent) || amountSpent <= 0 || !purpose) {
    alert('Please enter valid recipient name, amount, and purpose.');
    return;
  }

  // Add recipient to the list if it doesn't exist
  if (!recipients.includes(recipientName)) {
    recipients.push(recipientName);
    localStorage.setItem('recipients', JSON.stringify(recipients));
  }

  // Update total spending
  totalSpending += amountSpent;

  // Save spend to localStorage
  spends.push({ recipientName, amount: amountSpent, purpose });
  localStorage.setItem('spends', JSON.stringify(spends));

  // Update results
  updateBalance();
  updateSpendsDisplay();

  // Reset form
  e.target.reset();

  // Show success message
  alert('Spending recorded successfully!');
});

// Initialize Display
function initializeDisplay() {
  // Populate the input fields with recorded values if they exist
  if (initialSold) {
    document.getElementById('initialSold').value = initialSold;
  }
  if (cashRestant) {
    document.getElementById('cashRestant').value = cashRestant;
  }

  // Update displays
  updateInitialSoldDisplay();
  updateCashRestantDisplay();
  updateBalance();

  // Hide forms if values are already set
  if (initialSold) {
    document.getElementById('initialSoldForm').style.display = 'none';
  }
  if (cashRestant) {
    document.getElementById('cashRestantForm').style.display = 'none';
  }

  // Automatically navigate to the second step if both forms are filled
  if (initialSold && cashRestant) {
    navigateToStep(2);
  } else {
    navigateToStep(1); // Set the first step as default
  }
}

// Call initializeDisplay to set up the initial state
initializeDisplay();