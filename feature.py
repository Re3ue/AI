########## ########## ########## ##########

# Import : Internal
from datetime import datetime
from collections import Counter
import re
import socket
import urllib.parse
import math
from collections import Counter
import string
import sys

# Import : External
import requests
import tldextract

########## ########## ########## ##########

SUSPICIOUS_TLD = {
    # Free / Cheap ccTLD
    'tk', 'ml', 'ga', 'cf', 'gq',

    # Common gTLD
    'xyz', 'top', 'club', 'online', 'site', 'win', 'bid', 'loan', 'date', 'click',
    'work', 'party', 'gdn', 'stream', 'cricket', 'faith', 'science', 'webcam', 'download',
    'racing', 'men', 'accountant', 'trade', 'review', 'zip', 'cam', 'host', 'rest', 'space',

    # New gTLD
    'buzz', 'fit', 'mom', 'bar', 'kim', 'tokyo', 'wang', 'ooo', 'fun', 'icu', 'pro',
    'cyou', 'run', 'surf', 'monster', 'support', 'live', 'today', 'press', 'rocks',
    'lol', 'pics', 'help', 'gratis', 'mls', 'ink', 'moe', 'red', 'blue', 'black',

    # Low Trust Business / Promotion TLD
    'store', 'review', 'accountants', 'christmas', 'download', 'fail', 'gratis', 'host',
    'link', 'market', 'ninja', 'ooo', 'party', 'racing', 'review', 'science', 'space',
    'stream', 'trade', 'webcam', 'win', 'work', 'zip', 'biz', 'cc', 'tk', 'pw', 'cf',
    'gdn', 'cam', 'men', 'date', 'rest', 'click', 'uno', 'asia', 'buzz', 'icu', 'site',

    # Recent Flag from Threat Intelligence Feed
    'vip', 'dev', 'solutions', 'finance', 'broker', 'host', 'place', 'cloud', 'marketing',
    'email', 'cheap', 'zone', 'equipment', 'technology', 'directory', 'institute'
}

PHISHING_HINT = [
    # Core Log-In / Account Term
    'login', 'signin', 'logon', 'auth', 'authenticate', 'verify', 'verification', 'account', 'user',
    'id', 'password', 'passcode', 'credentials', 'session', 'access', 'profile', 'member', 'portal',

    # Security / Trust
    'secure', 'protection', 'security', 'safe', 'trusted', 'verify', '2fa', 'otp', 'mfa', 'token',
    'certified', 'encrypted', 'shield', 'authenticator',

    # Urgency / Action Trigger
    'update', 'confirm', 'validate', 'reactivate', 'unlock', 'restore', 'reset', 'recovery',
    'deactivate', 'limit', 'suspend', 'alert', 'warning', 'important',

    # Financial Trigger
    'bank', 'billing', 'payment', 'invoice', 'transaction', 'refund', 'claim', 'balance', 'deposit',
    'withdraw', 'transfer', 'wire', 'statement',

    # Support / Contact
    'support', 'help', 'service', 'customer', 'desk', 'center', 'contact', 'email', 'call',

    # Fake System / Official Term
    'admin', 'webmail', 'portal', 'dashboard', 'console', 'cpanel', 'mailbox', 'myaccount',
    'system', 'netbanking', 'eservices', 'gov', 'irs', 'service', 'loginpage',

    # ETC
    'official', 'verify-now', 'account-check', 'login-secure', 'confirm-id', 'update-info',
    'secure-login', 'account-verify', 'id-check', 'user-verification'
]

