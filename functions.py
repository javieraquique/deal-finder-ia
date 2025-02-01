def fetch_steam_data(
    game_title,
    currency,
    platform,
    platform_dict_steam,
    currency_dict_steam,
    re,
    BeautifulSoup,
    pd,
):
    """
    Fetches data from the Steam store page and returns it as a pandas DataFrame.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML of the Steam store page.
    titles (list): A list to store the titles of the games.
    prices (list): A list to store the prices of the games.
    links (list): A list to store the links to the games.
    uninitialized (list): A list of indices for uninitialized images.

    Returns:
    pd.DataFrame: A DataFrame containing the fetched data with columns 'title', 'price', 'link', 'image', and 'vendor'.
                  If no data is fetched, an empty DataFrame is returned.
    """
    # Transforming platform and currency to steam format
    cleared_platform = platform_dict_steam[platform]
    cleared_currency = currency_dict_steam[currency]
    steam_url = f"https://store.steampowered.com/search/?&term={game_title}&os={cleared_platform}&cc={cleared_currency}"
    # Getting steam's page
    steam_object = re.get(steam_url)
    if steam_object.status_code == 200:
        # Parsing the page
        soup = BeautifulSoup(steam_object.content, "html.parser")
        # Get the titles list
        titles = []
        for x in soup.find_all("span", class_="title"):
            titles.append(x.text)
        # Search for the 'Uninitialized' title and remove it
        uninitialized = []
        for i in range(0, len(titles) - 1):
            if titles[i] == "Uninitialized":
                uninitialized.append(i)
                del titles[i]
        # Get the prices list
        prices = []
        for x in soup.find_all('div', class_='col search_price_discount_combined responsive_secondrow'):
            try:
                prices.append(str(x).split('discount_final_price">')[1].split("</div>")[0].replace('$', '').replace('€', ''))
            except:
                prices.append('')        # Get the links list
        links = []
        for x in soup.find_all("a", class_="search_result_row ds_collapse_flag"):
            links.append(x.get("href"))
        for link in links:
            if links.index(link) in uninitialized:
                links.remove(link)
        # Get images
        images = []
        for x in soup.find_all("div", class_="col search_capsule"):
            images.append(str(x).split('src="')[1].split('"')[0])
        for image in images:
            if images.index(image) in uninitialized:
                images.remove(image)
        data = {"title": titles, "price": prices, "link": links, "image": images}
        df_steam = pd.DataFrame(data)
        df_steam["vendor"] = "Steam"
        return df_steam
    else:
        # Create an empty DataFrame
        empty_df = pd.DataFrame()

        # Return the empty DataFrame
        return empty_df


def fetch_gog_data(
    game_title, currency, platform, platform_dict_gog, re, pd, country_dict_gog
):
    """
    Fetches data from the GOG store page and returns it as a pandas DataFrame.

    Parameters:
    products (list): A list of dictionaries containing product information from the GOG store.

    Returns:
    pd.DataFrame: A DataFrame containing the fetched data with columns 'title', 'price', 'link', 'image', and 'vendor'.
                  If no data is fetched, an empty DataFrame is returned.
    """
    gog_url = f'https://catalog.gog.com/v1/catalog?countryCode={country_dict_gog[currency]}'  # GOG API URL
    gog_params = {
        "limit": "48",
        "query": game_title,
        "system": platform_dict_gog[platform],
        "currencyCode": currency,
    }

    gog_object = re.get(url=gog_url, params=gog_params)  # Fetch data from GOG API
    if gog_object.status_code == 200:
        # Get titles, prices, links and images
        titles = []
        prices = []
        links = []
        images = []
        for product in gog_object.json()["products"]:
            titles.append(product["title"])  # Append title
            prices.append(product["price"]["final"])  # Append price
            links.append(product["storeLink"])  # Append link
            images.append(product["coverHorizontal"])  # Append image
        data = {"title": titles, "price": prices, "link": links, "image": images}
        df_gog = pd.DataFrame(data)  # Create DataFrame
        df_gog["vendor"] = "GOG"  # Add vendor column
        return df_gog
    else:
        # Create an empty DataFrame
        empty_df = pd.DataFrame()

        # Return the empty DataFrame
        return empty_df


