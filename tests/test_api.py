from decimal import Decimal


def make_product(client, **overrides):
    payload = {"name": "Chicken breast", "default_unit": "g"}
    payload.update(overrides)
    return client.post("/products", json=payload)


# --- health -----------------------------------------------------------------

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


# --- products ---------------------------------------------------------------

def test_list_products_empty(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


def test_create_product(client):
    response = make_product(client, brand="Bachoco", barcode="750100", notes="fresh")
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "Chicken breast"
    assert body["brand"] == "Bachoco"
    assert body["barcode"] == "750100"
    assert body["default_unit"] == "g"


def test_create_product_defaults_and_trims(client):
    response = client.post("/products", json={"name": "  Rice  "})
    assert response.status_code == 201
    assert response.json()["name"] == "Rice"
    assert response.json()["default_unit"] == "piece"


def test_list_products_ordered_by_name(client):
    make_product(client, name="Zucchini")
    make_product(client, name="Apple")
    names = [p["name"] for p in client.get("/products").json()]
    assert names == ["Apple", "Zucchini"]


def test_create_product_rejects_empty_name(client):
    assert make_product(client, name="").status_code == 422
    assert make_product(client, name="   ").status_code == 422


def test_create_product_rejects_missing_name(client):
    assert client.post("/products", json={}).status_code == 422


def test_create_product_rejects_unknown_unit(client):
    assert make_product(client, default_unit="bananas").status_code == 422


def test_duplicate_barcode_returns_409(client):
    assert make_product(client, barcode="123").status_code == 201
    response = make_product(client, name="Other", barcode="123")
    assert response.status_code == 409
    assert "123" in response.json()["detail"]
    assert len(client.get("/products").json()) == 1


def test_blank_barcodes_do_not_conflict(client):
    assert make_product(client, name="A", barcode="").status_code == 201
    assert make_product(client, name="B", barcode="  ").status_code == 201
    assert make_product(client, name="C").status_code == 201


# --- inventory --------------------------------------------------------------

def test_list_inventory_empty(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.json() == []


def test_create_inventory_item(client):
    product_id = make_product(client).json()["id"]
    response = client.post(
        "/inventory",
        json={
            "product_id": product_id,
            "quantity": "500.5",
            "unit": "g",
            "expiration_date": "2026-11-01",
            "notes": "freezer",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["product_id"] == product_id
    assert body["product"]["name"] == "Chicken breast"
    assert Decimal(body["quantity"]) == Decimal("500.5")
    assert body["unit"] == "g"
    assert body["expiration_date"] == "2026-11-01"
    assert body["purchased_at"]  # defaulted by the server
    assert body["opened_at"] is None
    assert body["notes"] == "freezer"


def test_decimal_precision_survives_round_trip(client):
    product_id = make_product(client).json()["id"]
    client.post(
        "/inventory",
        json={"product_id": product_id, "quantity": "0.125", "unit": "kg"},
    )
    listed = client.get("/inventory").json()
    assert Decimal(listed[0]["quantity"]) == Decimal("0.125")


def test_inventory_unknown_product_returns_404(client):
    response = client.post(
        "/inventory", json={"product_id": 999, "quantity": "1", "unit": "g"}
    )
    assert response.status_code == 404


def test_inventory_rejects_invalid_quantities(client):
    product_id = make_product(client).json()["id"]
    for bad in ["0", "-5", "abc", None, "1.2345", "1" + "0" * 12]:
        response = client.post(
            "/inventory",
            json={"product_id": product_id, "quantity": bad, "unit": "g"},
        )
        assert response.status_code == 422, bad
    assert client.get("/inventory").json() == []


def test_inventory_rejects_unknown_unit(client):
    product_id = make_product(client).json()["id"]
    response = client.post(
        "/inventory",
        json={"product_id": product_id, "quantity": "1", "unit": "bananas"},
    )
    assert response.status_code == 422


def test_inventory_rejects_bad_date(client):
    product_id = make_product(client).json()["id"]
    response = client.post(
        "/inventory",
        json={
            "product_id": product_id,
            "quantity": "1",
            "unit": "g",
            "expiration_date": "not-a-date",
        },
    )
    assert response.status_code == 422


def test_inventory_ordering_soonest_expiry_first_nulls_last(client):
    product_id = make_product(client).json()["id"]

    def add(expiration):
        body = {"product_id": product_id, "quantity": "1", "unit": "piece"}
        if expiration:
            body["expiration_date"] = expiration
        return client.post("/inventory", json=body).json()["id"]

    no_date = add(None)
    later = add("2026-12-01")
    sooner = add("2026-11-01")

    ids = [i["id"] for i in client.get("/inventory").json()]
    assert ids == [sooner, later, no_date]
