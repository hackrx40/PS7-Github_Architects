import http.client
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.views.decorators.http import require_GET


@api_view(['POST'])
def get_instagram_profile(request):
    username = request.data.get('username', '')
    if not username:
        return JsonResponse({'error': 'Username parameter is missing.'}, status=400)

    conn = http.client.HTTPSConnection("scraper-api.smartproxy.com")
    payload = json.dumps({
        "target": "instagram_profile",
        "url": f"https://www.instagram.com/{username}/",
        "locale": "en",
        "geo": "India"
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic UzAwMDAxMTExMjE6UCRXMTM5YThjMmQwNTM2NTg2MmI5ZTk0Y2IzZjM3NzAzMzJj',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/scrape", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    json_data = json.loads(data)
    response_data = {}

    if "data" in json_data:
        profile_data = json_data["data"]["content"]["account"]

        response_data["username"] = profile_data["username"]
        response_data["verified"] = profile_data["verified"]

        stats_data = json_data["data"]["content"]["stats"]
        response_data["posts"] = stats_data["posts"]
        response_data["followers"] = stats_data["followers"]
        response_data["following"] = stats_data["following"]

        biography_data = json_data["data"]["content"]["biography"]
        response_data["name"] = biography_data["name"]
        response_data["occupation"] = biography_data["occupation"]
        response_data["url"] = biography_data["url"]

        posts_data = json_data["data"]["content"]["posts"]
        response_data["posts"] = [post["href"] for post in posts_data]

        related_accounts_data = json_data["data"]["content"]["relatedAccounts"]
        response_data["related_accounts"] = [account["username"] for account in related_accounts_data]
    else:
        response_data["error"] = "Posts data not found for the account."

    return JsonResponse(response_data)

@csrf_exempt
@require_POST
def get_instagram_stats(request):
    payload = json.loads(request.body)
    post_links = payload.get('post_links', [])

    result = []
    for link in post_links:
        conn = http.client.HTTPSConnection("scraper-api.smartproxy.com")
        payload = json.dumps({
            "target": "instagram_post",
            "url": link,
            "locale": "en",
            "geo": "India"
        })
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Basic UzAwMDAxMTExMjE6UCRXMTM5YThjMmQwNTM2NTg2MmI5ZTk0Y2IzZjM3NzAzMzJj',
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/scrape", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        response = json.loads(data)
        
        # Extract the required information from the response
        comments = response['data']['content']['comments']
        extracted_info = [{'username': comment['username'], 'likes': comment['likes'], 'replies': comment['replies'], 'comment': comment['comment']} for comment in comments]
        
        result.append({'post_link': link, 'comments': extracted_info})
    
    return JsonResponse(result, safe=False)

@api_view(['POST'])
def get_instagram_posts(request):
    hashtag = request.data.get('hashtag', '')
    
    conn = http.client.HTTPSConnection("scraper-api.smartproxy.com")
    payload = json.dumps({
        "target": "instagram_graphql_hashtag",
        "url": f"https://www.instagram.com/explore/tags/{hashtag}/",
        "locale": "en",
        "geo": "India"
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic UzAwMDAxMTExMjE6UCRXMTM5YThjMmQwNTM2NTg2MmI5ZTk0Y2IzZjM3NzAzMzJj',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/scrape", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    edges = data['data']['content']['hashtag']['edge_hashtag_to_media']['edges']
    post_links = [f"https://www.instagram.com/p/{edge['node']['shortcode']}/" for edge in edges]
    
    return Response({'post_links': post_links})


@api_view(['POST'])
def get_subreddit_data(request):
    subreddit_name = request.data.get('subreddit_name', '')

    conn = http.client.HTTPSConnection("scraper-api.smartproxy.com")
    payload = json.dumps({
        "target": "reddit_subreddit",
        "url": f"https://www.reddit.com/r/{subreddit_name}/",
        "locale": "en",
        "geo": "India"
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic UzAwMDAxMTExMjE6UCRXMTM5YThjMmQwNTM2NTg2MmI5ZTk0Y2IzZjM3NzAzMzJj',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/scrape", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    children_data = data['data']['content']['data']['children']
    response_data = []

    for child in children_data:
        child_data = child['data']
        response_data.append({
            'selftext': child_data['selftext'],
            'author_fullname': child_data['author_fullname'],
            'title': child_data['title'],
            'name': child_data['name'],
            'upvote_ratio': child_data['upvote_ratio'],
            'score': child_data['score'],
            'author': child_data['author'],
            'subreddit_subscribers': child_data['subreddit_subscribers']
        })

    return Response(response_data)


@csrf_exempt
@require_POST
def get_tweets(request):
    data = json.loads(request.body.decode('utf-8'))
    keyword = data.get('keyword', '')
    count = data.get('count', '20')  # Default count is set to 20 if not provided
    until = data.get('until')  # Optional parameter 'until' for the date filter
    print(keyword, count, until)
    
    url = "https://twitter135.p.rapidapi.com/v1.1/SearchTweets/"

    querystring = {"q": keyword, "count": count}
    
    if until:
        querystring['until'] = until

    headers = {
        'X-RapidAPI-Key': '7e7d825c09mshdf576f7bb75175ep1418b5jsnb9d3d7ad6763',
        'X-RapidAPI-Host': 'twitter135.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    
    tweets = []
    for status in data.get('statuses', []):
        tweet = {
            'created_at': status.get('created_at', ''),
            'full_text': status.get('full_text', ''),
            'user': {
                'name': status['user'].get('name', ''),
                'screen_name': status['user'].get('screen_name', ''),
                'location': status['user'].get('location', ''),
                'followers_count': status['user'].get('followers_count', 0),
                'friends_count': status['user'].get('friends_count', 0),
            },
            'lang': status.get('lang', ''),
        }
        tweets.append(tweet)

    return JsonResponse({'tweets': tweets})

def convert_dict_to_csv(data_dict):
    # Get the keys from the dictionary
    keys = list(data_dict.keys())

    # Specify the temporary file path to save the CSV file
    temp_file_path = "/path/to/temporary/file.csv"

    # Convert the dictionary to a list of rows
    rows = [keys]
    for values in zip(*[map(str, value) for value in data_dict.values()]):
        rows.append(values)

    # Save the rows to the temporary CSV file
    with open(temp_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

    # Return the temporary file path
    return temp_file_path


import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from leads.models import FacebookPost
from facebook_scraper import get_posts

@csrf_exempt
def scrape_facebook_page(request):
    if request.method == 'POST':
        data = request.POST
        page_url = data.get('page_url', '')

        # Scrape Facebook page data
        posts = []
        print(get_posts(page_url, pages=5, lang='en', extra_info=True))
        for post in get_posts(page_url, pages=5, lang='en', extra_info=True):  # Specify the number of pages to scrape
            post_data = {
                'account_name': post['username'],
                'post_content': post['text'],
                'likes': post['likes'],
                'comments': post['comments'],
                'shares': post['shares'],
            }
            posts.append(post_data)
            print(post_data)

            # Store the post data in the database
            FacebookPost.objects.create(**post_data)

        # Retrieve all stored Facebook posts from the database
        stored_posts = list(FacebookPost.objects.all().values())

        return JsonResponse({'new_posts': posts, 'stored_posts': stored_posts})

    return JsonResponse({'message': 'Invalid request method'})

@csrf_exempt
def save_posts(request):
    if request.method == 'POST':
        # data = json.loads(request.body.decode('utf-8'))
        combined_json = [
  {
    "account_name": "Bajaj Allianz life insurance",
    "post_content": "Public · 817 members · 5 posts a week\n\n*BAJAJ ALLIANZ LIFE INSURANCE INVESTMENT PLANS AND BENEFITS* • tax benefits & Saving • Family Protection • child Education/ Marriage plan • Retirement plan • returns getting is guaranted My solution is guaranteed for life - Guaranted returns - safety of money - liquidity options - Pension for lifetime - joint life with cash back - high returns U can Attach MWPA ( MARRIED WOMEN PROPERTY ACT) > ADVANTAGES:- • Wife & childrens • Money get secured againts banks, courts and creditors attachment It is covered under section 80C and 10 (10D) For More Details Contact 📲 Mr. Sanket Kadam :- 9892639513 🏠 𝐒𝐓𝐀𝐘 𝐇𝐎𝐌𝐄 𝐒𝐓𝐀𝐘 𝐒𝐀𝐅𝐄 🏠",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Bajaj Allianz life Insurance co.Ltd",
    "post_content": "Public · 136 members · 5 posts a week\n\nUrgently Required For The Post of Insurance Consultant for Bajaj Allianz Pvt Ltd. For more details Comments Me.",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Bajaj Allianz life insurance",
    "post_content": "Public · 74 members · 7 posts a month\n\nBajaj Allianz life insurance Hum apke sath h Humare sath jud kar kaam karene ke liye contact jariye ...... Ek better plan kariye apne aour apni family � ke sath sath.... Ek Good Earing �",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Kalyan Dombivali Thane Job Opportunity",
    "post_content": "DP Singh\n3 days ago\n\nBajaj Group Company\nUrgent Recruitment\n25 Male And Female Candidates… See more",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Arun Saxena",
    "post_content": "23 June at 10:00\n\nBuy today Bajaj Allianz life insurance company Plans for enquiry call me at 98106 87681",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Vrushi property's is in India.",
    "post_content": "23 June at 15:59\n\nBAJAJ ALLIANZ LIFE INSURANCE\nINTERESTED CALL ME 082915 41823 📞\nBEST INVESTMENT FOR LIFE\nVrushi property's\nProperty company",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Banuka Gopi",
    "post_content": "2 days ago\n\n# In London (UK) lo Naku \"Bajaj Allianz Life Insurance co Ltd\" Naku vachina Award",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Future life Advisor Group",
    "post_content": "3 July at 13:19\n\nWE ARE HIRING: FINANCIAL ADVISORS / INSURANCE AGENTS For Bajaj Allianz Life insurance company.\n(Part-time/Full-time)\nWHO CAN APPLY … See more",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Bajaj Allianz Association of india",
    "post_content": "Bajaj Allianz Association of india\nCHAT.WHATSAPP.COM\nBajaj Allianz Association of india\nWhatsApp Group Invite",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Er Mohan Sharma",
    "post_content": "3 July at 23:21\n\nGeneral Insurance festival of India(GIFI) conducted by Bajaj Allianz GIC Ltd Pune. Become a member of this grand fest. Thanks everyone for your support..",
    "keyword": "bajajallianzlifeinsurance"
  },
  {
    "account_name": "Monika Nigam Chauhan",
    "post_content": "a day ago\n\nContact no.-9999437603\nCompany name-:bajaj Allianz Life insurance company\nPost-: retail partner\nSalary 19000+ incentive\nJob details BAJAJ ALLIANZ LIFE INSURANCE COMPANY ( BALIC ) … See more",
    "keyword": "bajajallianzlifeinsurance"
  }
]

        combined_json=json.dumps(combined_json)
        # Parse the JSON object
        posts_data = json.loads(combined_json)

        # Iterate over the posts and save them
        for post_data in posts_data:
            post = Post(
                account_name=post_data['account_name'],
                post_content=post_data['post_content'],
                keyword=post_data['keyword']
            )
            post.save()

        return JsonResponse({'message': 'Posts saved successfully.'})

    return JsonResponse({'error': 'Invalid request method.'})