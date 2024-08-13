import requests
from selene import browser, have


def test_spending_title_exists():
    browser.open('http://frontend.niffler.dc')
    browser.element('a[href*=redirect]').click()
    browser.element('input[name=username]').set_value("stas")
    browser.element('input[name=password]').set_value("12345")
    browser.element('button[type=submit]').click()
    browser.element('.main-content').should(have.text('History of spendings'))


def test_spending_should_be_deleted_after_table_action():
    url = 'http://gateway.niffler.dc:8090/api/spends/add'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJraWQiOiJi...',
        'Content-Type': 'application/json',
        'Origin': 'http://frontend.niffler.dc',
    }
    data = {
        "amount": "108.51",
        "description": "QA.GURU Python Advanced 1",
        "category": "school",
        "spendDate": "2024-08-08T18:39:27.955Z",
        "currency": "RUB"
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    print(response.json())

    browser.open('http://frontend.niffler.dc')
    browser.element('a[href*=redirect]').click()
    browser.element('input[name=username]').set_value("stas")
    browser.element('input[name=password]').set_value("12345")
    browser.element('button[type=submit]').click()

    browser.element('.spendings-table tbody').should(have.text("QA.GURU Python Advanced 1"))
    browser.element('.spendings-table tbody input[type=checkbox]').click()
    browser.element('.spendings__bulk-actions button').click()

    browser.all(".spendings-table tbody tr").should(have.size(0))
    browser.element('.spendings__content').should(have.text("No spendings provided yet!"))