BRAND = [
    # Finance & Payment
    'paypal', 'paypalme', 'visa', 'mastercard', 'americanexpress', 'amex', 'chase', 'boa', 'wellsfargo',
    'capitalone', 'tdbank', 'revolut', 'n26', 'monzo', 'santander', 'barclays', 'postbank', 'intuit',
    'quickbooks', 'cashapp', 'zelle', 'venmo', 'robinhood', 'coinbase', 'binance', 'kraken', 'blockchain',
    'sofi', 'ally', 'discover', 'firstrepublic', 'etrade', 'swissbank', 'dbs', 'icicibank', 'nab', 'anz',

    # E-Mail & Web Account
    'google', 'gmail', 'outlook', 'hotmail', 'yahoo', 'aol', 'icloud', 'protonmail', 'zoho', 'gmx',
    'mailchimp', 'fastmail', 'tutanota', 'yandex', '163mail', 'squirrelmail', 'roundcube',

    # Tech & Cloud
    'github', 'gitlab', 'bitbucket', 'azure', 'aws', 'gcp', 'digitalocean', 'heroku', 'netlify', 'vercel',
    'dropbox', 'box', 'mega', 'icloud', 'onedrive', 'weebly', 'wordpress', 'joomla', 'drupal', 'wix',

    # E-Commerce & Retail
    'amazon', 'amazonprime', 'ebay', 'aliexpress', 'alibaba', 'target', 'walmart', 'costco', 'bestbuy',
    'homedepot', 'lowes', 'newegg', 'shopify', 'flipkart', 'rakuten', 'mercado', 'jd', 'coupang', 'gmarket',

    # Shipping & Delivery
    'dhl', 'fedex', 'ups', 'usps', 'canadapost', 'hermes', 'auspost', 'postnl', 'royalmail', 'gls',
    'colissimo', 'dpd', 'cjlogistics', 'yamato', 'lalamove', 'grabexpress',

    # Media & Streaming
    'netflix', 'spotify', 'hulu', 'disneyplus', 'primevideo', 'paramountplus', 'applemusic', 'hbomax',
    'youtube', 'twitch', 'vimeo', 'pandora', 'deezer', 'sling', 'crunchyroll',

    # Social Media & Communication
    'facebook', 'instagram', 'whatsapp', 'messenger', 'telegram', 'tiktok', 'twitter', 'linkedin', 'pinterest',
    'snapchat', 'line', 'wechat', 'kakaotalk', 'discord', 'reddit', 'quora', 'tumblr', 'skype', 'viber',

    # Gaming
    'steam', 'epicgames', 'origin', 'battle.net', 'riotgames', 'playstation', 'xbox', 'nintendo', 'roblox',
    'ea', 'bungie', 'rockstargames', 'minecraft', 'fortnite', 'pubg', 'genshin', 'valorant',

    # Travel & Booking
    'airbnb', 'booking', 'expedia', 'tripadvisor', 'trivago', 'klook', 'agoda', 'hotels', 'skyscanner',
    'delta', 'united', 'emirates', 'qatarairways', 'singaporeair', 'koreanair', 'jejuair', 'jetblue',

    # Crypto Currency Service
    'metamask', 'trustwallet', 'blockchain', 'bitfinex', 'bitstamp', 'poloniex', 'crypto', 'gemini', 'bybit',
    'bitmart', 'lbank', 'okx', 'gateio', 'kucoin',

    # Government & Institution
    'irs', 'usps', 'gov', 'govuk', 'govkr', 'nhbank', 'kb', 'shinhan', 'wooribank', 'kebhana', 'boc',
    'gouv', 'unitednations', 'who', 'europa', 'snu', 'kaist', 'mit', 'harvard', 'cambridge', 'oxford',

    # ETC
    'zoom', 'uber', 'lyft', 'airasia', 'doordash', 'grubhub', 'ubereats', 'naver', 'kakao', 'baidu',
    'toss', 'linepay', 'gmarket', '11st', 'tmon', 'wemakeprice', 'interpark', 'samsung', 'lg', 'huawei',
    'xiaomi', 'oppo', 'vivo', 'nvidia', 'intel', 'amd', 'docusign', 'adobe', 'cloudflare', 'norton',
    'mcafee', 'avast', 'avg', 'bitdefender', 'kaspersky', 'eset', 'zoominfo', 'zendesk', 'jira', 'confluence',
    'notion', 'slack', 'asana', 'monday', 'clickup', 'trello', 'mailgun', 'sendgrid', 'twilio', 'stripe',
    'square', 'klarna', 'afterpay', 'affirm', 'wise', 'remitly', 'transferwise', 'remit', 'billdesk',
    'razorpay', 'paytm', 'mobikwik', 'phonepe', 'gpay', 'alipay', 'wechatpay'
]