def fetch_cdkeys_data(
    game_title, currency, re, pd,
):
    """
    Fetches data from the CDKeys store page and returns it as a pandas DataFrame.

    Parameters:
    products (list): A list of dictionaries containing product information from the CDKeys store.

    Returns:
    pd.DataFrame: A DataFrame containing the fetched data with columns 'title', 'price', 'link', 'image', and 'vendor'.
                  If no data is fetched, an empty DataFrame is returned.
    """
    cdkeys_url = "https://muvyib7tey-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.1)%3B%20Browser%3B%20instantsearch.js%20(4.41.0)%3B%20Magento2%20integration%20(3.10.5)%3B%20JS%20Helper%20(3.8.2"
    cdkeys_form_data = {
        "requests": [
            {
                "indexName": "magento2_default_products",
                "params": f"highlightPreTag=__ais-highlight__&highlightPostTag=__%2Fais-highlight__&page=0&ruleContexts=%5B%22magento_filters%22%5D&hitsPerPage=24&clickAnalytics=true&query={game_title}&maxValuesPerFacet=10&facets=%5B%22restricted_countries.es_es%22%2C%22platforms.es_es%22%2C%22region.es_es%22%2C%22language.es_es%22%2C%22genres.es_es%22%2C%22price.EUR.default%22%5D&tagFilters=&facetFilters=%5B%22restricted_countries.es_es%3A-ES%22%2C%5B%22platforms.es_es%3ASteam%22%5D%5D&numericFilters=%5B%22visibility_search.default%3D1%22%2C%5B%22region_id.default%3D39%22%2C%22region_id.default%3D38%22%2C%22region_id.default%3D394%22%2C%22region_id.default%3D479%22%2C%22region_id.default%3D3382%22%2C%22region_id.default%3D3505%22%5D%5D",
            }
        ]
    }
    cdkeys_headers = {
        "Accept-Language": "es-ES;q=0.8,es;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "1472",
        "Host": "muvyib7tey-dsn.algolia.net",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "X-Algolia-Api-Key": "ODNjY2VjZjExZGE2NTg3ZDkyMGQ4MjljYzYwM2U0NmRjYWI4MDgwNTQ0NjgzNmE2ZGQyY2ZmMDlkMzAyYTI4NXRhZ0ZpbHRlcnM9",
        "X-Algolia-Application-Id": "MUVYIB7TEY",
    }
    cdkeys_object = re.post(
        url=cdkeys_url, json=cdkeys_form_data, headers=cdkeys_headers
    )  # Fetch data from CDKeys API
    if cdkeys_object.status_code == 200:
        # Get titles, prices, links and images
        titles = []
        prices = []
        links = []
        images = []
        for product in cdkeys_object.json()["results"][0]["hits"]:
            titles.append(product["name"]["default"])  # Append title
            prices.append(product["price"][currency]["default"])  # Append price
            links.append(product["url"]["default"])  # Append link
            images.append(product["thumbnail_url"]["default"])  # Append image
        data = {"title": titles, "price": prices, "link": links, "image": images}
        df_cdkeys = pd.DataFrame(data)  # Create DataFrame
        df_cdkeys["vendor"] = "CDKeys"  # Add vendor column
        return df_cdkeys
    else:
        # Create an empty DataFrame
        empty_df = pd.DataFrame()

        # Return the empty DataFrame
        return empty_df


def fetch_instan_gaming_data(
    game_title, currency, platform, re, pd, BeautifulSoup, platform_dict_instant_gaming
):
    """
    Fetches data from the Instant-Gaming store page and returns it as a pandas DataFrame.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML of the Instant-Gaming store page.
    titles (list): A list to store the titles of the games.
    prices (list): A list to store the prices of the games.
    links (list): A list to store the links to the games.
    images (list): A list to store the images of the games.

    Returns:
    pd.DataFrame: A DataFrame containing the fetched data with columns 'title', 'price', 'link', 'image', and 'vendor'.
                  If no data is fetched, an empty DataFrame is returned.
    """
    url = f"https://www.instant-gaming.com/es/busquedas/?platform%5B%5D={platform_dict_instant_gaming[platform]}&query={game_title}&currency={currency}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    instant_gaming_object = re.get(url, headers=headers)  # Fetch data from Instant-Gaming

    if instant_gaming_object.status_code == 200:
        soup = BeautifulSoup(instant_gaming_object.content, "html.parser")
        # Get the titles list
        titles = []
        prices = []
        images = []
        links = []
        for x in soup.find_all('div', class_='item force-badge'):
            titles.append(x.find('span', class_='title').text)
            try:
                prices.append(x.find('div', class_='price').text)
            except:
                prices.append('')
            images.append(str(x.find('img', class_='picture')).strip().split('src="')[1].split('"')[0])
            links.append(x.find('a').get('href'))        
        data = {"title": titles, "price": prices, "link": links, "image": images}
        df_instant_gaming = pd.DataFrame(data)  # Create DataFrame
        df_instant_gaming["vendor"] = "Instant-Gaming"  # Add vendor column
        return df_instant_gaming
    else:
        # Create an empty DataFrame
        empty_df = pd.DataFrame()

        # Return the empty DataFrame
        return empty_df


