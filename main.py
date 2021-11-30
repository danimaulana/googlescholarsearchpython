from bs4 import BeautifulSoup
import requests, lxml, os, json

print("Program Search Google Scholar")
text = input("Masukkan Keyword : ")

proxies = {
  'http': os.getenv('HTTP_PROXY') # or just type proxy here without os.getenv()
}

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
  "q": text,
  "hl": "en",
}

html = requests.get('https://scholar.google.com/scholar', headers=headers, params=params, proxies=proxies).text
soup = BeautifulSoup(html, 'lxml')

# Scrape just PDF links
for pdf_link in soup.select('.gs_or_ggsm a'):
  pdf_file_link = pdf_link['href']
  print(pdf_file_link)

# JSON data will be collected here
data = []

# Container where all needed data is located
for result in soup.select('.gs_ri'):
  title = result.select_one('.gs_rt').text
  title_link = result.select_one('.gs_rt a')['href']
  publication_info = result.select_one('.gs_a').text
  snippet = result.select_one('.gs_rs').text
  cited_by = result.select_one('#gs_res_ccl_mid .gs_nph+ a')['href']
  related_articles = result.select_one('a:nth-child(4)')['href']
  try:
    all_article_versions = result.select_one('a~ a+ .gs_nph')['href']
  except:
    all_article_versions = None

  data.append({
    'title': title,
    'title_link': title_link,
    'publication_info': publication_info,
    'snippet': snippet,
    'cited_by': f'https://scholar.google.com{cited_by}',
    'related_articles': f'https://scholar.google.com{related_articles}',
    'all_article_versions': f'https://scholar.google.com{all_article_versions}',
  })

print(json.dumps(data, indent = 2, ensure_ascii = False))