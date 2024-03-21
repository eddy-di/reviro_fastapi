from app.routers.product import (
    create_product,
    delete_product,
    get_product,
    get_products,
    patch_product,
    put_product,
)
from app.utils.pathfinder import reverse


def test_get_product_list_with_empty_products(
    api_client,
    create_company
):
    # given
    client = api_client
    company = create_company
    # when
    url = reverse(get_products, company_id=company.id)
    response = client.get(url)
    # then
    assert response.status_code == 200
    assert response.json() == []


def test_get_product_list_with_one_product(
    api_client,
    create_product,
    create_company
):
    # given
    client = api_client
    company = create_company
    product = create_product(company.id)
    # when
    url = reverse(get_products, company_id=product.company_id)
    response = client.get(url)
    # then
    assert response.status_code == 200
    assert response.json()[0]['name'] == product.name
    assert response.json()[0]['description'] == product.description
    assert response.json()[0]['price'] == str(product.price)
    assert response.json()[0]['discount'] == product.discount
    assert response.json()[0]['quantity'] == product.quantity
    assert response.json()[0]['company_id'] == product.company_id


def test_get_products_list_with_one_company_and_many_products(
    api_client,
    create_num_of_products_for_one_company
):
    # given
    client = api_client
    products = create_num_of_products_for_one_company(15)
    first_product = products[0]
    # when
    url = reverse(get_products, company_id=first_product.company_id)
    response = client.get(url)
    # then
    assert response.status_code == 200
    assert len(response.json()) == 10
    assert response.json()[0]['name'] == first_product.name
    assert response.json()[0]['description'] == first_product.description
    assert response.json()[0]['price'] == str(first_product.price)
    assert response.json()[0]['discount'] == first_product.discount
    assert response.json()[0]['quantity'] == first_product.quantity
    assert response.json()[0]['company_id'] == first_product.company_id


def test_post_product_list_api(
    api_client,
    create_company,
    product_create_data_dict
):
    # given
    client = api_client
    company = create_company
    post_data = product_create_data_dict(company.id)
    # when
    url = reverse(create_product, company_id=company.id)
    response = client.post(url, json=post_data)
    # then
    assert response.status_code == 200
    assert response.json()['name'] == post_data['name']
    assert response.json()['description'] == post_data['description']
    assert response.json()['price'] == post_data['price']
    assert response.json()['discount'] == post_data['discount']
    assert response.json()['quantity'] == post_data['quantity']
    assert response.json()['company_id'] == post_data['company_id']


def test_get_specific_product(
    api_client,
    create_product,
    create_company
):
    # given
    client = api_client
    company = create_company
    product = create_product(company.id)
    # when
    url = reverse(get_product, company_id=product.company_id, product_id=product.id)
    response = client.get(url)
    # then
    assert response.status_code == 200
    assert response.json()['name'] == product.name
    assert response.json()['description'] == product.description
    assert response.json()['price'] == str(product.price)
    assert response.json()['discount'] == product.discount
    assert response.json()['quantity'] == product.quantity
    assert response.json()['company_id'] == product.company_id


def test_patch_specific_product(
    api_client,
    create_product,
    create_company
):
    # given
    client = api_client
    company = create_company
    product = create_product(company.id)
    patch_data = {
        'name': 'patchedName',
        'description': 'patchedDescription'
    }
    # when
    url = reverse(patch_product, company_id=product.company_id, product_id=product.id)
    response = client.patch(url, json=patch_data)
    # then
    assert response.status_code == 200
    assert response.json()['name'] == patch_data['name']
    assert response.json()['description'] == patch_data['description']
    assert response.json()['price'] == str(product.price)
    assert response.json()['discount'] == product.discount
    assert response.json()['quantity'] == product.quantity


def test_put_specific_product(
    api_client,
    create_product,
    create_company
):
    # given
    client = api_client
    company = create_company
    product = create_product(company.id)
    put_data = {
        'name': 'updatePutName',
        'description': 'updatePutDescription',
        'price': '999.99'
    }
    # when
    url = reverse(put_product, company_id=company.id, product_id=product.id)
    response = client.put(url, json=put_data)
    # then
    assert response.status_code == 200


def test_delete_specific_product(
    api_client,
    create_product,
    create_company
):
    # given
    client = api_client
    company = create_company
    product = create_product(company.id)
    # when
    url = reverse(delete_product, company_id=company.id, product_id=product.id)
    response = client.delete(url)
    # then
    assert response.status_code == 204
    assert response.json() == 'Product deleted.'