SHORTENING = {
    'bit.ly', 'goo.gl', 'tinyurl.com', 't.co', 'ow.ly', 'is.gd', 'buff.ly',
    'adf.ly', 'bit.do', 'mcaf.ee', 'rebrand.ly', 'su.pr', 'shorte.st', 'cli.gs',
    'v.gd', 'url.kr', 'buly.kr', 'alie.kr', 'link24.kr', 'lrl.kr', 'tr.ee',
    't.ly', 't.me', 'rb.gy', 'shrtco.de', 'chilp.it', 'cutt.ly', 'vvd.bz',
    'iri.my', 'linc.kr', 'abit.ly', 'chzzk.me', 'flic.kr', 'glol.in', 'gourl.kr',
    'han.gl', 'juso.ga', 'muz.so', 'na.to', 't2m.kr', 'tny.kr',
    'tuney.kr', 'twr.kr', 'ual.kr', 'url.sg', 'vo.la', 'wo.to', 'yao.ng',
    'zed.kr', 'zxcv.be'
}

SPECIAL_CHARACTER = ['.', '-', '@', '?', '&', '=', '_', '~', '%', '/', '*', ':', ',', ';', '$', ' ']

CHARACTER_KEY_MAP = {
    '.': 'dot',
    '-': 'hyphen',
    '@': 'at',
    '?': 'question',
    '&': 'and',
    '=': 'equal',
    '_': 'underscore',
    '~': 'tilde',
    '%': 'percent',
    '/': 'slash',
    '*': 'star',
    ':': 'colon',
    ',': 'comma',
    ';': 'semicolon',
    '$': 'dollar',
    ' ': 'space'
}

########## ########## ########## ##########

def shannon_entropy(text) :
    if not text :
        return 0
    
    freq = Counter(text)
    probs = [count / len(text) for count in freq.values()]

    return -sum(p * math.log2(p) for p in probs if p > 0)

def extract_abnormal_subdomain(tldextract_result) :
    subdomains = tldextract_result.subdomain.split('.')

    for sub in subdomains :
        if len(sub) == 0 :
            continue

        entropy = shannon_entropy(sub)

        long_digit_flag = re.search(r'\d{5,}', sub) is not None

        # Case - Abnormal
        if entropy > 3.5 or long_digit_flag :
            return 1
        
    return 0

def look_like_random(domain) :
    entropy = shannon_entropy(domain)

    letter_flag = any(c in string.ascii_lowercase for c in domain)
    digit_flag = any(c in string.digits for c in domain)

    # Heuristic
    return int(entropy > 3.5 and letter_flag and digit_flag)

def get_root_domain(hostname : str) -> str :
    if not hostname :
        return ''
    
    tldextract_result = tldextract.extract(hostname)
    
    if tldextract_result.domain and tldextract_result.suffix :
        return f"{tldextract_result.domain}.{tldextract_result.suffix}"
    
    return ''

def check_ip(domain) :
    try :
        socket.inet_aton(domain)

        return True
    
    except socket.error :
        return False

def check_redirect(url) :
    try :
        response = requests.get(url, timeout=3, allow_redirects=True)

        redirects = response.history

        count_redirect = len(redirects)
        count_external_redirect = sum(1 for redirect in redirects if urllib.parse.urlparse(redirect.url).netloc != urllib.parse.urlparse(url).netloc)

        return count_redirect, count_external_redirect
    
    except :
        return -1, -1 # Fail to Access

########## ########## ########## ##########