def fetch_epic_games_data(
    re, pd, game_title, currency_dict_steam, currency,
):
    """
    Fetches data from the Epic Games store page and returns it as a pandas DataFrame.

    Parameters:
    products (list): A list of dictionaries containing product information from the Epic Games store.

    Returns:
    pd.DataFrame: A DataFrame containing the fetched data with columns 'title', 'price', 'link', 'image', and 'vendor'.
                  If no data is fetched, an empty DataFrame is returned.
    """
    epic_games_url = f"https://epic-games-store.p.rapidapi.com/search/{game_title}/page/1/country/{currency_dict_steam[currency]}/locale/us"
    epic_games_headers = {
        "x-rapidapi-key": "c6a5a891ecmsh03d9ec66402dd34p18a3c6jsnbe65087e49e4",
        "x-rapidapi-host": "epic-games-store.p.rapidapi.com",
    }
    epic_games_object = re.get(url=epic_games_url, headers=epic_games_headers)  # Fetch data from Epic Games API
    if epic_games_object.status_code == 200:
        # Get titles, prices, links and images
        titles = []
        prices = []
        links = []
        images = []
        for product in epic_games_object.json()["Catalog"]["searchStore"]["elements"]:
            titles.append(product["title"])  # Append title
            prices.append(product["price"]["totalPrice"]["discountPrice"] / 100)  # Append price
            term = product["title"].replace(" ", "+")
            links.append(
                f"https://store.epicgames.com/en-US/browse?q={term}&sortBy=relevancy&sortDir=DESC&count=40"
            )  # Append link
            images.append("Not available")  # Append image placeholder
        data = {"title": titles, "price": prices, "link": links, "image": images}
        df_epic_games = pd.DataFrame(data)  # Create DataFrame
        df_epic_games["vendor"] = "Epic Games"  # Add vendor column
        return df_epic_games
    else:
        # Create an empty DataFrame
        empty_df = pd.DataFrame()

        # Return the empty DataFrame
        return empty_df

def build_final_df(
        df_steam, 
        df_gog, 
        df_cdkeys, 
        df_instant_gaming, 
        df_epic_games,
        pd
):
    """
    Combines data from multiple DataFrames into a single DataFrame and sorts it by price.

    Parameters:
    df_steam (pd.DataFrame): DataFrame containing data from the Steam store.
    df_gog (pd.DataFrame): DataFrame containing data from the GOG store.
    df_cdkeys (pd.DataFrame): DataFrame containing data from the CDKeys store.
    df_instant_gaming (pd.DataFrame): DataFrame containing data from the Instant-Gaming store.
    df_epic_games (pd.DataFrame): DataFrame containing data from the Epic Games store.
    pd (module): The pandas module.

    Returns:
    pd.DataFrame: A combined DataFrame containing data from all the input DataFrames, sorted by price.
    """
    df_final = pd.concat([df_steam, df_gog, df_cdkeys, df_instant_gaming, df_epic_games]).reset_index(drop=True)  # Combine all DataFrames
    df_final['price'] = pd.to_numeric(df_final['price'].astype('str').str.replace('$', '').str.replace('€', '').str.replace(',', '.').replace('Free', '').fillna(0))  # Convert price to numeric
    return df_final.sort_values('price')  # Sort the final DataFrame by price

def start_over(st):
    st.session_state['game_title'] = ''