const categoryForm = document.getElementById('categoryForm');
const categoryTableBody = document.querySelector('#categoryTable tbody');

async function loadCategories() {
  const res = await fetch('/api/categories');
  const categories = await res.json();
  categoryTableBody.innerHTML = '';

  categories.forEach(c => {
    const row = document.createElement('tr');
    row.innerHTML = `<td>${c.category_id}</td><td>${c.name}</td>`;
    categoryTableBody.appendChild(row);
  });
}

categoryForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('categoryName').value;

  await fetch('/api/categories', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  });

  categoryForm.reset();
  loadCategories();
});

const supplierForm = document.getElementById('supplierForm');
const supplierTableBody = document.querySelector('#supplierTable tbody');

async function loadSuppliers() {
  const res = await fetch('/api/suppliers');
  const suppliers = await res.json();
  supplierTableBody.innerHTML = '';

  suppliers.forEach(s => {
    const row = document.createElement('tr');
    row.innerHTML = `<td>${s.supplier_id}</td><td>${s.name}</td><td>${s.contact || ''}</td>`;
    supplierTableBody.appendChild(row);
  });
}

supplierForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('supplierName').value;
  const contact = document.getElementById('supplierContact').value;

  await fetch('/api/suppliers', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, contact })
  });

  supplierForm.reset();
  loadSuppliers();
});

const form = document.getElementById('productForm');
const tableBody = document.querySelector('#productTable tbody');
let editingProductId = null;

async function loadProducts() {
  const res = await fetch('/api/products');
  const products = await res.json();
  tableBody.innerHTML = '';

  products.forEach(p => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${p.product_id}</td>
      <td>${p.name}</td>
      <td>${p.sku}</td>
      <td>${p.price}</td>
      <td>${p.quantity}</td>
      <td>${p.category_name || '-'}</td>
      <td>
        <button class="edit-btn" onclick="editProduct(${p.product_id})">Edit</button>
        <button class="delete-btn" onclick="deleteProduct(${p.product_id})">Delete</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
}

async function editProduct(id) {
  const res = await fetch(`/api/products/${id}`);
  const product = await res.json();

  document.getElementById('name').value = product.name;
  document.getElementById('sku').value = product.sku;
  document.getElementById('price').value = product.price;
  document.getElementById('quantity').value = product.quantity;
  document.getElementById('category_id').value = product.category_id || '';
  document.getElementById('description').value = product.detail ? product.detail.description : '';
  document.getElementById('warranty_months').value = product.detail ? product.detail.warranty_months : 0;

  const supplierIds = product.suppliers.map(s => s.supplier_id).join(',');
  document.getElementById('supplier_ids').value = supplierIds;

  editingProductId = id;
  document.querySelector('#productForm button[type="submit"]').textContent = 'Update Product';
}

async function deleteProduct(id) {
  if (!confirm('Delete this product?')) return;
  await fetch(`/api/products/${id}`, { method: 'DELETE' });
  loadProducts();
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const supplierInput = document.getElementById('supplier_ids').value;
  const supplierIds = supplierInput
    ? supplierInput.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id))
    : [];

  const body = {
    name: document.getElementById('name').value,
    sku: document.getElementById('sku').value,
    price: parseFloat(document.getElementById('price').value),
    quantity: parseInt(document.getElementById('quantity').value),
    category_id: document.getElementById('category_id').value || null,
    description: document.getElementById('description').value,
    warranty_months: parseInt(document.getElementById('warranty_months').value) || 0,
    supplier_ids: supplierIds
  };

  if (editingProductId) {
    await fetch(`/api/products/${editingProductId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    editingProductId = null;
    document.querySelector('#productForm button[type="submit"]').textContent = 'Add Product';
  } else {
    await fetch('/api/products', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
  }

  form.reset();
  loadProducts();
});

loadCategories();
loadSuppliers();
loadProducts();