def extract_features(url) :
    features = {}

    # URL => Parse URL
    parse_result = urllib.parse.urlparse(url) # Get
    tldextract_result = tldextract.extract(url) # Get

    # Parse URL => Set Information
    full_url = url
    hostname = parse_result.hostname or ''
    path = parse_result.path or ''
    root_domain = get_root_domain(hostname.lower())

    # Feature #1 ~ #4
    features['length_url'] = len(full_url)
    features['length_hostname'] = len(hostname)
    features['port'] = 1 if parse_result.port else 0
    features['path_extension'] = 1 if re.search(r'\.(exe|apk|scr|zip|rar|js|bat|dll)$', path, re.IGNORECASE) else 0 # ?

    # Feature #5 ~ #20
    for character in SPECIAL_CHARACTER:
        key = f"count_{CHARACTER_KEY_MAP.get(character, character)}"

        features[key] = full_url.count(character)

    # Feature #21 ~ #22
    features['count_tld'] = full_url.count('.' + tldextract_result.suffix)
    features['count_doubleslash'] = full_url.count('//') - 1 # Except - "http(s)://"

    # Feature #23 ~ #32
    features['ip'] = 1 if check_ip(hostname) else 0
    features['http_in_path'] = 1 if 'http' in path.lower() else 0
    features['https_in_path'] = 1 if 'https' in path.lower() else 0
    features['punycode'] = 1 if 'xn--' in hostname else 0
    features['tld_in_path'] = 1 if tldextract_result.suffix in path else 0
    features['tld_in_subdomain'] = 1 if tldextract_result.suffix in tldextract_result.subdomain else 0
    features['count_subdomain'] = len(tldextract_result.subdomain.split('.')) if tldextract_result.subdomain else 0
    features['abnormal_subdomain'] = extract_abnormal_subdomain(tldextract_result)
    features['random_domain'] = look_like_random(tldextract_result.domain)
    features['shortening_service'] = 1 if root_domain in SHORTENING else 0

    # Feature #33 ~ #35
    digit_count_url = sum(character.isdigit() for character in full_url)
    digit_count_host = sum(character.isdigit() for character in hostname)

    features['ratio_digit_url'] = digit_count_url / len(full_url)
    features['ratio_digit_host'] = digit_count_host / len(hostname) if hostname else 0
    features['character_repeat'] = 1 if re.search(r'(.)\1{3,}', full_url) else 0

    # Feature #36 ~ #45
    delimiters = r"[./?&=:_\-%,;*$ ]"

    words_raw = re.split(delimiters, full_url)
    words_host = re.split(delimiters, hostname)
    words_path = re.split(delimiters, path)

    for prefix, words in [('word_raw', words_raw), ('word_host', words_host), ('word_path', words_path)] :
        words = list(filter(None, words)) # Except - Empty

        lengths = [len(w) for w in words]

        if lengths :
            features[f'length_{prefix}'] = sum(lengths)
            features[f'shortest_{prefix}'] = min(lengths)
            features[f'longest_{prefix}'] = max(lengths)
            features[f'avg_{prefix}'] = sum(lengths) / len(lengths)
        
        else :
            features[f'length_{prefix}'] = 0
            features[f'shortest_{prefix}'] = 0
            features[f'longest_{prefix}'] = 0
            features[f'avg_{prefix}'] = 0

    # Feature #46 ~ #50
    url_lower = full_url.lower()

    features['phishing_hint'] = 1 if any(word in url_lower for word in PHISHING_HINT) else 0
    features['domain_in_brand'] = 1 if any(brand in tldextract_result.domain for brand in BRAND) else 0
    features['brand_in_subdomain'] = 1 if any(brand in tldextract_result.subdomain for brand in BRAND) else 0
    features['brand_in_path'] = 1 if any(brand in path for brand in BRAND) else 0
    features['suspicious_tld'] = 1 if tldextract_result.suffix in SUSPICIOUS_TLD else 0

    # Feature #51 ~ #52
    count_redirect, count_external_redirect = check_redirect(url)

    features['count_redirect'] = count_redirect
    features['count_external_redirect'] = count_external_redirect

    return features

# Main
if __name__ == "__main__" :
    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 feature.py < URL >")

        sys.exit(1)
    
    input_url = sys.argv[1]

    features = extract_features(input_url)
    
    print(f"{features}")