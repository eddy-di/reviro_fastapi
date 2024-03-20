from app.routers.company import (
    create_company,
    delete_company,
    get_companies,
    get_company,
    patch_company,
    put_company,
)
from app.utils.pathfinder import reverse


def test_get_company_list_api_with_empty_companies(
    api_client
):
    # given
    client = api_client
    # when
    url = reverse(get_companies)
    response = client.get(url)
    # then
    assert response.status_code == 200
    assert response.json() == []


def test_get_company_list_api_with_companies(
    api_client,
    create_num_of_companies
):
    # given
    client = api_client
    create_num_of_companies(20)
    # when
    url = reverse(get_companies)
    response = client.get(url)
    # then
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_post_company_create_api(
    api_client,
    company_create_data_dict
):
    # given
    client = api_client
    post_data = company_create_data_dict
    # when
    url = reverse(create_company)
    response = client.post(url, json=post_data)
    # then
    assert response.status_code == 201
    assert response.json()['name'] == post_data['name']
    assert response.json()['description'] == post_data['description']
    assert response.json()['schedule_start'] == post_data['schedule_start']
    assert response.json()['schedule_end'] == post_data['schedule_end']
    assert response.json()['phone_number'] == post_data['phone_number']
    assert response.json()['email'] == post_data['email']
    assert response.json()['map_link'] == post_data['map_link']
    assert response.json()['social_media1'] == post_data['social_media1']
    assert response.json()['social_media2'] == post_data['social_media2']


def test_get_company_specific_api_for_non_existent_company(
    api_client
):
    # given
    client = api_client
    # when
    url = reverse(get_company, company_id=100)
    response = client.get(url)
    # then
    assert response.status_code == 404
    assert response.json()['detail'] == 'Company not found.'


def test_get_company_specific_api_for_existent_company(
    api_client,
    create_company
):
    # given
    client = api_client
    company = create_company
    # when
    url = reverse(get_company, company_id=company.id)
    response = client.get(url)
    # then
    assert response.status_code == 200
    assert response.json()['name'] == company.name
    assert response.json()['description'] == company.description
    assert response.json()['schedule_start'] == company.schedule_start.strftime('%H:%M:%S')
    assert response.json()['schedule_end'] == company.schedule_end.strftime('%H:%M:%S')
    assert response.json()['phone_number'] == company.phone_number
    assert response.json()['email'] == company.email
    assert response.json()['map_link'] == company.map_link
    assert response.json()['social_media1'] == company.social_media1
    assert response.json()['social_media2'] == company.social_media2
    assert response.json()['social_media3'] == company.social_media3


def test_put_company_specific_api(
    api_client,
    create_company
):
    # given
    client = api_client
    company = create_company
    # when
    put_data = {
        'name': 'patchedCompanyName',
        'description': 'patchedCompanyDescription',
        'schedule_start': '09:00:00',
        'schedule_end': '00:00:00',
        'phone_number': '+996123456789',
        'email': 'put.example@mail.com',
        'map_link': 'https://2gis.kg',
        'social_media1': 'https://www.instagram.com/',
        'social_media2': 'https://www.tiktok.com/en/',
        'social_media3': 'https://www.facebook.com/'
    }
    url = reverse(put_company, company_id=company.id)
    response = client.put(url, json=put_data)
    # then
    assert response.status_code == 200
    assert response.json()['name'] == put_data['name']
    assert response.json()['description'] == put_data['description']
    assert response.json()['schedule_start'] == put_data['schedule_start']
    assert response.json()['schedule_end'] == put_data['schedule_end']
    assert response.json()['phone_number'] == put_data['phone_number']
    assert response.json()['email'] == put_data['email']
    assert response.json()['map_link'] == put_data['map_link']
    assert response.json()['social_media1'] == put_data['social_media1']
    assert response.json()['social_media2'] == put_data['social_media2']
    assert response.json()['social_media3'] == put_data['social_media3']


def test_patch_company_specific_api(
    api_client,
    create_company
):
    # given
    client = api_client
    company = create_company
    patch_data = {
        'name': 'patchedCompanyName',
        'description': 'patchedCompanyDescription'
    }
    # when
    url = reverse(patch_company, company_id=company.id)
    response = client.patch(url, json=patch_data)
    # then
    assert response.status_code == 200
    assert response.json()['name'] == patch_data['name']
    assert response.json()['description'] == patch_data['description']


def test_delete_company_specific_api(
    api_client,
    create_company
):
    # given
    client = api_client
    company = create_company
    # when
    url = reverse(delete_company, company_id=company.id)
    response = client.delete(url)
    # then
    assert response.status_code == 204
    assert response.json() == 'Company deleted.'
