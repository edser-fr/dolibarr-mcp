# Dolibarr MCP Server

## Repository layout

| Path | Purpose |
| --- | --- |

```bash
python -m dolibarr_mcp.cli test --url https://your-dolibarr.example.com/api/index.php --api-key YOUR_KEY
```

## Available tools

- **System** – `test_connection`, `get_status`
- **Users** – `get_users`, `get_user_by_id`, `create_user`, `update_user`, `delete_user`
- **Customers / Third parties** – `get_customers`, `get_customer_by_id`, `create_customer`, `update_customer`, `delete_customer`
- **Products** – `get_products`, `get_product_by_id`, `create_product`, `update_product`, `delete_product`
- **Invoices** – `get_invoices`, `get_invoice_by_id`, `create_invoice`, `update_invoice`, `delete_invoice`
- **Orders** – `get_orders`, `get_order_by_id`, `create_order`, `update_order`, `delete_order`
- **Contacts** – `get_contacts`, `get_contact_by_id`, `create_contact`, `update_contact`, `delete_contact`
- **Raw API access** – `dolibarr_raw_api`


## License

This project is released under the [MIT License](LICENSE).
