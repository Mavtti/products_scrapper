from typing import List, NamedTuple
import requests
from collections import namedtuple

Category = namedtuple("Node", ["id", "name", "has_descendants"])

def get_session_token() -> str:
    req = requests.get("https://graphql-gateway.farmdrop.com/graphql", data={})


def get_main_categories() -> List[Category]:
    # TODO
    return


def get_sub(id: str) -> List[Category]:
    data = {
        "operationName": "SubTaxons",
        "variables": "{{\"parentsOnly\": \"true\", \"first\": \"100\", \"id\": \"{0}\"}}".format(id),
        "extensions": "{\"persistedQuery\":{\"version\":1, \"sha256Hash\":\"b3001139e0b710555e42f37c36f0c2cb9064c07bb151e17abbfd1a1aa7411a35\"}}"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Accept": "*/*",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "content-type": "application/json",
        "cache-control": "public",
        "Origin": "https://www.farmdrop.com",
        "Sec-Fetch-Dest": "empty",
        "Connection": "keep-alive",
        "Sec-Fetch-Site": "same-site"
    }
    req = requests.get("https://graphql-gateway.farmdrop.com/graphql", params=data, headers=headers).json()
    sub_categories = req["data"]["tags"]["nodes"][0]["descendants"]["nodes"]
    return [Category(c["id"], c["name"], bool(c["descendants"]["totalCount"])) for c in sub_categories]


def get_final_categories(sub_categories: List[Category]) -> List[Category]:
    res = []
    for subcat in sub_categories:
        if subcat.has_descendants:
            res += get_final_categories(get_sub(subcat.id))
        else:
            res.append(subcat)
    return res


def list_products(category):
    data = {
        "operationName": "GetProducts",
        "variables": '{{"showHidden":false,"defaultOnly":true,"excludeMultibuy":true,"withCompanionTiles":true,"tags":[{{"id":"{0}"}}],"first":25,"after":""}}'.format(category.id),
        "extensions": "{\"persistedQuery\":{\"version\":1, \"sha256Hash\":\"b681acf4eff8b56099d60d6ca7cd314af737ee15ca7dfabf92efaf8faf09db39\"}}"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Accept": "*/*",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "content-type": "application/json",
        "cache-control": "public",
        "Origin": "https://www.farmdrop.com",
        "Sec-Fetch-Dest": "empty",
        "Connection": "keep-alive",
        "Sec-Fetch-Site": "same-site"
    }
    return requests.get("https://graphql-gateway.farmdrop.com/graphql", params=data, headers=headers).json()["data"]["productSearch"]["edges"]
    

init = "c56cdc92-115a-443a-a2d6-8769fb2cbaa4"

if __name__ == "__main__":
    session_token = get_session_token()
    main_categories = get_main_categories()  
    final_categories = get_final_categories(get_sub(init))

    for category in final_categories:
        print(f"Product for {category.name}")
        print([(x["node"]["id"], x["node"]["name"], x["node"]["producer"]["name"]) for x in list_products(category)])
