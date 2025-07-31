# Django Product Analytics API

This is a Django REST Framework project to manage and analyze products by category, price, and stock. It includes:

- Models for Category and Product
- Management command to import data from Excel
- API to fetch aggregated analytics
- Query parameter filtering
- Caching for performance

## Features

- 📦 Product & Category management
- 📊 `/api/products/analytics/` for total products, average price, and stock value
- 🔍 Filter by category (case-insensitive), `min_price`, `max_price`
- ⚡ Fast using bulk insert & 5-minute cache
- ✅ Data validation: ensures price and stock are non-negative
- 🧾 Import support via `large_dataset.xlsx`

---

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/pc-crazy/django-product-analytics-api.git
cd django-product-analytics-api
```

2. **Create a virtual environment and activate it**:
```bash
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Apply migrations**:
```bash
python manage.py migrate
```

---

## Usage

### Import Products

To import data from an Excel file:

```bash
python manage.py import_products path/to/large_dataset.xlsx
```

Handles:
- Non-negative price and stock
- Skips invalid rows with log output
- Uses bulk insert for performance

---

### API Endpoint

**URL:** `/api/products/analytics/`  
**Method:** `GET`  
**Parameters (optional):**
- `category`: filter by category name (case-insensitive)
- `min_price`: filter products with price ≥ `min_price`
- `max_price`: filter products with price ≤ `max_price`

**Sample Request:**
```http
GET /api/products/analytics/?category=Electronics&min_price=10&max_price=1000
```

**Sample Response:**
```json
{
  "total_products": 25,
  "average_price": 45.67,
  "total_stock_value": 5800.00
}
```

---

## Admin Access

Create a superuser to manage data via Django Admin:

```bash
python manage.py createsuperuser
```

Access at: `http://localhost:8000/admin/`

---

## Performance Optimizations

- ✅ **Caching**: Analytics responses are cached per filter for 5 minutes.
- ✅ **Database Indexing**: `price` and `category` fields are indexed to speed up queries.

---

## License

This project is open-source under the MIT License.